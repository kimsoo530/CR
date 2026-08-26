#!/usr/bin/env python3
"""Flag outline-length country-report sections without treating length as quality."""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path


EXCLUDED_TERMS = {"reference", "bibliograph", "integrity", "appendix", "update-workflow"}
HIGH_RISK_CHAPTERS = {3, 5, 7, 16, 17}


def section_dir(path: Path) -> Path:
    if path.name == "sections" and path.is_dir():
        return path
    if (path / "sources" / "sections").is_dir():
        return path / "sources" / "sections"
    if (path / "sections").is_dir():
        return path / "sections"
    raise SystemExit(f"Cannot find sources/sections under {path}")


def content_files(path: Path) -> list[Path]:
    files = []
    for file in sorted(section_dir(path).glob("*.md")):
        stem = file.stem.lower()
        if not re.match(r"^\d{2}[-_]\d{2}", stem):
            continue
        if any(term in stem for term in EXCLUDED_TERMS):
            continue
        files.append(file)
    return files


def word_count(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^]]*]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", text)
    text = re.sub(r"(?m)^#{1,6}\s+", "", text)
    return len(re.findall(r"[^\W_]+(?:[-'’][^\W_]+)*", text, flags=re.UNICODE))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    rows = []
    for file in content_files(Path(args.country_path).resolve()):
        count = word_count(file.read_text(encoding="utf-8"))
        chapter = int(file.stem[:2])
        band = "critical-short" if count < 200 else "first-pass" if count < 500 else "developed" if count < 800 else "extended"
        rows.append({"file": file.name, "chapter": chapter, "words": count, "band": band, "high_risk": chapter in HIGH_RISK_CHAPTERS})

    counts = [row["words"] for row in rows]
    critical = [row for row in rows if row["words"] < 200]
    below_working = [row for row in rows if row["words"] < 500]
    high_risk_below = [row for row in rows if row["high_risk"] and row["words"] < 800]
    median = statistics.median(counts) if counts else 0
    blocked = bool(rows) and (len(critical) / len(rows) > 0.10 or median < 500)
    result = {
        "section_count": len(rows),
        "median_words": median,
        "average_words": round(statistics.mean(counts), 1) if counts else 0,
        "critical_short_count": len(critical),
        "under_500_count": len(below_working),
        "high_risk_under_800_count": len(high_risk_below),
        "deep_draft_blocked_by_depth": blocked,
        "note": "Length is a diagnostic signal; manually review substance and documented exceptions.",
        "sections": rows,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.summary:
        print(
            f"sections={len(rows)} median_words={median} critical_short={len(critical)} "
            f"under_500={len(below_working)} deep_draft_blocked={str(blocked).lower()}"
        )
    else:
        print("# Section Depth Audit\n")
        print(f"- Sections: {len(rows)}")
        print(f"- Median words: {median}")
        print(f"- Critical-short sections: {len(critical)}")
        print(f"- Under 500 words: {len(below_working)}")
        print(f"- Deep-draft depth guardrail blocked: {blocked}\n")
        print("| File | Words | Band | High-risk chapter |")
        print("|---|---:|---|---|")
        for row in rows:
            print(f"| {row['file']} | {row['words']} | {row['band']} | {row['high_risk']} |")
        print("\nWord count does not prove quality; review each flag for missing argument, mechanism, evidence, and interpretation.")

    return 1 if args.fail_on_issues and (critical or blocked) else 0


if __name__ == "__main__":
    raise SystemExit(main())
