#!/usr/bin/env python3
"""Regression checks for high-risk audit false positives and false negatives."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load(name: str):
    path = ROOT / "scripts" / f"audit_{name}.py"
    spec = importlib.util.spec_from_file_location(f"audit_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    citations = load("citations")
    numeric = load("numeric_claims")
    narrative = load("narrative_structure")

    citation_result = citations.audit(FIXTURES / "good")
    assert citation_result["missing_reference_count"] == 0, citation_result["missing_references"]
    assert citation_result["uncited_reference_count"] == 0, citation_result["uncited_references"]

    numeric_result = numeric.audit(FIXTURES / "good")
    assert numeric_result["issue_count"] == 0, numeric_result["issues"]

    good_narrative = narrative.audit(FIXTURES / "good")
    assert not good_narrative["deep_draft_blocked"], good_narrative
    bad_narrative = narrative.audit(FIXTURES / "bad")
    assert bad_narrative["repeated_frame_count"] > 0, bad_narrative
    assert bad_narrative["deep_draft_blocked"], bad_narrative

    print("audit regression fixtures: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
