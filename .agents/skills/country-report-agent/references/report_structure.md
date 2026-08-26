# Report Structure Reference

Use this reference when checking or explaining the country-report package structure. For country-specific issue sections inside the standard chapter structure, also read `country_specific_issue_protocol.md`.

## Expected Country Folder

```text
[ISO3]/
  raw/
  processed/
  code/
  figures/
  report/
    index.html
    01-overview.html
    ...
    19-references.html
    sections/
  sources/
    sections/
    documents/
    source_register.csv
    section_evidence_plan.csv
```

## Canonical Relationships

- `sources/sections/*.md` is the editable manuscript.
- `report/sections/*.html` is the reader-facing section output.
- `report/*.html` is generated chapter and cover output.
- `code/build_report.py` rebuilds report artifacts when present.
- `code/serve_report.py` may provide persistent browser editing when present.
- `sources/section_evidence_plan.csv` maps sections to indicators, sources, charts, and update instructions.

## Standard Chapters

1. Country Overview
2. Historical Background
3. Constitution and Basic State Order
4. Political System and Power Structure
5. Administrative System and Government Organization
6. Governance and Institutional Capacity
7. Fiscal System and Public Sector
8. Population and Social Structure
9. Macroeconomic Structure
10. Trade, Investment, and External Economy
11. Infrastructure, Energy, and Digital Connectivity
12. Labor Market and Human Capital
13. Education, Health, and Welfare
14. Financial Sector and Economic Institutions
15. Foreign Relations, Security, and Geopolitics
16. Major Policies and National Development Strategy
17. Integrated Assessment
18. Appendix and Update Workflow
19. References

## Standard Plus Country-Specific Sections

The standard chapters should normally remain present across countries for comparability. Country-specific issue sections may be added or preserved inside the relevant standard chapter when they are necessary to explain the country's institutions, state capacity, political economy, development path, territorial condition, social structure, or external position.

Examples:

- a de facto authority issue belongs primarily in chapter 3 or 15, with synthesis in chapter 17
- a civil service reform or decentralization issue belongs primarily in chapter 5
- a fiscal dependence, debt, resource revenue, or SOE risk issue belongs primarily in chapter 7
- a water, energy, logistics, or climate infrastructure issue belongs primarily in chapter 11
- a national development strategy or reform sequencing issue belongs primarily in chapter 16

Avoid creating many new top-level chapters. Prefer focused sections within the standard chapters, and connect cross-cutting issues back to chapter 17.

## Structure Diagnosis Checklist

- Does the country folder contain raw, processed, code, report, and sources folders?
- Are section Markdown files present and section-numbered?
- Does the report include cover, chapter pages, references, and section pages?
- Does the report preserve the standard chapter structure while adding country-specific issue sections where needed?
- Are country-specific issue sections placed in the chapter with the strongest institutional or policy mechanism?
- Is there a source register or equivalent source notes?
- Is there a section evidence plan?
- Is there a build script?
- Are quality-audit outputs present?
- Are source documents archived or at least documented?
