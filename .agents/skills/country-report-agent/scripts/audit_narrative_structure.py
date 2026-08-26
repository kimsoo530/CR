#!/usr/bin/env python3
"""Detect checklist headings, repeated prose frames, and near-duplicate paragraphs."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


BANNED_HEADINGS = {
    "analytical claim", "statistical evidence", "statistical and institutional evidence",
    "mechanisms", "comparative interpretation and limits",
    "what the evidence can and cannot establish", "policy and administrative implications",
    "decision criteria and failure conditions", "분석적 주장", "통계적 근거", "통계 및 제도적 근거",
    "작동 메커니즘", "비교적 해석과 한계", "증거가 밝힐 수 있는 것과 없는 것", "정책 및 행정적 함의",
}
TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


def sections_dir(root: Path) -> Path:
    for candidate in (root / "sources" / "sections", root / "sections", root):
        if candidate.exists() and any(candidate.glob("*.md")):
            return candidate
    raise FileNotFoundError(f"No Markdown sections found under {root}")


def clean_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"!\[[^]]*]\([^)]*\)", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\([^)]*(?:19|20)\d{2}[a-z]?[^)]*\)", " ", text, flags=re.I)
    return text


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", clean_markdown(text)).casefold()
    return " ".join(TOKEN_RE.findall(text))


def paragraphs(text: str):
    for block in re.split(r"\n\s*\n", clean_markdown(text)):
        block = block.strip()
        if not block or block.startswith(("#", "|", "![")):
            continue
        key = normalize(block)
        if len(key.split()) >= 25:
            yield block, key


def shingles(key: str, width: int = 5) -> set[tuple[str, ...]]:
    words = key.split()
    return {tuple(words[i:i + width]) for i in range(max(0, len(words) - width + 1))}


def audit(root: Path) -> dict:
    folder = sections_dir(root)
    files = [p for p in sorted(folder.glob("*.md")) if not p.name.startswith("19-")]
    banned, paragraph_rows = [], []
    headings: dict[str, set[str]] = defaultdict(set)
    exact: dict[str, set[str]] = defaultdict(set)
    frame_files: dict[tuple[str, ...], set[str]] = defaultdict(set)

    for path in files:
        text = path.read_text(encoding="utf-8-sig")
        for line_number, line in enumerate(text.splitlines(), 1):
            if re.match(r"^#{2,4}\s+", line):
                raw = re.sub(r"^#{2,4}\s+", "", line).strip()
                heading = normalize(raw)
                headings[heading].add(path.name)
                if heading in BANNED_HEADINGS:
                    banned.append({"file": path.name, "line": line_number, "heading": raw})
        for raw, key in paragraphs(text):
            row = {"file": path.name, "excerpt": raw[:220], "key": key, "shingles": shingles(key)}
            paragraph_rows.append(row)
            exact[key].add(path.name)
            words = key.split()
            for width in (10,):
                for i in range(len(words) - width + 1):
                    frame_files[tuple(words[i:i + width])].add(path.name)

    threshold = max(4, max(1, len(files) // 5))
    repeated_headings = [
        {"heading": h, "section_count": len(fs), "files": sorted(fs)}
        for h, fs in headings.items() if h and len(fs) >= threshold
    ]
    repeated_paragraphs = [
        {"section_count": len(fs), "files": sorted(fs), "excerpt": key[:220]}
        for key, fs in exact.items() if len(fs) >= 3
    ]
    frame_candidates = [(phrase, fs) for phrase, fs in frame_files.items() if len(fs) >= 3]
    frame_candidates.sort(key=lambda item: (-len(item[1]), " ".join(item[0])))
    repeated_frames, covered = [], set()
    for phrase, fs in frame_candidates:
        # Adjacent n-grams from the same boilerplate produce the same file set;
        # report that family once instead of inflating the blocker count.
        signature = frozenset(fs)
        if signature in covered:
            continue
        covered.add(signature)
        repeated_frames.append({"phrase": " ".join(phrase), "section_count": len(fs), "files": sorted(fs)})
        if len(repeated_frames) >= 100:
            break

    near_duplicates = []
    for i, left in enumerate(paragraph_rows):
        for right in paragraph_rows[i + 1:]:
            if left["file"] == right["file"]:
                continue
            union = left["shingles"] | right["shingles"]
            if not union:
                continue
            score = len(left["shingles"] & right["shingles"]) / len(union)
            if score >= 0.60 and left["key"] != right["key"]:
                near_duplicates.append({"files": [left["file"], right["file"]], "similarity": round(score, 3), "excerpt": left["excerpt"]})
                if len(near_duplicates) >= 100:
                    break
        if len(near_duplicates) >= 100:
            break

    blockers = len(banned) + len(repeated_paragraphs) + len(repeated_frames)
    warnings = len(repeated_headings) + len(near_duplicates)
    return {
        "sections": len(files), "banned_heading_count": len(banned), "banned_headings": banned,
        "repeated_heading_count": len(repeated_headings), "repeated_headings": repeated_headings,
        "repeated_paragraph_count": len(repeated_paragraphs), "repeated_paragraphs": repeated_paragraphs,
        "repeated_frame_count": len(repeated_frames), "repeated_frames": repeated_frames,
        "near_duplicate_count": len(near_duplicates), "near_duplicates": near_duplicates,
        "blocker_count": blockers, "warning_count": warnings, "editorial_review_required": bool(blockers or warnings),
        "deep_draft_blocked": bool(blockers),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_path", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()
    result = audit(args.country_path.resolve())
    if args.summary:
        keys = ["sections", "banned_heading_count", "repeated_heading_count", "repeated_paragraph_count", "repeated_frame_count", "near_duplicate_count", "deep_draft_blocked"]
        print(" ".join(f"{k}={str(result[k]).lower() if isinstance(result[k], bool) else result[k]}" for k in keys))
    elif args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Narrative Structure Audit\n")
        for label, key in (("Sections", "sections"), ("Banned checklist headings", "banned_heading_count"),
                           ("Widely repeated headings", "repeated_heading_count"), ("Repeated paragraphs", "repeated_paragraph_count"),
                           ("Repeated sentence frames", "repeated_frame_count"), ("Near-duplicate paragraphs", "near_duplicate_count")):
            print(f"- {label}: {result[key]}")
    return 1 if args.fail_on_issues and result["deep_draft_blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
