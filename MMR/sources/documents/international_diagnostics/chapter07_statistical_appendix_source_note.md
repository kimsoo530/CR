# Chapter 7 Statistical Appendix Source Note

Access date: 2026-08-27.

This appendix run uses the existing `MMR/processed/fiscal_question_framework_diagnostics.csv` and the seven raw payloads listed in `MMR/raw/chapter07_statistical_appendix/statistical_metadata.csv`. It does not collect new external data and does not alter the existing raw files.

The existing processed data contain IMF DataMapper fiscal series and World Bank WDI fiscal series. IMF indicators use general-government coverage; World Bank indicators in this package use central-government coverage. They are therefore charted as separate indicators and are not added together or treated as one fiscal account.

The appendix run excludes IMF observations after 2024 because the archived payload does not preserve a reliable actual/estimate/projection flag. The 2024 IMF observations remain subject to the limitation that the local payload does not preserve that status field. The current reproducible run includes IMF `rev`, `GGXCNL_NGDP`, and `GGXWDG_NGDP`, plus World Bank `GC.REV.XGRT.GD.ZS`, `GC.TAX.TOTL.GD.ZS`, `GC.XPN.TOTL.GD.ZS`, and `GC.XPN.INTP.ZS`. IMF `exp` remains non-reproducible because the exact authoritative endpoint returned HTTP 403 during the focused recovery attempt. No national budget-execution series, SOE balance-sheet series, conflict-taxation series or actor-specific fiscal series were added.

The generator is `.agents/skills/country-report-agent/scripts/build_statistical_country_profile.py`. Its required inputs are `observations.csv`, `statistical_metadata.csv`, `manifest.json` with `validation_status=pass`, and a JSON configuration. Its outputs are a standalone statistical-profile Markdown file, standalone HTML, chart manifest, validation JSON, tooltip JavaScript and PNG/SVG figures.
