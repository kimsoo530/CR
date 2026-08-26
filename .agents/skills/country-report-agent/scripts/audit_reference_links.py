#!/usr/bin/env python3
"""Audit rendered country-report citation links and reference anchors."""

from __future__ import annotations

import argparse
import html
import re
from collections import Counter
from pathlib import Path


YEAR = r"(?:19|20)\d{2}[a-z]?|n\.d\."
CITATION_LINK_RE = re.compile(
    r"<a\b[^>]*\bclass=['\"][^'\"]*\bcitation-link\b[^'\"]*['\"][^>]*"
    r"\bhref=['\"]([^'\"]+)['\"][^>]*>",
    re.IGNORECASE,
)
ID_RE = re.compile(r"\bid=['\"]([^'\"]+)['\"]", re.IGNORECASE)
REFERENCE_ENTRY_RE = re.compile(
    r"<p\b[^>]*\bclass=['\"][^'\"]*\breference-entry\b[^'\"]*['\"][^>]*>(.*?)</p>",
    re.IGNORECASE | re.DOTALL,
)
ARTICLE_RE = re.compile(r"<article\b[^>]*>(.*?)</article>", re.IGNORECASE | re.DOTALL)
LITERAL_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
ANCHOR_RE = re.compile(r"<a\b[^>]*>.*?</a>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
PAREN_CITATION_RE = re.compile(
    r"\([A-Z][A-Za-zÀ-ÖØ-öø-ÿ&.,'’\- ]{1,100},\s*(?:" + YEAR + r")[^()]{0,80}\)"
)
NARRATIVE_CITATION_RE = re.compile(
    r"\b[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+)?(?:'s|’s)?\s*\((?:"
    + YEAR
    + r")\)"
)


def resolve_report(path: Path) -> Path:
    path = path.resolve()
    if (path / "report").is_dir():
        return path / "report"
    if path.is_dir() and any(path.glob("*.html")):
        return path
    raise SystemExit(f"Cannot locate generated report HTML under: {path}")


def visible_article_text(page: str) -> str:
    articles = ARTICLE_RE.findall(page)
    value = "\n".join(articles)
    value = LITERAL_RE.sub(" ", value)
    value = ANCHOR_RE.sub(" ", value)
    return html.unescape(TAG_RE.sub(" ", value))


def audit(report: Path) -> dict[str, object]:
    pages = sorted(report.rglob("*.html"))
    page_text = {page.resolve(): page.read_text(encoding="utf-8") for page in pages}
    broken: list[str] = []
    duplicates: list[str] = []
    reference_without_external: list[str] = []
    unlinked: list[str] = []
    citation_count = 0
    reference_entry_count = 0

    for page, text in page_text.items():
        relative = page.relative_to(report).as_posix()
        ids = ID_RE.findall(text)
        for target_id, count in Counter(ids).items():
            if target_id.startswith("ref-") and count > 1:
                duplicates.append(f"{relative}: duplicate id {target_id}")

        for href in CITATION_LINK_RE.findall(text):
            citation_count += 1
            target_name, separator, fragment = html.unescape(href).partition("#")
            target = (page.parent / target_name).resolve()
            if not separator or not fragment or target not in page_text:
                broken.append(f"{relative}: {href}")
                continue
            if not re.search(rf"\bid=['\"]{re.escape(fragment)}['\"]", page_text[target]):
                broken.append(f"{relative}: {href}")

        for entry in REFERENCE_ENTRY_RE.findall(text):
            reference_entry_count += 1
            if not re.search(r"\bhref=['\"]https?://", entry, re.IGNORECASE):
                reference_without_external.append(relative)

        if page.name.startswith("19-"):
            continue
        visible = visible_article_text(text)
        for match in PAREN_CITATION_RE.findall(visible):
            unlinked.append(f"{relative}: {match.strip()}")
        for match in NARRATIVE_CITATION_RE.findall(visible):
            unlinked.append(f"{relative}: {match.strip()}")

    return {
        "report": report.as_posix(),
        "pages": len(pages),
        "citation_links": citation_count,
        "reference_entries": reference_entry_count,
        "broken_links": sorted(set(broken)),
        "duplicate_ids": sorted(set(duplicates)),
        "reference_entries_without_external_links": sorted(set(reference_without_external)),
        "likely_unlinked_citations": sorted(set(unlinked)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Country folder or generated report folder")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()
    result = audit(resolve_report(Path(args.path)))
    issue_keys = (
        "broken_links",
        "duplicate_ids",
        "reference_entries_without_external_links",
        "likely_unlinked_citations",
    )
    print(
        f"pages={result['pages']} citation_links={result['citation_links']} "
        f"reference_entries={result['reference_entries']}"
    )
    for key in issue_keys:
        items = result[key]
        print(f"{key}={len(items)}")
        for item in items[:100]:
            print(f"- {item}")
    has_issues = any(result[key] for key in issue_keys)
    return 1 if args.fail_on_issues and has_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
