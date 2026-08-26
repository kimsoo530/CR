# Prompt Templates

Use this reference when preparing student exercises, researcher workflows, or reusable Codex prompts for country-report production.

## Prompt Formula

Use five parts:

1. Goal: what the agent should accomplish
2. Context: country, chapter, section, data, and files
3. Constraints: preserve facts, citation rules, scope limits, source hierarchy
4. Actions: inspect, diagnose, edit, audit, rebuild, or report
5. Done when: concrete completion conditions

## Student Basic Diagnosis Prompt

```text
Use $country-report-agent.

Goal: Diagnose one country-report section and identify what evidence is missing.
Context: Country folder is [ISO3]. Target section is [section file].
Constraints: Do not rewrite the section yet. Preserve country-specific institutions, laws, reforms, regions, and statistics. Distinguish official sources, international datasets, diagnostic reports, academic sources, and news.
Actions: Read the section, source register, and section evidence plan if present. Produce a claim-evidence-source table and identify the top three revision priorities.
Done when: I have a compact table, a readiness judgment, and a short note on what a human must verify.
```

## Student Rewrite Prompt

```text
Use $country-report-agent.

Goal: Improve one paragraph so it reads like a country-specific analytical report, not a generic template.
Context: Country folder is [ISO3]. Target section is [section file]. Focus on the paragraph beginning "[quote first words]".
Constraints: Keep verified facts, named institutions, laws, dates, statistics, and APA citations. Do not invent sources or numbers. If evidence is missing, mark the gap instead of guessing.
Actions: Diagnose the paragraph, rewrite it as reader-facing book prose, and explain what evidence supports the revised claim. Keep workflow tables and audit language out of the rewritten paragraph.
Done when: The paragraph has a clear claim, evidence, interpretation, and remaining source gap note.
```

## Narrative Style Improvement Prompt

```text
Use $country-report-agent.

Goal: Make this section read less mechanically while preserving evidence and citation integrity.
Context: Country folder is [ISO3]. Target section is [section file].
Constraints: Do not remove verified country-specific facts, statistics, institutions, laws, reforms, or APA citations. Do not add new unsupported claims. Keep audit tables, workflow language, and source inventories out of reader-facing prose.
Actions: Read the section and identify mechanical prose symptoms. Rewrite the most affected paragraphs using natural analytical narrative patterns. Briefly report what changed and what evidence still needs verification.
Done when: The section has varied paragraph rhythm, interpreted evidence, country-specific claims, and no visible workflow language.
```

## Codex Evidence Brief For ChatGPT Prompt

```text
Use $country-report-agent.

Goal: Prepare an evidence brief that I can give to ChatGPT for drafting a richer book-style section.
Context: Country folder is [ISO3]. Target section is [section file].
Constraints: Do not write the final prose yet. Use only verified or clearly marked evidence from the country folder, source register, evidence plan, statistical metadata, and existing section text. Mark gaps and uncertain claims explicitly.
Actions: Identify the section question, central claim, must-preserve facts, verified evidence, statistics, country-specific issues, source gaps, style goal, and claims ChatGPT must not invent.
Done when: I have a compact ChatGPT evidence brief that can be pasted into ChatGPT without losing evidence control.
```

## ChatGPT Draft Intake Prompt

```text
Use $country-report-agent.

Goal: Verify and integrate a ChatGPT-written draft into the country-report manuscript.
Context: Country folder is [ISO3]. Target section is [section file]. The ChatGPT draft is pasted below or stored at [draft file].
Constraints: Treat the ChatGPT draft as unverified manuscript input, not as a source. Do not keep new facts, statistics, citations, references, laws, institutions, or dates unless they can be verified. Preserve useful narrative flow where it is consistent with the evidence trail.
Actions: Compare the draft with the existing section and available source records. Produce a ChatGPT draft intake audit, remove or mark unsupported enrichment, align APA citations, and update the canonical Markdown only after verification.
Done when: The integrated section keeps the richer prose but has verified claims, supported statistics, matched references, and no unsupported ChatGPT-generated content.
```

## Researcher Source Gap Prompt

```text
Use $country-report-agent.

Goal: Prepare a publication-readiness source-gap plan for [ISO3].
Context: Review chapters [3, 5, 7, 16, 17] and the existing source register.
Constraints: Prioritize official legal, administrative, fiscal, policy strategy, national statistics, and central bank sources. Use BTI, V-Dem, and QoG for comparative governance interpretation when relevant, but do not let them replace official country-specific sources. Do not use news as structural evidence. Mark unverifiable sources as needs_verification.
Actions: Inspect the relevant section files, source register, evidence plan, and quality audit outputs. Return a source gap table with priority and next action.
Done when: Each high-risk chapter has a clear list of missing or weak sources and recommended source targets.
```

