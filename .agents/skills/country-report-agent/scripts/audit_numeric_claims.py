#!/usr/bin/env python3
"""Audit substantive numeric claims while ignoring citation and document-number noise."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

NUMBER_RE = re.compile(r"(?<![\w-])(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?![\w-])")
YEAR_RE = re.compile(r"\b(?:18|19|20)\d{2}\b")
CITATION_RE = re.compile(r"\([^()\n]{1,160}(?:(?:18|19|20)\d{2}[a-z]?|n\.d\.)[^()\n]{0,80}\)", re.I)
UNIT_RE = re.compile(r"(%|percent|percentage|points?|p\.p\.|billion|million|thousand|trillion|USD|US\$|\$|LCU|GDP|capita|people|persons|households|states?|countries|jurisdictions|km|sq\.?\s*km|index|score|ratio|rate|years?|months?|days?|tons?|tonnes?|MW|GW|kWh|명|가구|퍼센트|조|억|만|달러|년)", re.I)
SKIP_FILE_RE = re.compile(r"(reference|bibliography|citation|source|appendix)", re.I)


@dataclass(frozen=True)
class NumericIssue:
    file: str
    line: int
    passage: str
    numbers: str
    claim_type: str
    missing_year: bool
    missing_unit: bool
    missing_citation: bool
    severity: str


def resolve_sections_dir(path: Path) -> Path:
    for candidate in (path / "sources" / "sections", path if path.name == "sections" else None, path / "sections"):
        if candidate and candidate.exists():
            return candidate
    raise SystemExit(f"Cannot locate sources/sections under: {path}")


def paragraphs_with_lines(text: str):
    buffer, start = [], 1
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            if buffer:
                yield start, " ".join(buffer)
                buffer = []
            continue
        if stripped.startswith(("#", "|", "![", "<!--")):
            if buffer:
                yield start, " ".join(buffer)
                buffer = []
            continue
        if not buffer:
            start = number
        buffer.append(stripped)
    if buffer:
        yield start, " ".join(buffer)


def substantive_numbers(passage: str) -> tuple[list[str], list[str]]:
    citations = CITATION_RE.findall(passage)
    without_citations = CITATION_RE.sub(" ", passage)
    numbers = NUMBER_RE.findall(without_citations)
    return numbers, citations


def only_historical_years(passage: str, numbers: list[str]) -> bool:
    return bool(numbers) and all(re.fullmatch(r"(?:17|18|19|20)\d{2}", n) for n in numbers)


def extract_issues(sections_dir: Path) -> list[NumericIssue]:
    issues = []
    for path in sorted(sections_dir.glob("*.md")):
        if SKIP_FILE_RE.search(path.name):
            continue
        text = path.read_text(encoding="utf-8-sig")
        for line_no, passage in paragraphs_with_lines(text):
            numbers, citations = substantive_numbers(passage)
            if not numbers:
                continue
            historical = only_historical_years(passage, numbers)
            claim_type = "historical_date" if historical else "quantitative_claim"
            missing_citation = not bool(citations)
            missing_year = False if historical else not bool(YEAR_RE.search(CITATION_RE.sub(" ", passage)))
            missing_unit = False if historical else not bool(UNIT_RE.search(passage))
            if historical and not missing_citation:
                continue
            if missing_year or missing_unit or missing_citation:
                severity = "warning" if historical or sum((missing_year, missing_unit, missing_citation)) == 1 else "editorial_review"
                issues.append(NumericIssue(path.as_posix(), line_no, passage, ", ".join(numbers), claim_type, missing_year, missing_unit, missing_citation, severity))
    return issues


def audit(country_path: Path) -> dict:
    folder = resolve_sections_dir(country_path)
    issues = extract_issues(folder)
    return {"sections_dir": folder.as_posix(), "issue_count": len(issues), "blocker_count": 0,
            "warning_count": len(issues), "editorial_review_required": bool(issues),
            "issues": [asdict(issue) for issue in issues]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()
    result = audit(Path(args.country_path).resolve())
    if args.summary:
        print(f"flagged_passages={result['issue_count']} editorial_review_required={str(result['editorial_review_required']).lower()}")
    elif args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Numeric Claim Audit\n")
        print(f"- Flagged passages: {result['issue_count']}")
        for issue in result["issues"][:200]:
            print(f"- `{issue['file']}:{issue['line']}` [{issue['claim_type']}] {issue['passage'][:220]}")
    return 1 if args.fail_on_issues and result["issue_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
