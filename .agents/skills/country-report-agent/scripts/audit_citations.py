#!/usr/bin/env python3
"""First-pass APA in-text citation to reference audit for country reports.

This script uses conservative heuristics. It is meant to surface likely issues
for human review, not to certify publication readiness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


YEAR_RE = r"(?:19|20)\d{2}[a-z]?|n\.d\."
PAREN_CITATION_RE = re.compile(r"\(([^()\n]{2,120}?(?:" + YEAR_RE + r")[^()\n]{0,80})\)")
NARRATIVE_CITATION_RE = re.compile(r"\b([A-Z][A-Za-z&.,' -]{1,80}?)\s+\((" + YEAR_RE + r")\)")
REFERENCE_YEAR_RE = re.compile(r"\((" + YEAR_RE + r")\)")


@dataclass(frozen=True)
class Citation:
    author: str
    year: str
    file: str
    line: int
    raw: str


@dataclass(frozen=True)
class Reference:
    author: str
    year: str
    raw: str
    has_locator: bool


def normalize_author(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\bet al\.\b", "", value)
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    stop = {"the"}
    return " ".join(part for part in value.split() if part not in stop)


def citation_key(author: str, year: str) -> tuple[str, str]:
    return (normalize_author(author), year.lower())


def reference_author_variants(author: str) -> set[str]:
    """Return APA-compatible author keys for one-, two-, and multi-author entries."""
    direct = normalize_author(author)
    surnames = re.findall(r"(?:^|,\s*(?:&\s*)?)([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+),\s*(?=[A-Z])", author)
    if not surnames:
        return {direct}
    normalized = [normalize_author(name) for name in surnames]
    variants = {direct, normalized[0]}
    if len(normalized) == 2:
        variants.add(f"{normalized[0]} and {normalized[1]}")
    elif len(normalized) >= 3:
        variants.add(f"{normalized[0]} et al")
    return {value for value in variants if value}


def split_parenthetical(raw: str) -> Iterable[tuple[str, str]]:
    parts = [part.strip() for part in raw.split(";")]
    for part in parts:
        match = re.search(r"(.+?),\s*(" + YEAR_RE + r")\b", part)
        if not match:
            continue
        author = match.group(1).strip()
        year = match.group(2).strip()
        if author and not author.lower().startswith(("see ", "e.g.", "cf.")):
            yield author, year


def iter_markdown_files(sections_dir: Path) -> Iterable[Path]:
    for path in sorted(sections_dir.glob("*.md")):
        if path.name.lower() in {"19-01-references.md", "19-references.md"}:
            continue
        yield path


def extract_citations(sections_dir: Path) -> list[Citation]:
    citations: list[Citation] = []
    for path in iter_markdown_files(sections_dir):
        rel = path.as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        for line_no, line in enumerate(lines, 1):
            for match in PAREN_CITATION_RE.finditer(line):
                for author, year in split_parenthetical(match.group(1)):
                    citations.append(Citation(author, year, rel, line_no, match.group(0)))
            for match in NARRATIVE_CITATION_RE.finditer(line):
                citations.append(Citation(match.group(1).strip(), match.group(2).strip(), rel, line_no, match.group(0)))
    return citations


def find_references_file(sections_dir: Path) -> Path | None:
    preferred = sections_dir / "19-01-references.md"
    if preferred.exists():
        return preferred
    candidates = sorted(sections_dir.glob("*reference*.md")) + sorted(sections_dir.glob("*references*.md"))
    return candidates[0] if candidates else None


def split_reference_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                blocks.append(" ".join(current).strip())
                current = []
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith(("-", "*")) and current:
            blocks.append(" ".join(current).strip())
            current = []
        current.append(stripped.lstrip("-* ").strip())
    if current:
        blocks.append(" ".join(current).strip())
    return [block for block in blocks if REFERENCE_YEAR_RE.search(block)]


def extract_references(reference_file: Path | None) -> list[Reference]:
    if reference_file is None:
        return []
    try:
        text = reference_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = reference_file.read_text(encoding="utf-8-sig")
    refs: list[Reference] = []
    for block in split_reference_blocks(text):
        year_match = REFERENCE_YEAR_RE.search(block)
        if not year_match:
            continue
        author = block[: year_match.start()].strip().rstrip(".")
        year = year_match.group(1)
        has_locator = bool(re.search(r"(https?://|doi\.org|DOI:|doi:|ISBN|WorldCat|local|archive|access)", block, re.I))
        refs.append(Reference(author, year, block, has_locator))
    return refs


def resolve_country_path(path: Path) -> tuple[Path, Path]:
    if (path / "sources" / "sections").exists():
        return path, path / "sources" / "sections"
    if path.name == "sections" and path.exists():
        return path.parents[1], path
    if (path / "sections").exists():
        return path.parent, path / "sections"
    raise SystemExit(f"Cannot locate sources/sections under: {path}")


def audit(country_path: Path) -> dict:
    country_root, sections_dir = resolve_country_path(country_path)
    reference_file = find_references_file(sections_dir)
    citations = extract_citations(sections_dir)
    references = extract_references(reference_file)

    cited_keys = {citation_key(c.author, c.year) for c in citations}
    ref_keys = {
        (variant, r.year.lower())
        for r in references
        for variant in reference_author_variants(r.author)
    }

    missing_refs = [c for c in citations if citation_key(c.author, c.year) not in ref_keys]
    uncited_refs = [
        r for r in references
        if not any((variant, r.year.lower()) in cited_keys for variant in reference_author_variants(r.author))
    ]
    weak_refs = [r for r in references if not r.has_locator]

    return {
        "country_root": country_root.as_posix(),
        "sections_dir": sections_dir.as_posix(),
        "reference_file": reference_file.as_posix() if reference_file else None,
        "citation_count": len(citations),
        "reference_count": len(references),
        "missing_reference_count": len(missing_refs),
        "uncited_reference_count": len(uncited_refs),
        "weak_reference_locator_count": len(weak_refs),
        "blocker_count": len(missing_refs),
        "warning_count": len(uncited_refs) + len(weak_refs),
        "editorial_review_required": bool(missing_refs or uncited_refs or weak_refs),
        "missing_references": [asdict(item) for item in missing_refs],
        "uncited_references": [asdict(item) for item in uncited_refs],
        "weak_reference_locators": [asdict(item) for item in weak_refs],
    }


def print_markdown(result: dict) -> None:
    print("# Citation Audit")
    print()
    print(f"- Country root: `{result['country_root']}`")
    print(f"- Sections dir: `{result['sections_dir']}`")
    print(f"- References file: `{result['reference_file'] or 'not found'}`")
    print(f"- In-text citations found: {result['citation_count']}")
    print(f"- Reference entries found: {result['reference_count']}")
    print(f"- Missing reference matches: {result['missing_reference_count']}")
    print(f"- Uncited reference entries: {result['uncited_reference_count']}")
    print(f"- References without DOI/URL/local/access locator: {result['weak_reference_locator_count']}")
    print()

    def rows(title: str, items: list[dict], columns: list[str]) -> None:
        print(f"## {title}")
        print()
        if not items:
            print("No issues found.")
            print()
            return
        print("| " + " | ".join(columns) + " |")
        print("| " + " | ".join(["---"] * len(columns)) + " |")
        for item in items[:200]:
            values = [str(item.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
            print("| " + " | ".join(values) + " |")
        if len(items) > 200:
            print()
            print(f"Showing first 200 of {len(items)} issues.")
        print()

    rows("In-Text Citations Missing Final References", result["missing_references"], ["raw", "author", "year", "file", "line"])
    rows("Final References Not Cited In Manuscript", result["uncited_references"], ["author", "year", "raw"])
    rows("Reference Entries Missing Locator", result["weak_reference_locators"], ["author", "year", "raw"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit APA in-text citations against final references.")
    parser.add_argument("country_path", help="Country folder, sources folder, or sources/sections folder")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--summary", action="store_true", help="Emit one-line counts only")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit 1 when missing reference matches are found")
    args = parser.parse_args()

    result = audit(Path(args.country_path).resolve())
    if args.summary:
        print(
            "citations={citation_count} references={reference_count} "
            "missing={missing_reference_count} uncited={uncited_reference_count} "
            "weak_locators={weak_reference_locator_count}".format(**result)
        )
    elif args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_markdown(result)
    return 1 if args.fail_on_issues and result["missing_reference_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
