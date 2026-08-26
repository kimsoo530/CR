---
name: country-report-agent
description: Draft, build, diagnose, audit, and improve coherent evidence-based GDI Country Studies in this workspace. Use when working with ISO3 country folders, chapter-sensitive and non-template narrative design, `sources/sections/*.md`, source registers, section evidence plans, statistical coverage, citations, visual evidence, quality audits, publication-readiness checks, or student practice tasks for country-study production.
---

# GDI Country Studies Agent

## Overview

Use this skill to turn GDI Country Studies work into a controlled evidence workflow: diagnose first, preserve country-specific content, edit canonical Markdown, rebuild generated HTML when needed, and report remaining evidence gaps.

## Series Naming

- Use `GDI Country Studies` as the public series name.
- Format every country cover's visible title and HTML `<title>` as `GDI Country Studies: <Country Name>`.
- Do not use `Country Report`, `Country Report Series`, `Comparative Administration Country Report`, or `Professional Country Analysis Series` as the public cover series name. Retain “country report” only when it is a generic analytical term or part of an external source's official title.
- Preserve the established English country name for each study, including forms such as `Viet Nam` and `United States`.

## Cover Artwork

- Give each study a country-specific, text-free cover illustration that combines recognizable geography, public institutions, economy, and society without reducing the country to a flag, map outline, tourist postcard, political slogan, or stereotype.
- Store the optimized, self-hosted asset at `report/assets/cover-background.webp`. Keep the series title, country name, contributor details, and navigation as accessible HTML; never bake them into the bitmap.
- Compose wide cover art with quiet, dark negative space behind the title and the main visual identity toward the opposite side. Use a CSS gradient overlay so contrast does not depend on the image alone.
- Preserve the asset reference in the canonical builder as well as the generated `report/index.html` or stylesheet. Rebuilding the report must not remove the cover.
- Before publication, verify the image route, desktop and narrow-screen cropping, title and contributor readability, asset size, and a non-image fallback background. Prefer WebP and avoid unnecessary external image hosts.

## Workflow

1. Identify the task type: structure diagnosis, table-of-contents design, country-specific issue selection, source audit, schema/register design, citation/reference integrity review, statistical analysis, ChatGPT draft integration, section rewrite, narrative-style improvement, data/chart review, quality-gate review, report rebuild, prompt design, or student-practice support.
2. Locate the country folder and canonical files. Prefer `[ISO3]/sources/sections/*.md` for manuscript work and `[ISO3]/sources/section_evidence_plan.csv` or source registers for evidence mapping.
3. Diagnose before editing unless the user explicitly asks for immediate edits.
4. Preserve country-specific institutions, laws, reforms, regions, controversies, and academic debates.
5. Edit Markdown only within the requested scope. Treat generated HTML as an output artifact unless the user is editing slides or static presentation material.
6. Use `references/output_templates.md` when a structured audit table, evidence plan, or quality-gate summary would make the result easier to act on.
7. For a new report or broad rewrite, state each chapter's governing question, assign distinct roles to its sections, and classify each section as documentary, statistical, mixed, or interpretive. Choose a section-specific narrative pattern before drafting. Treat claim, evidence, mechanism, limitation, and implication as analytical checks, not mandatory visible headings or a fixed paragraph order. Do not treat a completed table of contents as a completed book.
8. When generated HTML contains citations, verify both semantic matching and rendered navigation: every linked citation must resolve to an existing reference anchor, reference URLs must be clickable, and chapter/section relative paths must be correct. Preserve scripts, charts, and prose while repairing links.
9. Run or inspect relevant build and audit outputs when the request implies verification. Before assigning `deep draft` or `publication candidate`, inspect section depth, statistical coverage, visual evidence, and rendered citation links in addition to citations and numeric claims.
10. Close with changed files, verification performed, the honest readiness level, and remaining source or editorial risks.

## Task Patterns

### Structure Diagnosis

Use for requests such as "inspect this country folder" or "what is missing?" Read `references/report_structure.md`. Read `references/country_specific_issue_protocol.md` when judging whether the report includes the country-specific issues needed to understand the case. Check:

- `raw/`, `processed/`, `code/`, `report/`, `sources/`, and `sources/sections/`
- `source_register.csv`, `section_evidence_plan.csv`, `enhanced_diagnostic_method.md`, quality-audit outputs, and build scripts
- coverage of high-risk chapters 3, 5, 7, 16, and 17
- whether the report has both the standard chapter structure and country-specific issue sections where needed

### Table Of Contents And Country-Specific Issues

