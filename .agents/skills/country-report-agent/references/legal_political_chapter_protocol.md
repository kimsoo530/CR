# Legal and Political Chapter Protocol

Use this protocol when revising constitutional, electoral, judicial, federal, accountability, or democratic-diagnostic chapters.

## Start With A Section-Specific Research Question

Do not ask ChatGPT or a search engine for a generic country summary. For every section, define one governing question and request formal design, observed practice, a causal mechanism, a competing interpretation, disconfirming evidence, and a policy implication. Save the question-and-answer exchange under `sources/chatgpt_drafts/` as an unverified research memo. Never cite or silently paraphrase model output as evidence.

## Assign Every Source An Evidentiary Role

- Constitution, enacted statute, gazette, or certified judgment: what the law authorizes or requires.
- Official administrative or election record: what an institution recorded or implemented.
- Peer-reviewed scholarship: mechanism, interpretation, comparison, and limitations.
- International-observer or research-institute report: independently documented process evidence.
- Survey: sampled attitudes or experiences, not objective institutional performance.

Use at least one primary legal or official source and one analytical source for a high-risk legal claim. Read the operative provision or holding; do not rely on a news headline where the primary text is available.

## Separate Legal Status From Implementation

Classify an instrument as proposal, bill, assented act, regulation, pending case, or final judgment. Record its exact date and identifier. An enacted amendment changes formal authority; it does not prove budget release, compliance, capacity, or outcomes. A court judgment changes the governing rule; it does not prove universal execution. State the additional evidence needed to establish implementation.

## Audit Political Statistics Before Interpretation

For elections, never mix registered voters, accredited voters, ballots cast, valid votes, rejected ballots, or votes for the winner. Name the denominator and source beside every percentage. For legislative representation, distinguish seats prescribed, seats filled immediately after election, and current membership. For surveys, report fieldwork year, sample meaning, wording, and uncertainty where available.

For composite indices such as WGI or expert-coded series such as V-Dem, archive the edition and raw source, confirm theoretical range and direction, and retain the transformation script. Quarantine a processed series if it has implausible values, missing provenance, an unidentified version, or an unreproducible transformation. Do not repair suspicious values by hand or substitute a convenient online number without rebuilding lineage.

## Match Evidence To The Causal Claim

Use legal text to establish authority, not effect. Use turnout to diagnose participation, not election integrity by itself. Use women's seat share for descriptive representation, not substantive policy influence. Use corruption perceptions for legitimacy pressure, not incidence or monetary loss. State at least one credible competing interpretation.

For historical political-order sections, separate four outcomes that are often collapsed: uninterrupted civilian succession, opposition alternation, party-system institutionalization, and liberal-democratic constraint. Identify the institution that carries a historical legacy into current practice. Where federalism is part of the mechanism, examine both whether subnational office preserves opposition organization and whether it entrenches localized elite control. A turnout series must identify election type and denominator; mixed parliamentary and presidential observations may illustrate a broad trajectory only with an explicit comparability warning.

For executive-power and government-formation sections, do not infer delivery from formal presidential authority. Trace the chain from legal power through electoral coalition, territorial appointment rules, legislative confirmation, portfolio assignment, cabinet coordination, finance, subnational execution, and observable result. Evaluate representativeness, expertise, party support, and performance as distinct dimensions. A nomination deadline establishes speed, not screening quality; a cabinet appointment establishes officeholding, not policy delivery; an intergovernmental council's advice is not binding execution. When using elite-career data, state the unit, period, sample boundary, and why career experience is not itself a performance measure. Remove security, election-administration, or public-management detail that belongs in another section unless it directly tests the government-formation mechanism.

For parliament-party-election sections, trace representation as a chain from party access and candidate nomination through accreditation, voting, result publication, seat conversion, and legislative activity. Diagnose where the pool narrows instead of attributing the final seat pattern only to voter choice. Separate prescribed seats, seats filled at the election snapshot, and current membership; separate candidate shares from elected shares. Treat party count as formal supply, not proof of programmatic or equally viable choice. When examining election technology, distinguish each tool's legal purpose, operational dependency, paper-record relationship, and documented implementation. Do not use evidence from a presidential result process as if it were a legislative turnout or seat statistic. Evaluate parliament with bill content, disposition, implementation, committee work, and oversight records rather than bill counts alone. Qualitative interview reports can identify a plausible mechanism, but cannot estimate prevalence unless the sample supports that inference.

## Derive Implementable Implications

Avoid generic calls for stronger institutions. Identify the responsible institution, legal or administrative instrument, required data, implementation sequence, and observable success measure. For reforms involving federal and subnational tiers, specify authority, finance, audit, coordination, and dispute resolution together.

## Preserve Section Identity In The Build

Canonical headings must begin `## X.Y Title`. The chapter manifest, source filename, navigation label, chapter heading, and individual section page must refer to the same title. After building, verify both the chapter page and at least one individual section page. A source-only number is insufficient if the generator strips it.

## Final Quality Gate

Reject the section if any of the following remains:

- a proposed reform is described as current law;
- a judgment is described as completed implementation;
- a percentage has an unnamed or inconsistent denominator;
- a perception measure is treated as an objective performance rate;
- an index lacks versioned raw provenance or contains implausible values;
- the policy implication does not follow from the diagnosed mechanism;
- every section uses the same mechanical sequence of subheadings;
- the generated page drops or duplicates the `X.Y` number.
