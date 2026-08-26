# International Statistics Toolkit

Use this reference with `statistical_analysis_protocol.md` when converting the GDI Colab toolkit into reproducible evidence for a country study.

## What Was Retained From The Colab Notebook

The notebook's strongest reusable components are World Bank Indicators/WGI, IMF, WHO GHO, UNDP HDR time series, and WhoGov leadership/cabinet data. The pipeline now also has adapters for ILOSTAT, UN DESA World Population Prospects, and UNCTAD table-specific bulk archives. It standardizes these sources to one long schema and creates versioned raw files, processed data, metadata, derived series, peer benchmarks, and PNG/SVG charts. WITS and QoG examples in the notebook rely on experimental API calls or separately hosted files; add them only after the exact dataset version, license, download URL, and variable definitions have been verified.

## Run

Copy `international_statistics_example.json`, then change the country, justified peers, indicators, units, periods, dimensions, and value type.
Use `world_bank_indicator_catalog.csv` to discover curated World Bank codes, but confirm the live API metadata. Use `multi_source_statistics_example.json` for IMF WEO, ILOSTAT, WPP, UNCTAD, derived-series, and peer-benchmark syntax.

Install the small runtime dependency set once in the project environment:

```powershell
python -m pip install -r .agents/skills/country-report-agent/references/requirements-international-statistics.txt
```

```powershell
python .agents/skills/country-report-agent/scripts/international_statistics_pipeline.py `
  --config .agents/skills/country-report-agent/references/international_statistics_example.json `
  --country-root NGA
```

For leadership experience, cabinet size, minister age, and retention, use the separate WhoGov example:

```powershell
python .agents/skills/country-report-agent/scripts/international_statistics_pipeline.py `
  --config .agents/skills/country-report-agent/references/whogov_example.json `
  --country-root UZB
```

The WhoGov example also calculates women's shares from female and total counts and includes average tenure and core-cabinet measures. Never substitute a female count for a percentage.

For the multi-source example:

```powershell
python .agents/skills/country-report-agent/scripts/international_statistics_pipeline.py `
  --config .agents/skills/country-report-agent/references/multi_source_statistics_example.json `
  --country-root NGA
```

The command creates immutable run folders:

```text
[ISO3]/raw/international_statistics/[RUN_ID]/
[ISO3]/processed/international_statistics/[RUN_ID]/
  observations.csv
  statistical_metadata.csv
  manifest.json
  figures/*.png
  figures/*.svg
```

Use `--run-id` only when a meaningful version name is needed. The command refuses to overwrite an existing run.
If one provider rejects an automated request, the other successful sources are retained and `manifest.json` marks the run `review` with the exact fetch error. Do not cite a failed source; retry later or preserve an official bulk download with an access note.

## Build A Statistical Country Profile Appendix

After a pipeline run has `validation_status=pass`, use `build_statistical_country_profile.py` to turn indicators into a categorized, reader-facing appendix. Copy and edit `statistical_country_profile_example.json`; the country, peers, categories, analytical questions, and chart families are research decisions. Set `auto_include_unlisted` to `true` when every indicator in the validated run should be charted. Use `coverage_catalog` to record the full variable universe from a source notebook or data inventory, including items that require a new adapter, national administrative data, or a derived analysis. A notebook heading is not automatically a comparable variable.

```powershell
python .agents/skills/country-report-agent/scripts/build_statistical_country_profile.py `
  --run-dir NGA/processed/international_statistics/[RUN_ID] `
  --config .agents/skills/country-report-agent/references/statistical_country_profile_example.json `
  --output-dir NGA/report/statistical-country-profile
