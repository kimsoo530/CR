# Section Rewrite Protocol

When revising more than one section in a chapter, read `chapter_coherence_protocol.md` first and assign each section a distinct role. Do not impose one prose sequence across sections merely because the same analytical checks apply to all of them.

Use this reference before substantial edits to `sources/sections/*.md`. When producing reader-facing prose, also read `narrative_style_protocol.md`. When integrating a ChatGPT draft, also read `chatgpt_draft_integration.md`. When adding, removing, or changing citations, also read `citation_reference_integrity.md`.

## Before Editing

1. Read the target section and, when needed, the neighboring section titles in the same chapter.
2. Identify the current central claim.
3. Extract country-specific material that must be preserved: institutions, laws, reforms, regions, dates, named programs, controversies, and scholarly debates.
4. Check the section evidence plan and source register when available.
5. If the text came from ChatGPT or another external drafting step, identify new claims, statistics, citations, and references that must be verified before integration.
6. Diagnose issues before changing text unless the user requested immediate rewriting.

## Rewrite Shape

A strong analytical section normally includes:

- a clear country-specific claim
- the institutional, historical, or policy mechanism behind the claim
- documentary or statistical evidence
- interpretation of what the evidence means for state capacity, implementation, or policy risk
- a link back to the report's central thesis

Do not force this sequence into every paragraph. Use the evidence to build a natural narrative arc. Choose historical development, institutional operation, statistical interpretation, comparative position, or contested interpretation patterns from `narrative_style_protocol.md` when appropriate.

## Select Structure Before Drafting

For multi-section work, record a private drafting decision for each section before writing:

- the section's substantive question
- its dominant narrative pattern
- whether statistics are central, supporting, or unnecessary
- the natural opening and ending
- zero to three reader-facing subheadings, if subheadings genuinely improve navigation

Do not convert this drafting decision into a repeated manuscript template. `Analytical claim`, `Statistical evidence`, `Mechanisms`, `Limitations`, `Policy implications`, and similar terms are diagnostic categories, not default reader-facing headings.

Use no subheading when a short historical or interpretive section reads more coherently as continuous prose. When subheadings are useful, name the country-specific institution, episode, dispute, trend, or trade-off. Avoid using the same abstract analytical headings in neighboring sections.

Vary the order according to the section's governing question. Evidence may open a data-centered section, follow institutional background in a historical section, or appear between competing interpretations in a contested section. Mechanisms may be implicit in chronological explanation and need not occupy a separately labeled block.

## Diagnostic Depth Bands

Use length as a warning signal, never as a writing target by itself:

- under 200 words: normally outline or abstract length; do not treat as a finished analytical section without a documented reason
- 200-499 words: structured first-pass range; inspect for missing mechanism, evidence, disagreement, or implication
- 500-799 words: normal working range for a developed section when the argument is focused
- 800-1,200 words: common working range for high-risk or integrative sections that require multiple institutions, evidence types, or competing interpretations

Chapters 3, 5, 7, 16, and 17 usually require deeper treatment, but do not pad prose or force every section into the same length. A legally focused, definitional, or tightly scoped section may be shorter when it still answers its question and the reason is recorded in the quality audit.

For a developed section, inspect whether the prose contains, as applicable:

- a specific analytical question and answer
- institutional or historical mechanism
- verified documentary or statistical evidence
- temporal change, comparison, distribution, or a reason these are not relevant
- variation across regions, groups, sectors, or implementing organizations when material
- counterargument, limitation, or evidentiary uncertainty
- comparative-administration or policy implication

Do not call a section complete merely because it has a heading, two summary paragraphs, citations, and valid HTML.

## Preserve

- Country-specific evidence and named institutions
- Exact values and source metadata when valid
- Useful existing citations
- Distinctive local terms and administrative structures
- Legitimate uncertainty or evidence limitations

## Remove Or Relocate

- `This chapter should`, `The report should`, `For annual updates`
- `Evidence Used in This Section`
- `Reading the Evidence`
- `Figure interpretation` labels when used as placeholders
- `The analytical value of...`
- `claim-evidence-source table`, `source gap table`, `audit result`, `workflow`, and similar process language in reader-facing prose
- generic paragraphs transferable to any country
- source inventories that belong in source registers, evidence plans, or appendices
- unsupported enrichment introduced by external drafting

## Narrative Synthesis Step

After evidence and citations are in place:

1. Identify the section's authorial claim in one sentence.
2. Move tables, source names, and statistical metadata into supporting roles.
3. Put country-specific institutions, laws, reforms, constraints, or policy episodes at the center of the prose.
4. Vary paragraph structure so the section does not repeat the same claim-evidence-interpretation rhythm mechanically.
5. Ensure each major paragraph explains why the evidence matters for institutions, state capacity, implementation, or policy risk.

## After Editing

- Run `scripts/audit_section_depth.py` for a new report, full-chapter rewrite, or publication-readiness review, and manually inspect every critical-short flag.
- Recheck numerical claims for value, year, unit, and source.
- Confirm APA in-text citations are consistent with the final References chapter, reference register, DOI/URL/source existence checks, and local source notes where available.
- Confirm any ChatGPT-assisted material has been verified and trimmed to the evidence trail.
- Confirm the section does not read like an audit table, evidence inventory, or prompt response.
- Compare the section's visible headings and paragraph sequence with at least two neighboring sections. Remove repeated analytical labels and boilerplate that do not arise from the subject matter.
- Confirm the section still fits the chapter's role.
- Rebuild HTML when the task requires updated report output and a build script exists.
- Report remaining source gaps instead of hiding them.
