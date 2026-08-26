# Fiscal Question Framework Source Note: Myanmar

- Retrieval country code: `MMR`.
- World Bank WDI indicators: `GC.XPN.TOTL.GD.ZS, GC.REV.XGRT.GD.ZS, GC.TAX.TOTL.GD.ZS, GC.DOD.TOTL.GD.ZS, GC.XPN.INTP.ZS, MS.MIL.TOTL.TF.ZS, MS.MIL.XPND.GD.ZS, MS.MIL.XPND.ZS`.
- IMF DataMapper indicators: `rev, exp, GGXCNL_NGDP, GGXWDG_NGDP, GGXIP_NGDP`.
- IMF `GGXIP_NGDP` is used for public-debt interest paid as percent of GDP when available. If the API does not provide a country observation, use IMF Article IV tables or national fiscal reports.
- Coverage rule: IMF general-government indicators and World Bank central-government indicators are not mechanically identical. Treat them as complementary diagnostics and verify recent IMF observations against national budget execution documents, because some recent IMF values may be estimates or projections.
