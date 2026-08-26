# ChatGPT Draft Integration

Use this reference when a country-report section is drafted or enriched in ChatGPT and then brought back into Codex for verification, editing, citation alignment, and file integration.

## Core Principle

Use ChatGPT for rich narrative drafting and interpretive expansion. Use Codex for evidence control, file integration, citation/reference checks, statistical verification, reproducibility, and final publication readiness.

Treat a ChatGPT draft as an unverified manuscript input, not as a source. Do not accept factual claims, statistics, citations, or references from a ChatGPT draft unless they can be traced to verified sources in the country folder, source register, databases, official documents, or reliable external sources.

## Role Split

### Codex Should Prepare

- section goal and central question
- country-specific facts that must be preserved
- known institutions, laws, reforms, regions, conflicts, and policy episodes
- available sources and source gaps
- usable statistics and limitations
- required APA citation constraints
- banned claims, uncertain facts, or unresolved evidence risks

### ChatGPT May Draft

- richer explanatory prose
- historical or institutional narrative flow
- alternative interpretations
- smoother transitions
- country-specific issue framing
- chapter-level synthesis language
- reader-facing paragraph structure

### Codex Must Verify

- all factual claims against sources
- all numerical claims for value, year, unit, and source
- all APA in-text citations and final references
- whether references really exist
- whether country-specific institutions, laws, and reforms are accurate
- whether the section fits the standard chapter structure and special-issue placement
- whether the final Markdown remains compatible with the report build pipeline

## Recommended Workflow

1. **Codex evidence brief**: Prepare a short brief for the target section using local files, evidence plans, source registers, statistical metadata, and quality audits.
2. **ChatGPT drafting**: Ask ChatGPT to write book-like prose using only the brief and clearly marked source constraints.
3. **Draft return**: Paste or store the ChatGPT draft in the workspace as a draft input, not as final manuscript.
4. **Codex verification**: Compare each major claim, statistic, and citation against the source trail.
5. **Codex integration**: Rewrite or trim the draft to fit the section, preserve verified content, remove unsupported enrichment, and align citations.
6. **Quality gate**: Run citation and numeric audits when appropriate, then apply narrative style and country-specific issue checks.
7. **Build/update**: Update `sources/sections/*.md` and rebuild generated report artifacts when needed.

## Evidence Brief Template

Use this before sending work to ChatGPT:

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

## ChatGPT Drafting Prompt Shape

When asking ChatGPT to draft, include:

- the target country and section
- the section question
- verified evidence only
- source limitations
- required APA citation forms if known
- instruction not to invent citations, references, laws, figures, or institutions
- instruction to mark uncertain claims as `[needs verification]`
- instruction to write reader-facing prose, not an evidence table

Do not ask ChatGPT to "research" unless a separate source verification workflow will follow. If ChatGPT supplies new facts or references, treat them as leads for verification, not as usable evidence.

## Codex Intake Checklist

Before integrating a ChatGPT draft:

- Identify all new claims not present in the evidence brief.
- Extract all numerical claims and check year, unit, and source.
- Extract all citations and references.
- Mark unverifiable claims as `needs verification` or remove them from reader-facing prose.
- Compare the draft against the existing section to avoid losing verified country-specific material.
- Check whether the draft adds generic or overconfident claims.
- Keep useful narrative flow while replacing unsupported detail with verified evidence.

## Safe Integration Rules

- Never overwrite the canonical Markdown with a ChatGPT draft without review.
- Do not keep invented-looking citations or references.
- Do not keep numerical claims without a source trail.
- Do not let ChatGPT introduce new laws, agencies, programs, or dates unless verified.
- Preserve the user's existing verified content when it is more specific than the draft.
- Prefer cautious wording when evidence is incomplete.
- Keep workflow notes outside reader-facing prose.

## Best Use Cases

Use ChatGPT drafting especially for:

- chapter introductions and transitions
- synthesis paragraphs in chapter 17
- historically rich background sections
- country-specific issue framing
- turning evidence tables into natural prose
- reducing mechanical Codex-generated wording

Use Codex drafting directly when:

- the section is mainly technical source cleanup
- the task requires precise file edits
- citations, references, or data structures are fragile
- the user asks for a small scoped fix
- no verified evidence brief exists yet

## Quality Check

A ChatGPT-assisted section is not publication-ready until:

- the final text is in `sources/sections/*.md`
- all major claims have a source trail
- all numerical claims have value, year, unit, and source
- APA citations match final references
- unsupported enrichment has been removed or marked
- the prose passes narrative style checks
- the section still fits the report's table of contents and chapter role
