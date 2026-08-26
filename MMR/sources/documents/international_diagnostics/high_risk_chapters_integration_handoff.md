# High-risk chapters canonical integration handoff

## Scope

Chapters 3, 5, 7, 15, 16, and 17 were integrated from their approved review candidates into the canonical Markdown section files. Generated HTML was not replaced in this batch.

## Integration record

- Chapter 3: constitutional order, military authority, emergency powers, competing post-2021 constitutional claims, and legal qualifications were integrated into `03-01` through `03-04`.
- Chapter 5: Union machinery, GAD, civil-service organization, formal territorial hierarchy, and post-2021 administrative fragmentation were integrated into `05-01`, `05-02`, `05-03`, `05-05`, and `05-07`. Existing sections without approved candidate coverage were preserved.
- Chapter 7: fiscal architecture, reproducible fiscal indicators, intergovernmental-finance limitations, SOE/resource gaps, and post-2021 fiscal qualifications were integrated into `07-01` through `07-05`. IMF `exp` remains excluded from publication-ready coverage.
- Chapter 15: formal foreign-relations architecture, representation versus recognition, ASEAN engagement, security actors, humanitarian definitions, and non-map territorial-reach qualifications were integrated into `15-01`, `15-02`, and `15-04`.
- Chapter 16: MSDP, MERP, FDC, implementation constraints, and strategy assessment were integrated into `16-01`, `16-02`, `16-03`, and `16-05`.
- Chapter 17: qualified cross-chapter operating-model, capacity, security/reach, external-environment, strategy-implementation, and evidence-limitation analysis were integrated into `17-01`, `17-02`, `17-03`, and `17-05`.

## Visuals

Only approved low-risk visuals were inserted. They are formal-structure diagrams, timelines, statistical charts with reproducible indicators, humanitarian/representation schematics, or qualitative synthesis diagrams. No territorial-control map, actor-control map, composite governance score, or IMF `exp` chart was inserted.

All inserted visual paths resolve to `MMR/figures/`. Captions retain source IDs, reference periods, and caveats. The Chapter 7 statistical figures use the final reproducible set: `rev`, `GGXCNL_NGDP`, `GGXWDG_NGDP`, `GC.REV.XGRT.GD.ZS`, `GC.TAX.TOTL.GD.ZS`, `GC.XPN.TOTL.GD.ZS`, and `GC.XPN.INTP.ZS`.

## References and qualifications

The canonical references section was extended with the verified legal, administrative, fiscal, diplomatic, humanitarian, and strategy sources used by the integrated chapters. The manuscript preserves distinctions among formal design, official actor claims, observed operation, contested interpretation, recognition, engagement, and unresolved evidence.

## Validation status

- Canonical Markdown: integrated for the approved high-risk chapter placements.
- Local visual existence: checked; inserted visual paths resolve.
- `exp`: excluded from Chapter 7 publication-ready prose and visuals.
- Build-workflow diagnosis: `MMR/code/build_report.py` and `MMR/code/fetch_data.py` are stubs referring to `tools/build_population_scope_reports.py`. That file and directory were not found under `C:\GDI`; the only relevant Git history is the initial commit. `MMR/code/serve_report.py` is an editor/server helper, not a full report builder. The published HTML tree is therefore not reproducibly rebuildable from the current repository.
- Pre-build checks: 25 expected high-risk canonical target files exist; all 20 approved visuals exist; no review-candidate links or duplicate canonical Markdown filenames were found; no `exp` figure or restored `exp` series appears in canonical Chapter 7; all inserted visual paths resolve locally.
- Generated HTML: not rebuilt because the established builder could not be recovered without inventing a build system.
- Automated Python audits: not rerun because no working Python interpreter is available in the current environment; `python` is absent and the Windows `py` launcher points to an unavailable packaged interpreter. Manual Markdown, citation-name, process-language, visual-path, duplicate, candidate-link, and `exp` checks were completed.

## Remaining review items

The report-wide audit baseline still contains pre-existing blockers and warnings, including short or generic sections outside the approved candidate placements and legacy ASEAN comparative-lens workflow text in untouched sections. These should be reviewed separately from the high-risk candidate integration. HTML rebuild and rendered-link validation remain pending restoration of the project builder/runtime.

## Recommended next step

Restore or identify the established report builder and Python runtime, rerun the full audit suite, repair any integration-specific citation or rendered-path findings, then perform one coordinated HTML rebuild and visual/rendered-link review. Do not reconstruct the builder from the existing HTML tree alone.
