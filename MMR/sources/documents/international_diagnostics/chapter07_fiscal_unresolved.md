# Chapter 7 Fiscal Evidence: Unresolved Items

- No locally archived national annual budget, enacted appropriation, final account, budget-execution table or medium-term fiscal framework was verified in this batch.
- No current Myanmar official revenue, expenditure, deficit or debt series was verified against the IMF and World Bank indicators.
- The archived IMF DataMapper payload does not preserve actual/estimate/projection status. The appendix therefore stops at 2024 and labels the latest IMF observations as status-uncertain international data.
- The archived World Bank fiscal series end in 2019 and cannot establish current post-2021 fiscal performance.
- No verified SOE financial statements, consolidated public-sector balance sheet, resource-revenue register or contingent-liability report was located in the existing local archive.
- No verified military-budget series or conflict-taxation/revenue series was added to the candidate. International military-expenditure indicators must not be treated as Myanmar budget execution or as evidence of actor-specific fiscal flows.
- No current audit report, procurement dataset, audit-follow-up record or PFM assessment was locally verified for this batch.
- The relationship between post-2021 conflict, sanctions, foreign-exchange constraints and fiscal outcomes remains unresolved without a stronger dated diagnostic package.

## Statistical Metadata Reconciliation

The World Bank recovery succeeded for the three exact indicator IDs. The IMF `exp` recovery attempt returned HTTP 403 from the authoritative endpoint, so no raw payload was archived and no substitute was used:

| Indicator | Previously referenced path | Finding | Processed provenance | Chart status |
|---|---|---|---|---|
| `exp` | `MMR/raw/imf_enhanced/exp.json` | Exact IMF endpoint identified from local lineage, but recovery returned HTTP 403; raw source remains missing. | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Not reproducible; not publication-ready |
| `GC.TAX.TOTL.GD.ZS` | `MMR/raw/world_bank_enhanced/GC_TAX_TOTL_GD_ZS.json` | Exact World Bank WDI payload recovered and verified. | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Recovered and included |
| `GC.XPN.TOTL.GD.ZS` | `MMR/raw/world_bank_enhanced/GC_XPN_TOTL_GD_ZS.json` | Exact World Bank WDI payload recovered and verified; prior `GC_XPN_COMP_ZS.json` was not used. | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Recovered and included |
| `GC.XPN.INTP.ZS` | `MMR/raw/world_bank_enhanced/GC_XPN_INTP_ZS.json` | Exact World Bank WDI payload recovered and verified; prior `GC_XPN_INTP_RV_ZS.json` was not used. | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Recovered and included |
