# High-risk chapters canonical integration plan

This plan is preparatory only. No canonical files were changed in the human-review batch.

| Chapter | Candidate source | Canonical targets | Preserve | Visuals | Required checks |
|---|---|---|---|---|---|
| 3 | `sources/drafts/chapter03_constitution_review_candidate.md` | `sources/sections/03-*.md` | Verified legal distinctions and emergency qualifications | Existing Ch.3 visuals only after legal caption review | Choose one candidate; reconcile legal citations and terminology |
| 5 | `sources/drafts/chapter05_administrative_system_review_candidate.md` | `sources/sections/05-*.md` | GAD history, formal hierarchy, civil-service distinction | Existing verified Ch.5 visuals if any | Remove workflow language; retain locality/date qualifications |
| 7 | `sources/drafts/chapter07_fiscal_system_review_candidate.md` | `sources/sections/07-*.md` | Fiscal architecture and reproducibility caveats | Ch.7 charts and formal fiscal architecture | Validate chart map; exclude `exp`; preserve raw-path caveat |
| 15 | `sources/drafts/chapter15_foreign_relations_security_review_candidate.md` | `sources/sections/15-*.md` | Recognition/representation distinction and no-control-map rule | Ch.15 schematic/timeline/humanitarian chart | Check humanitarian definitions, event dates and actor labels |
| 16 | `sources/drafts/chapter16_major_policies_strategy_review_candidate.md` | `sources/sections/16-*.md` | MSDP/MERP/FDC status distinctions | Ch.16 timeline, chain and matrix | Remove editorial wording; retain MERP/FDC limitations |
| 17 | `sources/drafts/chapter17_integrated_assessment_review_candidate.md` | `sources/sections/17-*.md` | Cross-chapter mechanisms and evidence limits | Ch.17 three synthesis visuals | Run contradiction and source-ID checks after Chapters 3/5/7/15/16 |

## Recommended sequence

1. Human reviewer approves one Chapter 3 candidate and confirms terminology.
2. Apply coordinated prose/citation revisions to all six candidates.
3. Integrate all six chapters in one controlled Markdown batch.
4. Insert only visuals marked KEEP after final caption and source review.
5. Update APA/reference anchors and source links.
6. Rebuild HTML once after all six canonical chapters are integrated.
7. Run citation, link, numeric, statistical, visual, narrative, section-depth and integrated audits.

Unresolved notes and raw provenance must remain in the source documentation and must not be silently converted into reader-facing facts.
