# Statistical Analysis Protocol

Use this reference when country-report prose needs statistical evidence, when a section asks for charts or tables, or when the agent must collect, process, analyze, visualize, or cite statistics from international organizations, national agencies, or research institutes. For metadata fields and file naming, also read `reference_schemas.md`. For statistical evidence plans and chart plans, also read `output_templates.md`.

## Core Principle

Statistics are not decoration. Use them only when they help test, qualify, or explain a country-specific claim about institutions, state capacity, fiscal space, social pressure, development strategy, implementation, or policy risk.

## When To Use Statistics

Use statistical evidence when the section needs to:

- support a quantitative claim in the prose
- compare national official claims with observed outcomes
- show a trend, turning point, volatility, or structural break
- compare the country with peers, region, income group, or strategic comparators
- explain administrative, fiscal, demographic, economic, infrastructure, labor, education, health, financial, trade, climate, or governance constraints
- decide whether a chart or table would clarify an argument

Do not use statistics when the issue is primarily legal interpretation, institutional design, chronology, or political context unless a statistic directly sharpens the claim.

## Minimum Analytical Coverage

Before drafting a data-intensive section, identify which analytical dimensions the claim requires:

- **level**: current magnitude with year, unit, and source
- **trend**: change over a defensible period, including turning points when relevant
- **comparison**: justified peers, regions, income groups, targets, or earlier policy periods
- **distribution**: subnational, demographic, sectoral, organizational, or socioeconomic variation

For data-intensive sections, normally use at least two relevant dimensions. A single latest value is insufficient when the claim concerns change, relative performance, inequality, implementation variation, resilience, or policy effects. Record a reason when data availability makes the preferred design impossible.

Apply this as an analytical sufficiency rule rather than a quota. Legal, institutional-design, and historical sections may rely primarily on documentary evidence. Do not add irrelevant numbers to satisfy the audit.

For a new full report, map data-intensive sections before drafting and include national official data wherever latest, granular, or subnational claims are made. International datasets support comparability but do not replace national official statistics for those claims.

## Source Hierarchy

Use sources according to their analytical role:

1. **National official statistics**: statistical office, census bureau, finance ministry, central bank, sector ministries, open data portals. Use for latest-year, subnational, sector-specific, and official national claims.
2. **International comparable data**: World Bank WDI/WGI, IMF, UN Data, UN DESA, UNCTAD, ILOSTAT, WHO GHO, UNESCO, FAO, OECD, ADB, AfDB, regional development banks. Use for comparable long-run trends and peer benchmarking.
3. **Research-institute datasets**: V-Dem, QoG, BTI, Varieties of Democracy, governance or conflict datasets, think-tank indices. Use cautiously for diagnostic or theoretical interpretation, with method limits stated.
   - Use BTI for democracy, market economy, governance transformation, steering capability, and country-report narrative leads.
   - Use V-Dem for democratic institutions, civil liberties, electoral democracy, autocratization, and political-regime indicators.
   - Use QoG for corruption, quality of government, administrative capacity, public goods, and broad governance-related comparative indicators.
4. **Diagnostic reports**: World Bank, IMF Article IV, OECD, UN, development-bank, and reputable institutional diagnostics. Use to interpret what the numbers mean, not as a substitute for raw values.

If national official data and international estimates conflict, identify the difference and explain the likely reason: definition, coverage, revision, estimation method, fiscal year/calendar year, exchange rate, territory, or missing data.

## Collection Rules

- Prefer structured APIs, bulk downloads, official CSV/Excel tables, or documented PDF tables over manual copy-paste.
- Preserve original files under `[ISO3]/raw/` with source-specific subfolders.
- Save cleaned analytical datasets under `[ISO3]/processed/`.
- Record source metadata in `[ISO3]/sources/source_register.csv`, a source note, or the section evidence plan.
- Keep query parameters, indicator codes, table IDs, download dates, and access notes when available.
- Do not silently overwrite raw files from an earlier run. If replacing data, note the reason or keep a dated copy when useful.
- If a source blocks automated download, create an access note and flag the source for manual verification.

## Metadata Required

For each indicator or statistical table used in reader-facing prose, record:

- source institution
- dataset or publication title
- indicator/table ID or exact table name
- country code and country coverage
- unit and denominator
- frequency
- year range requested
- latest non-missing observation year
- original URL, API endpoint, DOI, or access note
- local raw file path
- local processed file path when derived
- whether values are official observations, international estimates, projections, or project-calculated ratios

## Processing Rules

- Keep raw and processed data separate.
- Convert data to tidy long format when possible: country, year, indicator_code, indicator_name, value, unit, source.
- Preserve missing values instead of inventing zeros.
- Do not interpolate, extrapolate, deflate, convert currency, or calculate ratios unless the method is explicitly documented.
- When calculating derived ratios, state numerator, denominator, formula, units, and processed file.
- Check for duplicated observations, inconsistent country names, mixed frequencies, and non-numeric flags.
- Use the latest non-missing observation, not simply the latest calendar year in the file.

