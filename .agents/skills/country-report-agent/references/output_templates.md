# Output Templates

Use this reference when the agent needs to return structured results for country-report diagnosis, evidence planning, rewriting, statistical work, citation audits, or quality gates.

These templates are for agent output, teaching feedback, and workflow control. Do not paste these tables into reader-facing manuscript prose unless the user explicitly asks for an appendix or methodology note.

## General Response Pattern

Use this order unless the user asks for another format:

1. Direct answer or status judgment
2. Highest-priority findings
3. Action table or audit table
4. Files changed or files inspected
5. Verification performed
6. Remaining risks or human checks

Keep tables compact. Do not bury the main judgment below long process notes.

## Claim-Evidence-Source Table

| Section | Claim | Current evidence | Source type needed | Gap | Priority |
|---|---|---|---|---|---|
| 07-01 | Revenue base is narrow | WDI tax revenue trend | National budget, IMF fiscal table | Need latest official budget value | High |

Use for source audits, section rewrites, and student practice.

## Source Gap Table

| Chapter/section | Missing source | Why it matters | Best source target | Next action |
|---|---|---|---|---|
| 05-02 | Civil service law | Explains appointment and accountability rules | Official legal portal or civil service agency | Locate law text and verify year |

Use when the report has claims but weak source backing.

## Country-Specific Issue Plan

| Issue | Why country-specific | Evidence base | Recommended placement | Section action | Priority |
|---|---|---|---|---|---|
| Water scarcity | Shapes agriculture, energy, and regional diplomacy | Official strategy, FAO, World Bank diagnostic | Chapter 11, linked to 15 and 17 | Add focused section | High |

Use when designing or auditing the table of contents. Keep the standard chapters intact and place special issues inside the most relevant chapter.

## ChatGPT Evidence Brief

| Field | Content |
|---|---|
| Country | ISO3 and country name |
| Target section | Section file and chapter role |
| Section question | What the section must answer |
| Central claim | Provisional thesis |
| Must preserve | Institutions, laws, reforms, regions, statistics, debates |
| Verified evidence | Source IDs, citations, values, and source notes |
| Source gaps | Claims that must remain cautious or unresolved |
| Statistics | Values, years, units, source institutions, indicator/table IDs |
| Country-specific issues | Special issue placement and links to other chapters |
| Style goal | Narrative pattern and tone |
| Do not claim | Unsupported, politically sensitive, or uncertain points |

Use before asking ChatGPT to draft richer prose. The brief should limit ChatGPT to verified evidence and clearly marked gaps.

## ChatGPT Draft Intake Audit

| Draft claim | Location | Evidence trail | Status | Action |
|---|---|---|---|---|
| Civil service reform changed appointment rules | paragraph 2 | Civil service law and government reform plan | partially verified | Keep cautious wording and add APA citation |

Use after receiving a ChatGPT draft. Treat the draft as manuscript input, not as evidence.

## Statistical Evidence Plan

| Section | Question | Indicator/table | Source | Unit | Years | Comparator | Output |
|---|---|---|---|---|---|---|---|
| 09-01 | Is growth volatile? | GDP growth | World Bank WDI | annual % | 2000-latest | region, income group | line chart and prose note |

Always connect the statistic to a section question.

## Statistical Result Summary

| Indicator | Latest value | Latest year | Trend | Interpretation | Limitation |
|---|---:|---:|---|---|---|
| Tax revenue | 14.2% of GDP | 2023 | Flat since 2018 | Fiscal space remains constrained | International estimate, not budget outturn |

Use after data processing and before inserting prose.

## Chart Plan

| Chart ID | Section | Purpose | Data source | Unit | Design | Source note |
|---|---|---|---|---|---|---|
| fig-07-01 | 07-01 | Show revenue constraint | IMF/WB | % of GDP | single line with peer median | Include indicator ID and latest year |

Reject a chart if its purpose cannot be stated in one sentence.

## APA Citation Audit Table

| Citation | Location | Final reference? | Source exists? | Register/local note? | Issue | Action |
|---|---|---|---|---|---|---|
| (World Bank, 2024) | 09-01 | Yes | Yes | Partial | Missing access date | Add access date to register |

Use for publication-readiness checks and reference cleanup.

## Numeric Claim Audit Table

| Location | Numeric claim | Value/year/unit present? | Citation present? | Issue | Action |
|---|---|---|---|---|---|
| 08-01 | population reached 12.4 million | value yes, year no, unit yes | no | Missing year and source | Add year and official statistics citation |

Use after running `scripts/audit_numeric_claims.py` or when manually reviewing prose.

## Section Rewrite Report

| Item | Result |
|---|---|
| Section | `05-02-civil-service.md` |
| Central claim | The civil service system is formally centralized but implementation capacity varies by region. |
| Preserved evidence | Civil service law, ministry names, reform program, regional implementation issue |
| Added evidence | APA citation to official civil service statute |
| Removed material | Generic template prose and unsupported transition |
| Remaining risk | Need latest public employment statistics |

Use when changing manuscript text.

## Narrative Style Review Table

| Location | Mechanical symptom | Why it weakens the book prose | Revision move |
|---|---|---|---|
| 07-02 | Three sentences list indicators without interpretation | The reader sees data points but not fiscal meaning | Combine into one claim about fiscal capacity and use numbers as support |

Use when a section feels template-like, audit-like, or overloaded with source names and statistics.

## Quality Gate Summary

| Dimension | Status | Evidence | Main fix |
|---|---|---|---|
| Country specificity | Deep draft | Institutions and laws named | Add subnational implementation detail |
| Country-specific issues | Structured first-pass | Some issues noted in prose | Add focused issue section and link to chapter 17 |
| ChatGPT-assisted prose | Deep draft | Draft verified against source trail | Remove unsupported enrichment |
| Official sources | Structured first-pass | Some official citations | Fill budget and civil service source gaps |
| Statistics | Deep draft | WDI and IMF values used | Add indicator IDs to chart notes |
| APA integrity | Structured first-pass | References chapter exists | Verify unmatched citations |

Final readiness labels:

- `structured first-pass`
- `deep draft`
- `publication candidate`

## Student Feedback Template

| Criterion | What worked | What to improve | Priority |
|---|---|---|---|
| Country specificity | Named the cabinet and civil service agency | Needs law title and year | High |
| Evidence mapping | Distinguished official and international data | Academic source missing | Medium |
| Prompt quality | Clear goal and constraints | Done condition too vague | Medium |

Use for teaching and practice review.

## Final Delivery Checklist

When completing an agent task, report:

- changed files, if any
- scripts or audits run
- unresolved evidence gaps
- citations or references that still need human verification
- whether generated HTML or charts were rebuilt
