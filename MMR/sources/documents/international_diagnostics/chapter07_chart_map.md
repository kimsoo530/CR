# Chapter 7 Statistical Chart Map

| Chart ID | Indicator | Analytical question | Unit | Source / raw path | Processed path | Caveat |
|---|---|---|---|---|---|---|
| MMR-CH07-FISCAL-REV | `rev` | How has broad public revenue changed relative to GDP? | percent of GDP | IMF DataMapper / `MMR/raw/imf_enhanced/rev.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | General-government coverage; estimate status not preserved |
| MMR-CH07-FISCAL-BALANCE | `GGXCNL_NGDP` | Has the broad fiscal balance moved toward borrowing pressure? | percent of GDP | IMF DataMapper / `MMR/raw/imf_enhanced/GGXCNL_NGDP.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Negative values mean net borrowing; estimates may be present |
| MMR-CH07-FISCAL-DEBT | `GGXWDG_NGDP` | How has broad public debt changed? | percent of GDP | IMF DataMapper / `MMR/raw/imf_enhanced/GGXWDG_NGDP.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | General-government gross debt; not central-government debt |
| MMR-CH07-CENTRAL-REV | `GC.REV.XGRT.GD.ZS` | How broad was central-government revenue excluding grants? | percent of GDP | World Bank WDI / `MMR/raw/world_bank_enhanced/GC_REV_XGRT_GD_ZS.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Latest archived observation 2019 |
| MMR-CH07-CENTRAL-TAX | `GC.TAX.TOTL.GD.ZS` | How large was historical tax revenue? | percent of GDP | World Bank WDI / `MMR/raw/world_bank_enhanced/GC_TAX_TOTL_GD_ZS.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Latest archived observation 2019 |
| MMR-CH07-CENTRAL-EXP | `GC.XPN.TOTL.GD.ZS` | How did central-government expenses change? | percent of GDP | World Bank WDI / `MMR/raw/world_bank_enhanced/GC_XPN_TOTL_GD_ZS.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Latest archived observation 2019 |
| MMR-CH07-INTEREST | `GC.XPN.INTP.ZS` | How much expense was absorbed by interest? | percent of expense | World Bank WDI / `MMR/raw/world_bank_enhanced/GC_XPN_INTP_ZS.json` | `MMR/processed/fiscal_question_framework_diagnostics.csv` | Cannot be compared directly with IMF interest percent of GDP |
