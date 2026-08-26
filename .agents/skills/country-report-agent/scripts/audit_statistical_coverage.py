#!/usr/bin/env python3
"""Audit statistical coverage against evidence, indicator, chart, and source registers."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

DEFAULT_DATA_CHAPTERS = {7, 8, 9, 10, 11, 12, 13, 14, 16}
EXCLUDED_TERMS = {"reference", "bibliograph", "integrity", "appendix", "update-workflow"}
LEGACY_EXCEPTION = re.compile(r"<!--\s*statistics-not-applicable:\s*(.+?)-->", re.I | re.S)
LEVEL = re.compile(r"\b\d+(?:[.,]\d+)*(?:\s*(?:%|percent|million|billion|trillion|per\s+capita|index|rate|ratio))", re.I)
TREND = re.compile(r"\b(trend|increase|decrease|grew|growth|decline|rose|fell|change|turning point|volatil|since|over time)\b", re.I)
COMPARISON = re.compile(r"\b(compare|comparison|peer|region|income group|higher than|lower than|relative to|benchmark)\b", re.I)
DISTRIBUTION = re.compile(r"\b(state|province|region|urban|rural|gender|income|racial|ethnic|sector|subnational|distribution|inequal|gap|variation)\b", re.I)


def country_root(path: Path) -> Path:
    if (path / "sources" / "sections").is_dir(): return path
    if path.name == "sections" and path.parent.name == "sources": return path.parent.parent
    if (path / "sections").is_dir(): return path.parent
    raise SystemExit(f"Cannot find country root from {path}")


def csv_rows(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def section_files(root: Path) -> list[Path]:
    result = []
    for file in sorted((root / "sources" / "sections").glob("*.md")):
        if not re.match(r"^\d{2}[-_]\d{2}", file.stem) or any(t in file.stem.lower() for t in EXCLUDED_TERMS): continue
        if int(file.stem[:2]) in DEFAULT_DATA_CHAPTERS: result.append(file)
    return result


def dimensions(text: str) -> list[str]:
    tests = (("level", LEVEL), ("trend", TREND), ("comparison", COMPARISON), ("distribution", DISTRIBUTION))
    return [name for name, pattern in tests if pattern.search(text)]


def audit(path: Path) -> dict:
    root = country_root(path)
    plans = csv_rows(root / "sources" / "section_evidence_plan.csv")
    charts = csv_rows(root / "sources" / "chart_map.csv")
    metadata = csv_rows(root / "processed" / "statistical_metadata.csv")
    sources = csv_rows(root / "sources" / "source_register.csv")
    mode = "registered_evidence" if plans and (charts or metadata) else "legacy_keywords"
    by_section: dict[str, list[dict]] = {}
    for row in plans: by_section.setdefault((row.get("section_id") or "").strip(), []).append(row)
    chart_ids = {(r.get("chart_id") or "").strip(): r for r in charts if r.get("chart_id")}
    indicator_ids = {(r.get("indicator_id") or "").strip() for r in metadata if r.get("indicator_id")}
    source_ids = {(r.get("source_id") or "").strip() for r in sources if r.get("source_id")}
    rows = []
    for file in section_files(root):
        section_id = file.stem[:5].replace("_", "-")
        text = file.read_text(encoding="utf-8-sig")
        dims = dimensions(text)
        plan_rows = by_section.get(section_id, [])
        registered_charts = {v.strip() for row in plan_rows for v in (row.get("chart_id") or "").split(";") if v.strip()}
        registered_indicators = {v.strip() for row in plan_rows for v in (row.get("indicator_id") or "").split(";") if v.strip()}
        registered_sources = {v.strip() for row in plan_rows for v in (row.get("source_id") or "").split(";") if v.strip()}
        missing_chart_records = sorted(registered_charts - set(chart_ids))
        missing_indicator_records = sorted(registered_indicators - indicator_ids)
        missing_source_records = sorted(registered_sources - source_ids)
        missing_chart_files = []
        for chart_id in registered_charts & set(chart_ids):
            rel = (chart_ids[chart_id].get("file") or "").strip()
            if rel and not (root / rel).exists(): missing_chart_files.append(rel)
        exception_reason = ""
        for row in plan_rows:
            if (row.get("statistics_status") or "").strip().lower() == "not_applicable":
                exception_reason = (row.get("statistics_exception_reason") or row.get("next_action") or "").strip()
                break
        legacy_exception = LEGACY_EXCEPTION.search(text)
        has_table = bool(re.search(r"(?m)^\s*\|.+\|\s*$", text) and re.search(r"(?m)^\s*\|?\s*:?-{3,}", text))
        has_figure = "![" in text
        issues, warnings = [], []
        if missing_chart_records: issues.append("unregistered_chart_id")
        if missing_indicator_records: issues.append("unregistered_indicator_id")
        if missing_source_records: issues.append("unregistered_source_id")
        if missing_chart_files: issues.append("missing_chart_file")
        if legacy_exception and not exception_reason: warnings.append("comment_only_exception_not_accepted")
        evidence_linked = bool((registered_charts and not missing_chart_records and not missing_chart_files) or
                               (registered_indicators and not missing_indicator_records))
        if not exception_reason:
            if mode == "registered_evidence" and not evidence_linked: issues.append("no_registered_statistical_evidence")
            if not evidence_linked and not has_table and not has_figure and len(set(dims)) < 2: issues.append("insufficient_analytical_dimensions")
        rows.append({"file": file.name, "section_id": section_id, "chapter": int(file.stem[:2]), "dimensions": dims,
                     "mode": mode, "registered_chart_ids": sorted(registered_charts), "registered_indicator_ids": sorted(registered_indicators),
                     "exception_reason": exception_reason, "issues": sorted(set(issues)), "warnings": sorted(set(warnings))})
    blocker_count = sum(len(row["issues"]) for row in rows)
    warning_count = sum(len(row["warnings"]) for row in rows) + (1 if mode == "legacy_keywords" else 0)
    return {"mode": mode, "data_intensive_section_count": len(rows), "issue_count": blocker_count,
            "blocker_count": blocker_count, "warning_count": warning_count,
            "deep_draft_blocked_by_statistics": bool(blocker_count),
            "publication_candidate_blocked": bool(blocker_count or mode == "legacy_keywords"),
            "editorial_review_required": bool(blocker_count or warning_count), "sections": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()
    result = audit(Path(args.country_path).resolve())
    if args.json: print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.summary: print(f"mode={result['mode']} data_sections={result['data_intensive_section_count']} blockers={result['blocker_count']} warnings={result['warning_count']} deep_draft_blocked={str(result['deep_draft_blocked_by_statistics']).lower()}")
    else:
        print("# Statistical Coverage Audit\n")
        print(f"- Mode: `{result['mode']}`\n- Blockers: {result['blocker_count']}\n- Warnings: {result['warning_count']}")
        for row in result["sections"]:
            if row["issues"] or row["warnings"]: print(f"- `{row['file']}`: {', '.join(row['issues'] + row['warnings'])}")
    return 1 if args.fail_on_issues and result["blocker_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
