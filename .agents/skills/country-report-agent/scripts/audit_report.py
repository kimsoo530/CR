#!/usr/bin/env python3
"""Run all country-report audits and produce one severity-aware readiness summary."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

AUDITS = ("citations", "numeric_claims", "section_depth", "statistical_coverage", "visual_evidence", "narrative_structure")


def run_audit(script_dir: Path, name: str, country: Path) -> dict:
    process = subprocess.run([sys.executable, str(script_dir / f"audit_{name}.py"), str(country), "--json"], capture_output=True, text=True, encoding="utf-8")
    if not process.stdout.strip():
        return {"audit_error": process.stderr.strip() or f"exit {process.returncode}"}
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError:
        return {"audit_error": process.stdout.strip()[:500]}


def summarize(results: dict) -> dict:
    blockers, warnings, errors = [], [], []
    for name, result in results.items():
        if "audit_error" in result:
            errors.append({"audit": name, "message": result["audit_error"]})
            continue
        if name == "citations" and result.get("missing_reference_count"):
            blockers.append({"audit": name, "count": result["missing_reference_count"], "reason": "unmatched_in_text_citations"})
        elif name == "section_depth" and result.get("deep_draft_blocked_by_depth"):
            blockers.append({"audit": name, "count": result.get("under_500_count", 1), "reason": "insufficient_section_depth"})
        elif name == "statistical_coverage" and result.get("deep_draft_blocked_by_statistics"):
            blockers.append({"audit": name, "count": result.get("blocker_count", 1), "reason": "unverified_statistical_coverage"})
        elif name == "narrative_structure" and result.get("deep_draft_blocked"):
            blockers.append({"audit": name, "count": result.get("blocker_count", 1), "reason": "template_or_repeated_prose"})
        if name == "numeric_claims" and result.get("issue_count"):
            warnings.append({"audit": name, "count": result["issue_count"], "reason": "numeric_claims_need_editorial_review"})
        if name == "visual_evidence" and result.get("publication_candidate_blocked"):
            warnings.append({"audit": name, "count": 1, "reason": "publication_visual_guardrail"})
        if name == "citations" and (result.get("uncited_reference_count") or result.get("weak_reference_locator_count")):
            warnings.append({"audit": name, "count": result.get("uncited_reference_count", 0) + result.get("weak_reference_locator_count", 0), "reason": "bibliography_cleanup"})
        if name == "statistical_coverage" and result.get("mode") == "legacy_keywords":
            warnings.append({"audit": name, "count": 1, "reason": "legacy_keyword_mode_cannot_support_publication_candidate"})
        if name == "narrative_structure" and result.get("warning_count"):
            warnings.append({"audit": name, "count": result["warning_count"], "reason": "manual_narrative_review"})
    if errors or blockers:
        readiness = "structured first-pass"
    elif warnings:
        readiness = "deep draft"
    else:
        readiness = "publication candidate (automated checks only; manual chapter review required)"
    return {"readiness": readiness, "blocker_count": sum(x["count"] for x in blockers),
            "warning_count": sum(x["count"] for x in warnings), "audit_error_count": len(errors),
            "blockers": blockers, "warnings": warnings, "errors": errors,
            "manual_editorial_review_required": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_path", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()
    scripts = Path(__file__).resolve().parent
    results = {name: run_audit(scripts, name, args.country_path.resolve()) for name in AUDITS}
    summary = summarize(results)
    output = {"country_path": args.country_path.resolve().as_posix(), "summary": summary, "audits": results}
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print("# Integrated Country Report Audit\n")
        print(f"- Readiness: **{summary['readiness']}**")
        print(f"- Blockers: {summary['blocker_count']}")
        print(f"- Warnings: {summary['warning_count']}")
        print(f"- Audit errors: {summary['audit_error_count']}")
        print("- Automated output is triage; chapter-level editorial review remains mandatory.")
    return 1 if args.fail_on_blockers and (summary["blocker_count"] or summary["audit_error_count"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