```

The example coverage catalog is `references/colab_statistical_visualization_catalog.csv`. Its statuses deliberately distinguish `available_current_run`, `adapter_ready_not_in_run`, `adapter_needed`, `national_data_required`, `derived_analysis`, `target_data_unavailable`, and `non_variable`. Do not show a fabricated empty chart for an unavailable item and do not silently substitute a Korea-only KOSIS series for another country's national statistic. Automatic inclusion charts only indicators with at least one focal-country observation. The validation output must report all input indicators, focal-country-available indicators, visualized indicators, target-missing indicators, and any unexplained omissions; `omitted_input_indicators` must be empty.

The output contains a standalone responsive `index.html`, editable Markdown, PNG/SVG figures, summary statistics, a chart manifest, and `validation.json`. The generator supports trend, latest-value comparison, and start-to-end change charts. It automatically falls back from an underpowered trend to a latest-value comparison when no series has at least eight time points. Latest-value charts label the observation year because source coverage can differ by country.

Organize the appendix by analytical type rather than data provider. A useful default is demography, macroeconomy, labor, human development and digital access, external structure, and governance/executive organization. Do not combine incompatible units, treat WEO projections as observed outcomes, interpret a WGI estimate as direct performance, or read cabinet tenure as expertise. The generated prose is a descriptive evidence summary and still requires country-specific interpretation before publication.

Multi-country trend figures must distinguish countries with both color and line style. Use a thick solid focal-country series and stable peer-specific color/dash combinations so the comparison remains legible in color, grayscale, and common forms of color-vision deficiency.

The HTML appendix adds self-hosted pointer tooltips without replacing the static PNG/SVG exports. Trend-chart hover reports all available country values for the nearest year; bar-chart hover reports the corresponding country, period, value, and unit. Keep `chart-tooltips.js` beside `index.html` during publication and verify that the static figure remains readable if scripting is blocked.

## Required Research Decisions

Before running, state the section claim and decide:

1. Why each indicator measures or qualifies that claim.
2. Why the comparison countries are theoretically or institutionally relevant.
3. Whether the requested period captures the policy regime, shock, or turning point.
4. Whether the unit and denominator are genuinely comparable.
5. Whether national official data are also needed for the latest or subnational claim.

Do not treat an API call as analysis. After the run, inspect missing years, breaks, revisions, projection boundaries, and conflicts with national statistics. Then write the institutional mechanism and policy implication in prose.

## Source-Specific Cautions

- **World Bank**: use API v2 and preserve the source ID. WDI and WGI codes can share the API but have different measurement meanings. Governance estimates are diagnostic, not direct measures of administrative performance.
- **IMF**: prefer `source=imf_weo`, which uses the official IMF SDMX 3.0 WEO bulk CSV. If the IMF download edge rejects the request, download the official WEO CSV/XLSX manually and set `local_file`; the parser does not depend on an unofficial mirror. DataMapper remains available as `source=imf`. Record the WEO vintage and identify each country's latest actual year before citing estimates or projections.
- **ILOSTAT**: specify the indicator and exact `sex`, age/classification, and—where necessary—source dimensions. The adapter refuses unresolved duplicate country-year rows. Distinguish ILO modelled estimates from national-source observations.
- **UN DESA WPP**: set `value_column` to an official WPP 2024 field and preserve the `Variant`. Population-count columns are generally in thousands; confirm the data dictionary. Label the estimate/projection boundary in prose and figures.
- **UNCTAD**: use an official table-specific bulk endpoint and explicit `value_column` and dimension `filters`. The adapter archives the original 7z file and refuses duplicate country-year rows. Preserve table ID, flow, partner/product coverage, flags, and footnotes.
- **WHO**: the Colab notebook uses the legacy GHO OData endpoint. WHO announced migration to a new interface. Verify the current endpoint, indicator definition, and all disaggregation dimensions before publication. The pipeline rejects duplicate country-year rows instead of averaging incompatible observations.
- **UNDP**: preserve the downloaded HDR vintage. Compare countries within one vintage because historical HDI values can be revised for comparability.
- **WhoGov**: use the official versioned cross-sectional file, not the notebook's opaque Drive copy. Use `whogov_indicator_catalog.csv`. Distinguish continuous from total leader experience; cabinet ministers from all or core government positions; raw from cabinet-expansion-adjusted retention; and personnel continuity from policy or administrative performance. Calculate women's shares only from matching female and total counts. Average tenure is composition-dependent and is not itself a measure of expertise. Age statistics require attention to `age_share`, the share with coded age.
  Inspect the first and last observation for every country. State formation, independence, dissolution, mid-year leadership change, and incomplete update years can produce partial or non-comparable annual snapshots. For the Kazakhstan-Uzbekistan example, begin in 1992 rather than treating the partial 1991 observation as a full cabinet year.
- **WITS/QoG**: do not reuse opaque Drive file IDs as authoritative sources. Download a documented release from the originating institution, preserve the file, and register the version and variables.

## Derived Indicators And Peer Benchmarks

Put calculations in top-level `derived_indicators` and comparisons in `benchmarks`; do not hand-edit their output.

Supported derived operations are `ratio`, `difference`, `sum`, `percent_change`, and `index_base`. Ratio specifications require `numerator`, `denominator`, and an explicit `scale`; base indexes require `input_indicator` and `base_year`. Calculations use matching non-missing country-years, reject ambiguous duplicate inputs, and omit zero-denominator ratios.

Benchmarks require `target_country`, an explicit `peer_countries` list, `statistic` (`mean` or `median`), and `min_peers`. Justify peers by the section's comparison logic—region, income, state structure, resource dependence, administrative tradition, or a specified counterfactual—not by data availability alone. Report sensitivity to an alternative defensible peer set when a policy conclusion depends on the benchmark. A peer average is descriptive unless the research design establishes a causal comparison.

## Adding A New Source Adapter

A new adapter must return tidy observations with country code/name, year, and value plus the original payload, endpoint, dataset title, and limitations. It must not aggregate duplicate observations, interpolate missing values, or convert units silently. Add a mocked or fixture-based test before using the adapter in a published study.