## Table Of Contents And Country-Specific Issue Prompt

```text
Use $country-report-agent.

Goal: Design or audit the table of contents for [ISO3] so it preserves the standard country-report structure while adding the country-specific issues needed to understand the country.
Context: Country folder is [ISO3]. Inspect existing sources/sections, quality audits, source registers, and evidence plans if present.
Constraints: Keep the standard 1-19 chapter model for comparability. Do not create special sections just to make the report longer. Each special section must have a country-specific central claim, placement rationale, and source plan.
Actions: Identify structurally important country-specific issues, decide whether each needs a new section, renamed section, or paragraph, and recommend placement inside the relevant standard chapter.
Done when: I have a country-specific issue plan table, a revised table-of-contents recommendation, and a note on which issues must be synthesized in chapter 17.
```

## Statistical Evidence Prompt

```text
Use $country-report-agent.

Goal: Decide what statistics should be used in [section file] and prepare an evidence plan.
Context: Country folder is [ISO3]. The section's main question is [question].
Constraints: Use statistics only when they test or clarify a substantive claim. Prefer national official data for latest/granular claims and World Bank, IMF, UN, ILO, WHO, OECD, or regional development bank data for comparability. Record value, year, unit, source, indicator/table ID, and limitations.
Actions: Read the section and evidence plan. Propose indicators, sources, raw/processed file locations, charts, and prose interpretation.
Done when: I have a statistical evidence plan and know what data must be collected before writing.
```

## Comparative Governance Indicators Prompt

```text
Use $country-report-agent.

Goal: Decide whether BTI, V-Dem, QoG, or similar governance indicators should be used in [section file].
Context: Country folder is [ISO3]. The section's question is [question].
Constraints: Use these sources as diagnostic and comparative evidence, not as substitutes for official documents. Record dataset/report version, indicator name/code, year, scale direction, source URL, and methodological caveat. Explain what the indicator can and cannot show.
Actions: Identify relevant BTI, V-Dem, or QoG indicators/reports, propose how they support or qualify the section's argument, and flag source limits.
Done when: I have a short governance-indicator evidence plan and prose guidance that avoids overclaiming.
```

## Citation And Reference Audit Prompt

```text
Use $country-report-agent.

Goal: Audit APA in-text citations and the final References chapter for [ISO3].
Context: The manuscript is in [ISO3]/sources/sections/*.md. Final references should be in [ISO3]/sources/sections/19-01-references.md.
Constraints: Every in-text citation must match a real reference entry. Do not accept invented-looking sources. Verify DOI, official URL, local archived file, source note, or source register evidence where possible.
Actions: Run scripts/audit_citations.py if available, inspect suspicious cases manually, and return an APA citation audit table.
Done when: Missing references, uncited references, year mismatches, and unverifiable entries are listed with actions.
```

## Numeric Claim Audit Prompt

```text
Use $country-report-agent.

Goal: Find numerical claims that lack year, unit, or citation support.
Context: Country folder is [ISO3]. Focus on chapters [chapters or all].
Constraints: Do not change the manuscript yet. Treat script output as a first-pass heuristic that requires human judgment.
Actions: Run scripts/audit_numeric_claims.py if available. Review the flagged sentences and classify real problems versus false positives.
Done when: I have a numeric claim audit table and a prioritized repair list.
```

## Publication Gate Prompt

```text
Use $country-report-agent.

Goal: Decide whether [ISO3] is a structured first-pass, deep draft, or publication candidate.
Context: Inspect the country folder, sources/sections, source register, evidence plan, quality audits, figures, and report output.
Constraints: Pay special attention to chapters 3, 5, 7, 16, and 17. Check APA citation integrity, statistical claims, chart notes, official-source coverage, country-specific issue coverage, ChatGPT-assisted claims if any, template-like prose, and mechanical workflow language.
Actions: Run available citation and numeric audit scripts, inspect high-risk sections manually, and produce a quality gate summary.
Done when: The readiness label is justified, the top fixes are prioritized, and unresolved evidence risks are explicit.
```

## Instructor Exercise Prompt

```text
Use $country-report-agent.

Goal: Turn this country-report section into a classroom exercise.
Context: Country folder is [ISO3]. Target section is [section file]. Students have [time limit].
Constraints: The exercise should teach evidence tracing, not blind rewriting. Include what students should inspect, produce, and verify.
Actions: Create a short assignment, expected student outputs, rubric, and one model Codex prompt.
Done when: The exercise can be used directly in class.
```