Use when designing, revising, or auditing the report table of contents. Read `references/report_structure.md` for the standard chapter structure and `references/country_specific_issue_protocol.md` for issue selection and placement.

Keep the standard 1-19 chapter model for comparability. Add or preserve country-specific issue sections inside the relevant standard chapter when they are necessary to explain institutions, state capacity, political economy, development strategy, territorial condition, social structure, or external position.

Do not add special sections just to make the report longer. Each special section needs a country-specific central claim, placement rationale, and source plan.

### Source Audit

Use for citation, evidence, comparative governance sources, or publication-readiness questions. Read `references/source_quality_rules.md` when source reliability, source packages, citation sufficiency, BTI/V-Dem/QoG use, or data limitations matter. Read `references/citation_reference_integrity.md` when APA in-text citations, final References entries, invented-reference risk, DOI/URL existence, or source-to-reference matching matters.

Output a compact claim-evidence-source table when useful:

- claim or section issue
- current evidence
- missing evidence
- recommended source type
- priority

Read `references/output_templates.md` before returning a source gap table, claim-evidence-source table, APA citation audit table, or numeric claim audit table.

### Rendered Citation Link Integrity

Use when body citations, DOI links, reference navigation, or generated HTML links are missing or broken. Read `references/citation_reference_integrity.md` and audit the generated report with `scripts/audit_reference_links.py`.

Repair the canonical builder or source pipeline, then rebuild. Do not hand-patch generated HTML as the only fix. Give each final reference a stable `ref-*` anchor, link parenthetical and narrative author-date citations to that anchor, and calculate the target path from the current page depth. Treat chapter pages and `sections/` pages as separate relative-path contexts.

When the requested scope is link repair, prove that the rebuild preserved existing prose, tables, charts, scripts, and navigation. If a full rebuild removes unrelated material, stop that output from replacing the published tree; fix the generator or apply a narrow generated-artifact transformation while retaining the canonical generator correction.

### Schema And Register Design

Use when creating, repairing, or standardizing `source_register.csv`, `apa_reference_register.json`, `statistical_metadata.csv`, or `section_evidence_plan.csv`. Read `references/reference_schemas.md`.

Prefer explicit fields for source identity, verification status, local paths, section usage, indicator IDs, and access dates. Keep workflow metadata in registers rather than overloading reader-facing prose.

### Automated Audit Scripts

Use scripts for first-pass checks when a country folder exists and the user asks about publication readiness, APA references, unsupported numbers, or broad quality issues:

```bash
python .agents/skills/country-report-agent/scripts/audit_citations.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_reference_links.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_numeric_claims.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_section_depth.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_statistical_coverage.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_visual_evidence.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_narrative_structure.py [ISO3]
python .agents/skills/country-report-agent/scripts/audit_report.py [ISO3] --fail-on-blockers
```

Prefer `audit_report.py` for a broad review; use the individual scripts to diagnose its findings. The integrated audit separates blockers, warnings, and mandatory editorial review. Treat script output as a triage aid, not a final judgment. Manually review false positives and important missed cases before changing manuscript text.

### Section Rewrite

Use for improving `sources/sections/*.md`. Read `references/section_rewrite_protocol.md` before substantial rewrites. Read `references/narrative_style_protocol.md` when the output must become reader-facing book prose. Read `references/citation_reference_integrity.md` before adding, changing, or removing APA in-text citations or reference entries.
Read `references/country_specific_issue_protocol.md` when adding, renaming, relocating, or preserving sections that address country-specific issues.
Read `references/chatgpt_draft_integration.md` when the section draft came from ChatGPT or when preparing an evidence brief for ChatGPT drafting.

Use the diagnostic depth bands in `references/section_rewrite_protocol.md`. Never expand prose merely to satisfy a word count; a short-section flag means that claims, mechanisms, evidence, interpretation, and comparative implications require human review.

For multi-section or chapter revisions, read `references/chapter_coherence_protocol.md`. Define the chapter question and section roles before editing, then review transitions, repeated evidence, conceptual consistency, disagreement, and the chapter-level answer after editing.

Before rewriting more than one section, assign each section a narrative pattern based on its substantive purpose. Do not apply a shared visible sequence such as `Analytical claim`, `Statistical evidence`, `Mechanisms`, `Limits`, and `Implications` across the manuscript. A concept needed for analytical rigor may be integrated within prose, omitted when irrelevant, or placed in a different order when the section's logic requires it.

Preserve:

- named institutions and laws
- country-specific reform episodes
- regional and territorial details
- exact statistics with source metadata
- legitimate scholarly disagreement or uncertainty

