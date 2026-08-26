# Quality Gate

Use this reference when judging report readiness or prioritizing fixes. For APA in-text citation matching, final References integrity, and real-source verification, also read `citation_reference_integrity.md`. For country-specific issue coverage and table-of-contents design, also read `country_specific_issue_protocol.md`. For ChatGPT-assisted or externally drafted prose, also read `chatgpt_draft_integration.md`. For book-like prose and anti-mechanical style checks, also read `narrative_style_protocol.md`. For standard quality-gate tables, read `output_templates.md`.

## Status Levels

### Structured First-Pass

The report has the standard chapter and section structure, basic data, and generated HTML. It may still contain outline-length sections, shallow country-specific analysis, missing country-specific issue sections, incomplete official-document coverage, weak citations, mechanical source listing, or sections that read like template text. A complete site shell is not evidence that the manuscript is a complete book.

### Deep Draft

The report has meaningful country-specific evidence, stronger analytical claims, improved citations, country-specific issue sections in plausible chapters, and fewer mechanical artifacts. Most sections are developed prose rather than outlines, and data-intensive chapters use statistical evidence beyond isolated latest values. It may still require narrative smoothing, issue integration in chapter 17, source replacement, chart cleanup, external-review response, or chapter-specific rewriting.

### Publication Candidate

The report is close to external release. It has country-specific official sources, verified APA citations and reference entries, sufficient statistical coverage, figure notes, coherent thesis, strong chapters 3/5/7/16/17, well-placed country-specific issue sections, natural book-like prose, no obvious production language, and a documented response to evidence limitations.

## Classification Guardrails

Use `scripts/audit_report.py` as the broad triage entry point, inspect the focused audit behind each finding, and then review the flagged sections manually. Automated success never waives the chapter-coherence review.

- Keep the report at `structured first-pass` when most substantive sections are under 500 words, many are under 200 words, or the text mainly states conclusions without mechanism and evidence.
- Keep the report at `structured first-pass` when data-intensive chapters lack actual statistics in prose, tables, or figures, even if an evidence-plan CSV names possible indicators.
- Do not use word count as proof of quality. A long generic section can still be first-pass, and a shorter tightly scoped section can pass with a documented reason.
- Require data-intensive sections to use the relevant combination of level, trend, comparison, and distribution. A latest-value-only paragraph normally cannot support claims about change, relative performance, inequality, or implementation variation.
- Do not classify a report with zero tables and zero figures as `publication candidate` unless the quality audit documents why visual evidence is unnecessary for each data-intensive chapter.
- Never describe a `structured first-pass` or `deep draft` as a completed book without stating the remaining editorial and evidence work.

## Priority Fix Order

1. Preserve or restore lost country-specific evidence.
2. Remove placeholders and production instructions.
3. Strengthen the central thesis and chapter-specific arguments.
4. Identify missing or misplaced country-specific issue sections.
5. Convert mechanical evidence lists into natural analytical prose.
6. Fill official-source gaps for constitution, administration, fiscal system, policy strategy, and integrated assessment.
7. Fix unsupported numerical claims.
8. Split mixed-unit charts and add source footnotes.
9. Add natural chart interpretation.
10. Align APA citations and References.
11. Verify that cited references actually exist through DOI, URL, official publication pages, local archives, or access notes.
12. Run or inspect quality audit outputs.
13. Run the narrative-structure audit and compare neighboring sections for repeated headings, paragraph order, and boilerplate.
14. Apply `chapter_coherence_protocol.md`: verify the governing question, distinct section roles, transitions, evidence overlap, and synthesis.
15. Document unresolved limitations.

## High-Risk Chapters

- Chapter 3: constitutional order and actual allocation of authority
- Chapter 5: administrative organization, civil service, accountability, local implementation
- Chapter 7: revenue, expenditure, debt, procurement, audit, fiscal risk
- Chapter 16: development strategy, reform sequencing, implementation capacity
- Chapter 17: integrated operating model and comparative-administration contribution

## Publication Candidate Must Not

- Rely mainly on generic template language
- Omit issues that are structurally decisive for understanding the country
- Add special sections without source plans or placement rationale
- Read like a checklist, audit output, evidence inventory, or source-register summary
- Present official policy plans as achieved outcomes
- Use international indicators without methodological limits
- Contain unsupported numeric claims
- Leave first-pass status ambiguous
- Mix incompatible chart units
- Omit source registers or reference alignment
- Include unverifiable, invented, or unmatched references
- Treat ChatGPT-generated claims, citations, statistics, or references as verified evidence without checking the source trail

## Narrative Quality Checks

Before classifying a report as `publication candidate`, confirm:

- major sections have an authorial analytical claim, not only accumulated facts
- workflow language is absent from reader-facing prose
- statistics are interpreted rather than listed
- citations support paragraphs without dominating the prose
- paragraph openings and endings are varied
- country-specific institutions, laws, reforms, places, and policy episodes drive the narrative
- short sections have a documented substantive reason rather than reflecting unfinished drafting
- visible subheadings arise from the subject matter rather than a shared analytical checklist
- neighboring sections do not repeat the same paragraph sequence or methodological disclaimer without a substantive reason
- each chapter has a governing question, distinct section roles, cumulative transitions, and a synthesis that answers the chapter question

## Statistical And Visual Coverage Checks

Before classifying a report as `deep draft` or `publication candidate`, confirm:

- data-intensive sections are identified and mapped to actual datasets, not only proposed sources
- relevant sections interpret at least two dimensions among level, trend, comparison, and distribution, or document a defensible exception
- latest, granular, and subnational claims use national official statistics where available
- processed data, prose values, tables, and figures can be traced to raw sources and metadata
- each table or figure answers a section question and is interpreted in the prose
- zero-visual or sparse-visual reports have an explicit editorial justification
- `audit_section_depth.py`, `audit_statistical_coverage.py`, `audit_visual_evidence.py`, and `audit_narrative_structure.py` outputs were reviewed manually

## Country-Specific Issue Checks

Before classifying a report as `deep draft` or `publication candidate`, confirm:

- the standard 1-19 chapter structure remains intact
- country-specific issue sections are added only where they explain a major institutional, fiscal, social, territorial, development, or geopolitical feature
- special sections are placed in the chapter with the strongest mechanism
- high-priority special issues have source plans and evidence trails
- chapter 17 synthesizes the most important cross-cutting issues

## ChatGPT-Assisted Draft Checks

Before classifying ChatGPT-assisted sections as `deep draft` or `publication candidate`, confirm:

- the draft was treated as manuscript input, not as a source
- new claims introduced by the draft were verified or removed
- statistics from the draft have value, year, unit, and source
- citations and references from the draft exist and match the final References chapter
- useful narrative richness was preserved without keeping unsupported detail
