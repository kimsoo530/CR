#!/usr/bin/env python3
"""Audit tables, embedded figures, and figure assets in a country report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FIGURE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def country_root(path: Path) -> Path:
    if (path / "sources" / "sections").is_dir():
        return path
    if path.name == "sections" and path.parent.name == "sources":
        return path.parent.parent
    raise SystemExit(f"Cannot find country root from {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    root = country_root(Path(args.country_path).resolve())
    sections = sorted((root / "sources" / "sections").glob("*.md"))
    embedded = []
    table_sections = []
    for file in sections:
        text = file.read_text(encoding="utf-8")
        if "![" in text:
            embedded.append(file.name)
        if re.search(r"(?m)^\s*\|.+\|\s*$", text) and re.search(r"(?m)^\s*\|?\s*:?-{3,}", text):
            table_sections.append(file.name)

    figure_dir = root / "figures"
    assets = sorted(file for file in figure_dir.rglob("*") if file.is_file() and file.suffix.lower() in FIGURE_EXTENSIONS) if figure_dir.exists() else []
    zero_visual = not embedded and not table_sections and not assets
    result = {
        "section_count": len(sections),
        "embedded_figure_section_count": len(embedded),
        "table_section_count": len(table_sections),
        "figure_asset_count": len(assets),
        "zero_visual_evidence": zero_visual,
        "publication_candidate_blocked": zero_visual,
        "note": "Visual sufficiency requires editorial review; every visual must answer a section question.",
        "embedded_figure_sections": embedded,
        "table_sections": table_sections,
        "figure_assets": [str(file.relative_to(root)) for file in assets],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.summary:
        print(
            f"sections={len(sections)} embedded_figure_sections={len(embedded)} table_sections={len(table_sections)} "
            f"figure_assets={len(assets)} publication_candidate_blocked={str(zero_visual).lower()}"
        )
    else:
        print("# Visual Evidence Audit\n")
        print(f"- Embedded-figure sections: {len(embedded)}")
        print(f"- Table sections: {len(table_sections)}")
        print(f"- Figure assets: {len(assets)}")
        print(f"- Publication-candidate guardrail blocked: {zero_visual}")
        print("\nZero visuals require a documented chapter-by-chapter justification; nonzero visuals still require substantive review.")

    return 1 if args.fail_on_issues and zero_visual else 0


if __name__ == "__main__":
    raise SystemExit(main())