## Analysis Rules

- Analyze trend and level together. A high current value may still be improving or deteriorating.
- Identify turning points when they matter for the institutional argument.
- Compare only like with like: same definition, unit, denominator, frequency, and country coverage.
- Use peer comparisons only when the peer group is analytically justified.
- Avoid ranking language unless the ranking source and coverage are clearly stated.
- Treat governance indices, perception indices, and model-based estimates as diagnostic signals, not direct measurements of administrative reality.
- For BTI, V-Dem, and QoG, record the exact dataset/report version, indicator name/code, year, scale direction, country coverage, and methodological caveat.
- State source limitations when a statistic is politically sensitive, estimated, lagged, survey-based, or incomplete.

## Visualization Rules

- Every chart must answer a section question.
- Do not mix incompatible units in one chart.
- Separate absolute values, percentages, ratios, index scores, counts, and monetary values.
- If a chart has five or more series, use small multiples, panels, or a carefully explained summary chart.
- Label axes with units.
- Include source institution, dataset, indicator/table ID, unit, country code, processed file, and latest non-missing year in chart notes.
- Show uncertainty or data gaps when they materially affect interpretation.
- Avoid charts for one-off values unless a table would be clearer.

## Prose Integration Rules

When inserting statistics into a section:

- state the exact value, year, unit, source, and indicator/table ID nearby
- explain why the statistic matters for institutions, policy implementation, fiscal space, social pressure, or state capacity
- interpret the trend or comparison, not only the latest value
- connect the statistic to the section's central thesis
- distinguish official targets, official outcomes, international estimates, and project calculations
- add a limitation sentence where definitions, lags, missing data, or political sensitivity matter

Good prose pattern:

```text
The statistic should not stand alone. It should show what the state can finance, administer, regulate, deliver, or sustain, and it should explain whether the observed trend supports or qualifies the official narrative.
```

## Common Data Families By Chapter

- Chapters 3, 4, 6, and 17: V-Dem, BTI, QoG, WGI, regime and governance diagnostics, democracy/autocratization indicators, audit and anti-corruption data
- Chapter 7: revenue, tax, expenditure, debt, deficit, interest burden, procurement, SOE risk, IMF fiscal tables
- Chapter 8: population, dependency, urbanization, migration, remittances, census, UN DESA
- Chapter 9: GDP, growth, inflation, productivity, sectoral value added, macro vulnerability
- Chapter 10: exports, imports, FDI, current account, partners, product concentration, UNCTAD and trade databases
- Chapter 11: electricity, energy mix, transport, logistics, internet, mobile, infrastructure access
- Chapter 12: labor force, informality, unemployment, youth, gender, skills, ILOSTAT
- Chapter 13: education, health, welfare, HDI, WHO, UNESCO, national service capacity
- Chapter 14: credit, banking, monetary indicators, inclusion, capital markets, financial regulation
- Chapter 16: development strategy indicators, SDGs, climate, digital transition, implementation milestones

## Governance Indicator Source Notes

- BTI: useful when the report needs a concise country-level narrative on transformation, governance steering capacity, democracy, and market economy. Pair BTI with official sources and academic literature before drawing strong conclusions.
- V-Dem: useful for long-run democracy and regime comparisons. State that many variables are expert-coded or index-based and avoid treating them as direct administrative measurements.
- QoG: useful for multi-source governance and social indicator comparison. Identify the original variable source when QoG compiles rather than originates a variable.

## Quality Checklist Before Delivery

- Were data-intensive sections identified before drafting?
- Does each data-intensive section use at least two relevant dimensions among level, trend, comparison, and distribution, or document why that is not possible?
- Are national official statistics used for latest, granular, and subnational claims where available?
- Does each numerical claim have value, year, unit, and source?
- Is the source role clear: national official, international comparable, research dataset, or diagnostic report?
- Are raw and processed files stored in the expected folders?
- Are source URLs, indicator IDs, and local paths recorded?
- Are mixed units avoided?
- Does each chart have a source footnote and prose interpretation?
- Are data gaps and estimation limits stated?
- Does the statistic strengthen the country-specific argument rather than decorate the report?
- For BTI, V-Dem, or QoG indicators, is the dataset/report version and indicator meaning clear?
- Were `scripts/audit_statistical_coverage.py` and `scripts/audit_visual_evidence.py` reviewed for a new full report or publication-readiness decision?

## Prohibited Shortcuts

- Do not use unsourced numbers from model memory.
- Do not cite a chart without preserving or documenting the underlying data.
- Do not treat official targets as achieved outcomes.
- Do not use international estimates as if they were national official statistics.
- Do not rank a country without naming the ranking source and comparator set.
- Do not hide conflicting values between sources.
- Do not add a chart whose unit, source, or interpretation cannot be explained.
