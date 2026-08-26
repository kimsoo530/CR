# Reference Schemas

Use this reference when creating or repairing country-report source registers, APA reference registers, statistical metadata, or evidence plans.

## Core Principle

Registers are the traceability layer between manuscript claims, source files, datasets, charts, and final bibliography entries. They should be boring, explicit, and easy to audit.

## Source Register CSV

Preferred path:

```text
[ISO3]/sources/source_register.csv
```

Recommended columns:

| Column | Required | Purpose |
|---|---:|---|
| source_id | yes | Stable local ID, such as `WB-WDI-NY.GDP.MKTP.KD.ZG-2026-08-04` |
| source_type | yes | `official_law`, `government_report`, `national_statistics`, `international_dataset`, `research_dataset`, `governance_index`, `diagnostic_report`, `academic`, `book`, `news`, `other` |
| institution | yes | Issuing institution or publisher |
| author | conditional | Personal author when applicable |
| year | yes | Publication year, data release year, or `n.d.` |
| title | yes | Full title, dataset title, table title, or law title |
| series_or_number | no | Report number, law number, working paper number, table ID, or indicator ID |
| url | conditional | Official URL, DOI URL, dataset endpoint, or landing page |
| doi | no | DOI without invention or guesswork |
| local_path | conditional | Local archived file or source note path |
| accessed_date | conditional | Required for dynamic web data and database pulls |
| country_code | conditional | ISO3 or local country code when country-specific |
| country_coverage | conditional | National, subnational, disputed territory, comparator group, etc. |
| sections_used | yes | Comma-separated section IDs or chapter IDs |
| claim_supported | conditional | Short description of supported claim |
| verification_status | yes | `verified`, `partially_verified`, `needs_verification`, `rejected` |
| verification_method | yes | DOI, official URL, local file, source note, library catalog, etc. |
| notes | no | Caveats, blocked access, conflicting values, revision history |

Rules:

- Keep one row per source, dataset, or table that needs independent verification.
- Do not use a row as a dumping ground for several unrelated sources.
- Use stable source IDs in chart notes and evidence plans when possible.
- Preserve rejected or replaced sources only when they document an important audit decision.

## APA Reference Register JSON

Preferred path:

```text
[ISO3]/sources/apa_reference_register.json
```

Recommended shape:

```json
[
  {
    "reference_id": "world-bank-2024-wdi",
    "apa_author": "World Bank",
    "year": "2024",
    "title": "World Development Indicators",
    "reference_type": "statistical_dataset",
    "apa_entry": "World Bank. (2024). World Development Indicators. https://databank.worldbank.org/source/world-development-indicators",
    "doi": "",
    "url": "https://databank.worldbank.org/source/world-development-indicators",
    "accessed_date": "2026-08-04",
    "source_id": "WB-WDI",
    "local_path": "raw/world_bank/",
    "sections_cited": ["09-01", "17-02"],
    "verification_status": "verified",
    "verification_method": "official_url",
    "notes": ""
  }
]
```

Required fields:

- `reference_id`
- `apa_author`
- `year`
- `title`
- `reference_type`
- `apa_entry`
- `verification_status`

Recommended fields:

- `doi`
- `url`
- `accessed_date`
- `source_id`
- `local_path`
- `sections_cited`
- `verification_method`
- `notes`

Rules:

- Match `apa_author` and `year` to the in-text citation form.
- Keep `apa_entry` synchronized with `sources/sections/19-01-references.md`.
- Mark uncertain records as `needs_verification`; do not let them silently become final citations.

## Statistical Metadata CSV

Use a separate statistical metadata file when many indicators are used:

```text
[ISO3]/processed/statistical_metadata.csv
```

Recommended columns:

| Column | Required | Purpose |
|---|---:|---|
| indicator_id | yes | Stable local indicator ID |
| source_id | yes | Links to source register |
| institution | yes | World Bank, IMF, NSO, central bank, etc. |
| dataset | yes | Dataset name |
| indicator_code | conditional | Official code, table ID, or variable name |
| indicator_name | yes | Human-readable indicator name |
| unit | yes | Percent, current LCU, constant USD, index, count, etc. |
| frequency | yes | Annual, quarterly, monthly, irregular |
| country_code | yes | ISO3 or source-specific code |
| country_coverage | yes | National, subnational, disputed territory, etc. |
| year_start | conditional | First year requested or available |
| year_end | conditional | Last year requested or available |
| latest_non_missing_year | yes | Latest usable observation year |
| value_type | yes | `official_observation`, `international_estimate`, `projection`, `project_calculation` |
| raw_path | yes | Raw downloaded file or access note |
| processed_path | conditional | Cleaned file path |
| query_or_url | conditional | API query, source URL, or manual access note |
| downloaded_date | conditional | Required for dynamic data |
| transformation | conditional | Formula, deflator, ratio, aggregation, or cleaning method |
| limitation | conditional | Missing data, break in series, estimation issue, coverage limit |
| scale_direction | conditional | Required for index scores where higher/lower has substantive meaning |
| methodology_note | conditional | Expert-coded, perception-based, compiled variable, model estimate, official observation, etc. |

## Evidence Plan CSV

Preferred path:

```text
[ISO3]/sources/section_evidence_plan.csv
```

Recommended columns:

| Column | Required | Purpose |
|---|---:|---|
| section_id | yes | Section file prefix or chapter-section ID |
| central_claim | yes | One-sentence claim the evidence must support |
| evidence_need | yes | Official document, statistic, academic source, diagnostic, chart, etc. |
| source_id | conditional | Link to source register |
| reference_id | conditional | Link to APA register |
| indicator_id | conditional | Link to statistical metadata |
| chart_id | conditional | Link to figure or chart note |
| is_country_specific_issue | conditional | `yes` when the row supports a country-specific issue section |
| issue_category | conditional | Statehood, fiscal, administrative, demographic, geopolitical, infrastructure, development strategy, etc. |
| why_country_specific | conditional | Why the issue changes interpretation of this country |
| placement_rationale | conditional | Why this issue belongs in the selected chapter or section |
| linked_chapters | conditional | Other chapters that should connect to the issue, especially chapter 17 |
| status | yes | `missing`, `found`, `verified`, `used_in_prose`, `needs_revision` |
| priority | yes | `high`, `medium`, `low` |
| next_action | conditional | What the agent or human should do next |
| statistics_status | conditional | `required`, `provided`, or `not_applicable`; do not use prose comments as the sole exemption |
| statistics_exception_reason | conditional | Substantive reason statistics are not appropriate for this section |

Use the country-specific issue fields when following `country_specific_issue_protocol.md`. Do not mark routine section evidence as a special issue unless it affects the report's interpretation of the country.

## Verification Status Vocabulary

Use these status values consistently:

- `verified`: Source exists and key metadata match.
- `partially_verified`: Source likely exists but one important field is missing or uncertain.
- `needs_verification`: Source cannot yet be confirmed.
- `rejected`: Source was checked and should not be used.
- `superseded`: Source was replaced by a newer or better source.

## File Naming Guidance

Prefer stable, readable filenames:

```text
raw/world_bank/WDI_NY.GDP.MKTP.KD.ZG_2026-08-04.csv
raw/imf/WEO_NGDP_RPCH_2026-08-04.xlsx
raw/bti/BTI_country_report_[ISO3]_[year].pdf
raw/vdem/V-Dem_indicator_extract_[ISO3]_[date].csv
raw/qog/QoG_standard_extract_[ISO3]_[date].csv
raw/national_statistics/census_population_2024.pdf
processed/statistical_section_pipeline_long.csv
processed/statistical_metadata.csv
figures/07-02_revenue_trend.png
figures/17-01_governance_benchmark.svg
```

Do not overwrite raw files silently. If a newer pull replaces an older pull, keep the old file when it supports an audit trail or record the replacement in the source register.