Remove:

- prompt-like instructions
- generic transitions
- unverified numerical claims
- mechanical evidence inventories in reader-facing prose
- chart interpretations that only describe methodology
- repeated audit-like headings or boilerplate paragraphs inserted to make every section appear complete

### ChatGPT Draft Integration

Use when the user wants to draft prose in ChatGPT and bring it back into this workspace, or when a pasted draft was written outside Codex. Read `references/chatgpt_draft_integration.md`.

Treat ChatGPT output as an unverified manuscript draft, not a source. Use Codex to prepare evidence briefs before drafting, then verify claims, statistics, citations, references, country-specific facts, section placement, and Markdown integration before updating canonical files.

### Legal And Political Chapters

Use for constitutions, amendments, elections, courts, federalism, accountability, and political-system diagnostics. Read `references/legal_political_chapter_protocol.md`.

Separate enacted law from proposals, judicial holdings from implementation, election denominators from one another, and perception indicators from administrative performance. Preserve visible `X.Y` numbering in both canonical Markdown and generated HTML.

### Administrative System Chapters

Use for centre-of-government coordination, machinery-of-government reform, civil-service management, public financial administration, local delivery, digital administration, or implementation-capacity analysis. Read `references/administrative_chapter_protocol.md`.

Map authority, finance, personnel, information, implementation, and correction as distinct but connected circuits. Do not infer administrative performance from an organogram, mandate, reform announcement, dashboard, meeting count, or composite score. Use editable tables or code-based diagrams for exact institutional relationships; use generated imagery only when it clarifies rather than simplifies the evidence.

### Narrative Style Improvement

Use when a section feels mechanical, template-like, stitched together, overloaded with source names, or too close to an audit table. Read `references/narrative_style_protocol.md`.

Keep workflow tables, audit results, source inventories, and update instructions outside reader-facing prose. Convert them into country-specific analytical paragraphs with varied structure, clear interpretation, and natural citation density.

For a full-chapter or full-book revision, inspect section headings across the manuscript as a set. Repeated topical headings may be legitimate, but repeated analytical checklist headings are not. Run `scripts/audit_narrative_structure.py` and manually compare neighboring sections before classifying the prose as a deep draft.

### Statistical Analysis And Visualization

Use when a section needs statistics from the World Bank, IMF, UN, ILO, WHO, OECD, regional development banks, BTI, V-Dem, QoG, research institutes, national statistical offices, central banks, or other structured datasets. Read `references/statistical_analysis_protocol.md` before collecting, processing, charting, or inserting statistical evidence.
Read `references/reference_schemas.md` when recording indicator metadata, raw/processed paths, source IDs, or statistical evidence plans.

Do not add a statistic merely because it is available. Use statistics to test a claim, identify a trend, compare countries, show a turning point, measure state capacity, or qualify an official narrative.

For a new full report, prepare the statistical evidence plan before drafting data-intensive chapters. Link prose to registered `indicator_id`, `chart_id`, and `source_id` values. A latest-value-only paragraph does not count as adequate statistical integration when a trend, comparator, or distribution is needed to support the claim. A `statistics-not-applicable` HTML comment alone is not an exemption; record `statistics_status=not_applicable` and a substantive reason in the evidence plan.

Expected outputs may include:

- statistical evidence plan
- source and indicator inventory
- raw/processed file placement plan
- analysis table
- chart plan with units and source notes
- prose interpretation ready for a section

When the user wants reusable collection and visualization from the GDI Colab toolkit, also read `references/international_statistics_toolkit.md`. Use `scripts/international_statistics_pipeline.py` with a copied and edited `references/international_statistics_example.json` or `references/multi_source_statistics_example.json`. The pipeline supports World Bank Indicators/WGI, IMF DataMapper and official WEO SDMX bulk data, WHO GHO, UNDP HDR, official WhoGov, ILOSTAT, UN DESA WPP, and table-specific UNCTAD bulk archives. Treat WITS, QoG, and other file-based examples as separate verified-source extensions rather than silently reusing notebook or Drive dependencies.

For leadership experience, cabinet size, women in cabinet, average tenure, minister age, core cabinet, and cabinet retention, use `references/whogov_example.json` and `references/whogov_indicator_catalog.csv`. Preserve the WhoGov version and codebook, calculate women's shares from matching female and total counts, distinguish cabinet ministers from core or total positions, distinguish continuous from total leader experience, and never infer expertise, policy continuity, or administrative performance directly from tenure or personnel-retention measures.

