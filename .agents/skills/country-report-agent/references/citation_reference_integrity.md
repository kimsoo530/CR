# Citation And Reference Integrity

Use this reference when adding, editing, auditing, or verifying citations and final References for a country report. For APA register fields, read `reference_schemas.md`. For citation audit reporting, read `output_templates.md`.

## Core Standard

Use APA-style author-date in-text citations in the manuscript and maintain a final References chapter that contains the full bibliography for every cited source. Every in-text citation must connect to one real, verifiable reference entry, and every final reference entry should normally correspond to a source cited in the report.

## Where References Live

- In-text citations appear inside `sources/sections/*.md`.
- Final bibliography entries normally appear in `sources/sections/19-01-references.md`.
- Citation and source-integrity notes may appear in `sources/sections/19-02-citation-and-source-integrity-notes.md`.
- Machine-readable reference registers may appear at `sources/apa_reference_register.json`.
- Source metadata may also appear in `sources/source_register.csv`, `sources/section_evidence_plan.csv`, or source notes under `sources/documents/`.

## APA In-Text Citation Rules

Use concise APA author-date citations:

- Institutional author: `(World Bank, 2024)`
- Long institutional author on first use if needed: `(International Monetary Fund, 2023)`
- Scholarly source: `(Kim, 2021)` or `(Kim & Park, 2022)`
- Three or more authors: `(Kim et al., 2020)`
- Multiple sources: `(International Monetary Fund, 2023; World Bank, 2024)`
- Direct quotation or precise table reference when needed: `(World Bank, 2024, Table 2.1)`

Use citations for:

- factual claims drawn from official or diagnostic documents
- statistics and data interpretation
- scholarly arguments
- institutional or legal descriptions not directly obvious from the report's own data
- contested political, administrative, or historical interpretations

Avoid citation clutter for every sentence. Cite at the paragraph level when several sentences rely on the same source, but do not leave major claims uncited.

## Final References Requirements

Each final reference entry should contain, as applicable:

- author or institutional author
- year or n.d. if genuinely undated
- title
- publication series, report number, journal, publisher, or issuing institution
- DOI, URL, official landing page, or access note
- dataset/table/indicator name when the source is data
- access or download date when the source is dynamic, database-driven, or not stably dated

Use final References for full source identity. Use source registers and evidence plans for workflow metadata, local paths, and update instructions.

## Source Existence Verification

Before treating a reference as usable, verify at least one of the following:

- DOI resolves or is listed by the publisher, Crossref, journal, or academic database
- URL opens to the official publication, dataset, institutional page, or stable landing page
- official institutional website confirms the title, year, and authoring body
- local archived file exists under `sources/documents/` with matching title or source note
- source register entry records a URL, local path, title, institution, and access/download date
- for books, a reputable publisher, library catalog, DOI, ISBN, Google Books, WorldCat, or university-press page confirms existence

If none of these can be confirmed, do not cite the item as evidence. Mark it as `needs verification` or remove it from reader-facing citations until verified.

## Matching Audit

When auditing a report, check four links:

1. In-text citation -> final reference entry
2. Final reference entry -> real source existence
3. Final reference entry -> source register or local source note when available
4. Statistical citation -> indicator/table ID, raw or processed file, and chart/source note when applicable
5. Rendered in-text citation link -> existing final-reference anchor
6. Final-reference DOI/URL link -> intended external source

Flag:

- cited source missing from final References
- final reference never cited in the report
- mismatched year between in-text citation and reference entry
- mismatched institutional author name
- invented-looking article, book, or report metadata
- reference without DOI, URL, local source file, or access note
- URL that leads to an unrelated page
- statistics cited to a report when the underlying dataset should be identified
- rendered citation link with a missing file, missing fragment, wrong relative path, or duplicate target ID
- plain-text DOI/URL that should be clickable in the reader-facing References page
- a rebuild that repairs links but silently removes prose, tables, charts, scripts, or navigation

## Generated HTML Link Integrity

Treat citation-reference matching in Markdown and citation navigation in generated HTML as separate publication requirements. `audit_citations.py` checks the first requirement; `audit_reference_links.py` checks the second.

Generate stable reference targets:

