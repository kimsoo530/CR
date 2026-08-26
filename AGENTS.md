# GDI Country Studies Workspace Instructions

## Project Purpose

This workspace produces the evidence-based electronic series `GDI Country Studies`. Treat each country folder as a reproducible study package, not as a loose collection of generated HTML files.

## Series Naming

- Use `GDI Country Studies` as the official public series name.
- Format each country's visible cover title and HTML `<title>` as `GDI Country Studies: <Country Name>`.
- Do not use `Country Report` or earlier variant labels as the public series name. The phrase “country report” may remain when used generically or when it is part of an external source's official title.
- Use a country-specific, text-free `report/assets/cover-background.webp` for the first page. Keep all titles and contributor information as HTML, preserve the reference in the builder, and verify desktop/mobile contrast and cropping before publication.

## Canonical Files

- Treat `[ISO3]/sources/sections/*.md` as the canonical manuscript.
- Treat `[ISO3]/report/*.html` and `[ISO3]/report/sections/*.html` as generated reader-facing artifacts.
- Treat `[ISO3]/raw/` as preserved source material. Do not edit raw files unless the user explicitly asks to repair or replace a corrupted download.
- Treat `[ISO3]/processed/` as derived analytical data used by charts, tables, and quantitative prose.
- Store or document consulted legal, official, diagnostic, academic, statistical, and map sources under `[ISO3]/sources/`.

## Country Report Method

- Preserve the standard 1-19 chapter structure for comparability across countries.
- Add or preserve country-specific issue sections inside the relevant standard chapter when they are necessary to understand the country's institutions, state capacity, political economy, development path, territorial condition, social structure, or external position.
- Use `.agents/skills/country-report-agent/references/country_specific_issue_protocol.md` when selecting, placing, or auditing country-specific issue sections.
- Explain official institutional design with constitutions, laws, government organization documents, budgets, plans, administrative rules, and official statistics.
- Test actual performance and constraints with comparable international indicators and independent diagnostic reports.
- Use BTI, V-Dem, and QoG as comparative governance and institutional-performance sources when relevant, while recognizing that they complement rather than replace official country-specific sources.
- Use academic literature to clarify contested institutional, political-economy, or comparative-administration interpretations.
- Preserve country-specific institutions, laws, reforms, regions, conflicts, policy episodes, and scholarly debates during any rewrite.
- Do not turn the report into a generic template where only the country name changes.

## Evidence Rules

- For quantitative claims, include exact value, year or period, unit, source institution, and indicator/table ID when available.
- Separate national official data from international comparable data. National data normally supports latest/granular claims; international data supports cross-country comparability and long-run trend reading.
- Do not mix incompatible units in one chart. Separate values, percentages, ratios, index scores, and counts unless a clear multi-panel design handles units safely.
- Do not cite news as authoritative evidence for structural claims unless the user explicitly asks and limitations are stated.
- Flag missing, stale, blocked, or ambiguous sources instead of guessing.
- Use APA-style in-text citations for cited evidence.
- Every in-text citation must map to a real, verified reference entry in the final References chapter.
- Do not cite unverifiable or invented references; mark uncertain items as `needs verification`.

## Statistical Analysis Rules

- When a section needs statistical evidence, follow `.agents/skills/country-report-agent/references/statistical_analysis_protocol.md`.
- Prefer structured APIs, downloaded datasets, official tables, or documented bulk files over manual copy-paste.
- Preserve raw statistical files under `[ISO3]/raw/` and write cleaned analytical datasets under `[ISO3]/processed/`.
- Record source institution, dataset name, indicator/table ID, URL or access note, download/access date, unit, frequency, and latest non-missing year.
- Use national official statistics for latest and granular claims; use World Bank, IMF, UN, ILO, WHO, OECD, regional development banks, and research-institute data for comparability and diagnostic context.
- For BTI, V-Dem, QoG, and other governance indicators, record dataset/report version, indicator name or code, year, scale direction, and methodological caveat.
- Every chart must answer a substantive section question and be followed by prose interpretation.
- Use `.agents/skills/country-report-agent/references/reference_schemas.md` when standardizing `source_register.csv`, `apa_reference_register.json`, `statistical_metadata.csv`, or `section_evidence_plan.csv`.

## Editing Workflow

- Diagnose before editing when the user asks for improvement, review, or publication readiness.
- Keep changes scoped to the requested country, chapter, section, or file.
- Before major rewrites, identify the strongest existing country-specific evidence and preserve or deliberately relocate it.
- When using ChatGPT for richer drafting, first prepare an evidence brief in Codex, then treat the returned ChatGPT text as unverified manuscript input that must be checked before integration.
- Use `.agents/skills/country-report-agent/references/chatgpt_draft_integration.md` when preparing ChatGPT briefs or integrating ChatGPT-assisted drafts.
- Remove reader-facing production language such as `this chapter should`, `placeholder`, `for annual updates`, `Evidence Used in This Section`, and generic chart filler.
- Keep workflow tables, audit results, source inventories, and update instructions out of reader-facing prose unless they belong in an appendix.
- After evidence-heavy edits, apply `.agents/skills/country-report-agent/references/narrative_style_protocol.md` so the manuscript reads as analytical book prose rather than a mechanical checklist.
- Prefer section-level Markdown edits over direct HTML edits unless the user is explicitly editing the slide deck or generated artifact.
- After Markdown edits, rebuild the report when a country build script exists and the user request implies updated HTML.

## Quality Gates

- Classify reports as `structured first-pass`, `deep draft`, or `publication candidate`.
- A publication candidate must have country-specific official sources for constitution/basic law, government organization, civil service or public employment, budget/debt, audit or anti-corruption, local government where relevant, current development strategy, financial sector or central bank, and national statistics.
- A publication candidate must preserve the standard chapter structure while covering the country-specific issues that are decisive for understanding the case.
- Chapters 3, 5, 7, 16, and 17 require especially careful country-specific rewriting before publication.
- Fragile, conflict-affected, partially recognized, or de facto divided polities require statehood, territorial-control, recognition, humanitarian service delivery, and de facto authority notes where relevant.
- A publication candidate must have natural narrative synthesis: country-specific claims, interpreted evidence, varied paragraph rhythm, and no visible workflow language in reader-facing sections.
- A publication candidate must not contain unverified claims, invented citations, unsupported statistics, or unverifiable references introduced by ChatGPT-assisted drafting.
- Before publication, verify that APA in-text citations, final reference entries, source-register records, and local archived/source notes are mutually consistent.
- When available, run `.agents/skills/country-report-agent/scripts/audit_citations.py [ISO3]` and `.agents/skills/country-report-agent/scripts/audit_numeric_claims.py [ISO3]` as first-pass checks, then manually review the flagged issues.
- Run or inspect quality audits when available before claiming a report is ready.

## Codex Operating Rules

- Use `rg` or `rg --files` first for search and discovery.
- Prefer local project scripts over ad hoc reconstruction.
- Do not overwrite unrelated user changes.
- Do not perform destructive operations without explicit user approval.
- When creating reusable workflows, prefer project-scoped skills under `.agents/skills/`.