Do not paste notebook functions unchanged into a country report. The reusable pipeline must preserve immutable raw payloads in their true format, tidy observations, metadata, validation results, formulas, peer definitions, and chart source notes. For WHO and ILOSTAT, require exact dimensions when duplicate country-year observations exist. For IMF WEO and UN DESA WPP, record the vintage, variant, and estimate/projection boundary. For UNCTAD, preserve the table ID and all analytical dimension filters. For every source, justify peers and periods from the section's analytical question. Derived indicators must preserve missingness and state the formula; comparison modules must state the target, fixed peer list, statistic, minimum peer count, and non-causal status unless the research design supports a causal claim.

When the user requests a categorized statistical appendix or a "country in statistics" overview, run the validated international-statistics pipeline first and then use `scripts/build_statistical_country_profile.py` with a copied `references/statistical_country_profile_example.json`. Classify indicators by the substantive question rather than the issuing institution. Require distinct units, visible observation years, source and limitation notes, at least eight points for a trend chart, an explicit fixed peer group, and a mix of trend, current-level comparison, and start-to-end change views where the evidence supports them. Treat the generated descriptive paragraphs as an editorial starting point, not a substitute for country-specific institutional analysis.

For multi-country trend charts, encode country identity redundantly with both color and line style. Keep the focal country visually dominant with the series focal color, solid line, and thicker stroke; assign each peer a stable distinct color and dash pattern. Do not rely on color alone or render all peers as indistinguishable gray lines.

For HTML statistical appendices, keep PNG and SVG exports as durable static artifacts and add a self-hosted interactive layer that reveals the year, country, value, and unit on pointer hover or click. Do not depend on a third-party CDN, and keep the chart usable when JavaScript is unavailable by retaining the static image, visible axes, legend, and source note.

When a reference notebook or statistical catalog contains more variables than the first appendix draft, inventory the entire substantive table of contents before selecting charts. Separate (a) variables already present in the validated run, (b) internationally comparable variables supported by an existing adapter but not yet requested, (c) variables requiring a new adapter, (d) country-specific administrative or survey measures, (e) derived analyses, and (f) setup or task cells that are not variables. Use `auto_include_unlisted: true` so every distinct focal-country indicator in `observations.csv` is visualized, and attach `references/colab_statistical_visualization_catalog.csv` (or a country-specific successor) as `coverage_catalog` so unavailable items remain visible as a coverage plan rather than disappearing. If a provider returns peer observations but no focal-country observation, do not create a peer-only chart: classify it as `target_data_unavailable` and record it in `target_missing_indicators`. Never create placeholder charts, treat missing values as zero, or imply that Korea-only KOSIS/NPS series exist for another country. Report `input_indicators`, `target_available_indicators`, `visualized_indicators`, `target_missing_indicators`, and `omitted_input_indicators` in validation output and require zero unexplained omissions before claiming coverage of the available focal-country data. Exclude credentials and helper-code cells from every report artifact and immediately flag any plaintext secret found in a source notebook.

### Quality Gate

Use for "ready for publication?", "audit this report", or "what should we fix first?" Read `references/quality_gate.md`. Read `references/narrative_style_protocol.md` when judging whether the manuscript reads like a book rather than a mechanical workflow output. Read `references/citation_reference_integrity.md` when judging whether citations and final references are publication-ready.
Read `references/country_specific_issue_protocol.md` when judging whether the report captures the country's decisive issues, not only the generic table of contents.
Read `references/chatgpt_draft_integration.md` when judging sections drafted or enriched outside Codex.
Run `scripts/audit_report.py` (which invokes all six focused audits) when the country folder is available and the user wants a broad readiness review. Read `references/chapter_coherence_protocol.md` and perform the manual chapter review that automation cannot replace. Treat audit output as evidence for, not a substitute for, editorial judgment.

Classify as:

- `structured first-pass`: standard structure exists, but sections may remain outline-length and official-source, statistical, visual, or country-specific depth remains limited
- `deep draft`: substantial country-specific argument, evidence, and interpretation exist across the manuscript; data-intensive chapters have usable statistical evidence beyond isolated latest values; quality-gate gaps remain
- `publication candidate`: major chapters, citations, source register, statistical coverage, charts or justified visual exceptions, references, and external-review issues are substantially resolved

Do not classify a report as `deep draft` when most sections are outline-length, data-intensive chapters lack actual statistical integration, or the evidence plan exists only as workflow metadata. Do not classify a report as `publication candidate` when the report has no tables or figures without a documented section-by-section reason.