- assign each final reference a unique source ID
- render the target as `id="ref-{slug(source_id)}"`
- keep the same source ID and slug across rebuilds so saved links remain valid
- reject duplicate IDs and citation links whose target file or fragment does not exist

Generate links for both parenthetical and narrative citation forms, including multiple citations, year suffixes such as `2025a`, institutional authors, accepted abbreviations, possessives, and multiword surnames. Do not convert ordinary year ranges, case numbers, URLs, or non-citation parentheses into reference links.

Resolve paths from the page that contains the citation. A chapter page may use `19-references.html#ref-*`; a page under `sections/` may use `19-01-references.html#ref-*` or another verified relative path. Never assume that one relative URL works at every directory depth.

Make each DOI, official landing page, dataset page, or archived source URL clickable in the final References display. Keep internal citation navigation and external source access distinct: an internal anchor can be structurally valid even when an external site is temporarily unavailable. Report whether external URLs were syntax-checked, sampled live, or comprehensively tested.

Repair the canonical Markdown/build pipeline and rebuild generated HTML. Do not leave a hand-edited HTML-only fix that disappears on the next build. When only link repair was requested, compare the regenerated output with the prior published artifact after normalizing the intended link wrappers, anchor attributes, and link CSS. Any remaining difference in prose, tables, figures, scripts, navigation, or assets is out of scope and must be investigated before publication.

Do not run citation substitution across `<script>`, `<style>`, existing `<a>`, JSON, chart configuration, or editor-source blocks. Preserve these literal regions and visible statistical evidence.

Run:

```bash
python .agents/skills/country-report-agent/scripts/audit_reference_links.py [ISO3] --fail-on-issues
```

Before publication, confirm:

1. every generated citation link resolves to an existing HTML file and `ref-*` target
2. every reference target ID is unique on its page
3. final-reference entries expose a usable external link when one is registered
4. likely author-date citations do not remain as unlinked visible prose without an explicit reason
5. representative chapter, section, and References routes return successfully
6. a link-only change did not alter non-link content

## Reference Type Guidance

### Official Laws And Government Documents

Use the issuing government body as author when no personal author exists. Include law title, year, document number when available, and official source URL or local archive note.

### International Organization Reports

Use the institution as author. Include report title, year, series/report number when available, and DOI or official URL.

### Statistical Datasets

Use the database owner as author. Include dataset name, indicator/table ID or table title, country code, unit, year range, URL/API endpoint or access note, and access/download date if dynamic.

### Academic Articles

Verify journal, year, volume/issue/pages, DOI where available. Do not invent DOI or page ranges.

### Books And Chapters

Verify publisher and year. For chapters, include chapter author, chapter title, editors, book title, publisher, and DOI/URL if available.

### Working Papers And Research Institute Reports

Verify the institution, series number where available, title, year, and official landing page or PDF URL.

## Handling Uncertain References

If a source looks useful but cannot yet be verified:

- do not use it as an authoritative citation in final prose
- place it in a note or source-gap list with `needs verification`
- state what must be checked: DOI, URL, title, author, year, publisher, local file, or official source page
- prefer replacing it with a verified official, institutional, or scholarly source

## Updating References

When adding a new citation:

1. Add the APA in-text citation in the relevant Markdown section.
2. Add or update the final reference entry in `19-01-references.md`.
3. Add or update the source register or APA reference register if the workflow uses one.
4. Verify the source exists.
5. Record local archive path or access note when available.

When removing a citation:

1. Remove the in-text citation only if the claim remains supported or is removed.
2. Remove the final reference entry if it is no longer cited anywhere.
3. Preserve source-register history if it documents a consulted source.

## Publication Gate

A report is not publication-ready if:

- any major claim has no citation or source trail
- any in-text citation lacks a final reference entry
- final References contain unverifiable or invented-looking sources
- citation years and reference years conflict
- statistical references lack indicator/table IDs or dataset identity
- official documents cited in prose are absent from source registers or source notes without explanation

## Script Support

Use `scripts/audit_citations.py` for a first-pass match between in-text APA citations and final reference entries. Treat the output as triage: manually review institution-name variants, narrative citations, paragraph-level citations, and references that are intentionally retained for background or appendices.