### Student Practice

Use when the user is preparing teaching materials or asking for classroom workflows. Read `references/student_practice_mode.md`.
Read `references/prompt_templates.md` when the user needs student-facing or researcher-facing Codex prompt examples.

Emphasize outputs students can produce:

- target country and section
- one-sentence central thesis
- claim-evidence-source table
- improved Codex prompt
- top three revision priorities

## Useful Local Files

- Root standards: `design.md`
- Global audit: `country_report_quality_audit.md`
- Source-gap plan: `official_source_gap_plan.md`
- Pipeline docs: `tools/README_chatgpt_statistical_section_pipeline.md`
- International-statistics pipeline: `scripts/international_statistics_pipeline.py`
- International-statistics guide: `references/international_statistics_toolkit.md`
- International-statistics example config: `references/international_statistics_example.json`
- Multi-source statistics and benchmark example: `references/multi_source_statistics_example.json`
- World Bank curated indicator catalog: `references/world_bank_indicator_catalog.csv`
- WhoGov leadership and cabinet example: `references/whogov_example.json`
- WhoGov indicator catalog: `references/whogov_indicator_catalog.csv`
- Statistical-country-profile generator: `scripts/build_statistical_country_profile.py`
- Statistical-country-profile example: `references/statistical_country_profile_example.json`
- Reference-notebook variable coverage catalog: `references/colab_statistical_visualization_catalog.csv`
- Batch docs: `tools/README_country_report_batch.md`
- Country manuscript: `[ISO3]/sources/sections/*.md`
- Country evidence plan: `[ISO3]/sources/section_evidence_plan.csv`
- Country source register: `[ISO3]/sources/source_register.csv`
- Country APA reference register when present: `[ISO3]/sources/apa_reference_register.json`
- Country statistical metadata when present: `[ISO3]/processed/statistical_metadata.csv`
- Country quality audits: `[ISO3]/quality_audit/*.md`
- Statistical pipeline data when present: `[ISO3]/raw/statistical_section_pipeline/` and `[ISO3]/processed/statistical_section_pipeline_long.csv`
- Skill citation audit script: `scripts/audit_citations.py`
- Skill rendered-reference-link audit script: `scripts/audit_reference_links.py`
- Skill numeric-claim audit script: `scripts/audit_numeric_claims.py`
- Skill section-depth audit script: `scripts/audit_section_depth.py`
- Skill statistical-coverage audit script: `scripts/audit_statistical_coverage.py`
- Skill visual-evidence audit script: `scripts/audit_visual_evidence.py`
- Skill narrative-structure audit script: `scripts/audit_narrative_structure.py`
- Skill integrated audit script: `scripts/audit_report.py`

## References

- Read `references/report_structure.md` for folder and report architecture checks.
- Read `references/country_specific_issue_protocol.md` for selecting, placing, evidencing, and integrating country-specific issue sections within the standard table of contents.
- Read `references/reference_schemas.md` for source register, APA register, statistical metadata, and evidence plan field standards.
- Read `references/output_templates.md` for structured audit tables, evidence plans, rewrite reports, and quality-gate summaries.
- Read `references/prompt_templates.md` for student, instructor, and researcher prompt examples.
- Read `references/source_quality_rules.md` for source sufficiency, source types, and citation rules.
- Read `references/citation_reference_integrity.md` for APA in-text citation, final References, source existence, citation-reference matching, generated anchors, relative paths, and rendered-link validation rules.
- Read `references/statistical_analysis_protocol.md` for statistical source collection, processing, analysis, visualization, governance indicator use, and prose-integration rules.
- Read `references/chatgpt_draft_integration.md` for evidence briefs, ChatGPT-assisted drafting, draft intake, verification, and safe integration into canonical Markdown.
- Read `references/legal_political_chapter_protocol.md` for legal status, implementation evidence, election denominators, political indicators, and numbered-section integrity.
- Read `references/administrative_chapter_protocol.md` for central coordination, organizational reform, civil service, financial controls, local delivery, digital administration, and implementation-chain analysis.
- Read `references/narrative_style_protocol.md` for book-like analytical prose, anti-mechanical rewriting, paragraph rhythm, and narrative synthesis.
- Read `references/chapter_coherence_protocol.md` for chapter questions, distinct section roles, narrative-pattern choice, transitions, evidence overlap, and manual chapter review.
- Read `references/section_rewrite_protocol.md` for Markdown revision workflow.
- Read `references/quality_gate.md` for report status classification.
- Read `references/student_practice_mode.md` for classroom mode and assignments.
