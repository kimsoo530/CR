## 4.6 Political System Diagnostics and Democratic Trajectory

<!-- asean-comparative-lens-2026:start -->
**ASEAN comparative lens (2026).** Myanmar should be read in ASEAN comparison as ASEAN's most fragile contemporary state-capacity and conflict-governance case. It differs from the developmental trajectories of Vietnam, Thailand, Malaysia, and Indonesia because regime conflict, armed fragmentation, sanctions, and administrative breakdown dominate the policy environment. For this section, the regional comparison should explain how political authority differs from neighboring ASEAN cases in party organization, executive power, local mediation, civil-military influence, and informal power. Local comparable indicators show: population 54.50 million (2024), rank 5 among the nine ASEAN reports in this workspace; GDP US$74.07 billion (2024), rank 7 among the nine ASEAN reports in this workspace; GDP per capita US$1,359 (2024), rank 9 among the nine ASEAN reports in this workspace; real GDP growth -0.97% (2024), rank 9 among the nine ASEAN reports in this workspace; government effectiveness -1.23 (2023), rank 9 among the nine ASEAN reports in this workspace; internet use 45.45% (2020), rank 9 among the nine ASEAN reports in this workspace. Use `sources/documents/regional/asean_comparative_lens_2026.md` together with ASEANstats, ASEAN Secretariat materials, and the country processed-indicator files before making cross-ASEAN claims.
<!-- asean-comparative-lens-2026:end -->

| Dimension | Source table ID | Latest year | Latest value | Unit | Change since 2000 or earliest post-2000 value |
| Electoral democracy index | `v2x_polyarchy` | 2025 | 0.08 | 0-1 | -0.02 |
| Liberal democracy index | `v2x_libdem` | 2025 | 0.01 | 0-1 | -0.00 |
| Electoral integrity index | `v2x_electoral_integrity` | 2025 | 0.13 | 0-1 | -0.06 |
| Clean elections index | `v2xel_frefair` | 2025 | 0.00 | 0-1 | 0.00 |
| Party system institutionalization | `v2xps_party` | 2020 | 0.66 | 0-1 | -0.06 |
| Legislative constraints on the executive | `v2xlg_legcon` | 2022 | 0.29 | 0-1 | 0.26 |
| Judicial constraints on the executive | `v2x_jucon` | 2025 | 0.03 | 0-1 | -0.01 |
| Rule of law index | `v2xcl_rol` | 2025 | 0.09 | 0-1 | 0.00 |
| Political corruption index | `v2x_corr` | 2025 | 0.86 | 0-1, higher means more corruption | -0.02 |
| Public-sector corruption index | `v2x_pubcorr` | 2025 | 0.84 | 0-1, higher means more corruption | 0.06 |
| Regime of the World classification | `v2x_regime` | 2025 | 0.00 | 0 closed autocracy, 1 electoral autocracy, 2 electoral democracy, 3 liberal democracy | 0.00 |
| Voice and accountability | `VA.EST` | 2023 | -1.29 | WGI estimate | 2.18 |
| Political stability and absence of violence/terrorism | `PV.EST` | 2023 | -1.49 | WGI estimate | 1.36 |
| Rule of law | `RL.EST` | 2023 | -1.13 | WGI estimate | 1.30 |
| Control of corruption | `CC.EST` | 2023 | -0.85 | WGI estimate | 1.46 |

### Political-system trajectory in V-Dem indicators

  Source: V-Dem vdemdata, table IDs v2x_polyarchy, v2x_libdem, v2x_electoral_integrity, and v2x_jucon. Unit: index from 0 to 1. Processed file: MMR/processed/political_system_diagnostics.csv.

    document.addEventListener('DOMContentLoaded', function () {
      var el = document.getElementById('vdem-politics-mmr');
      if (!el || !window.Chart) return;
      new Chart(el, {
        type: 'line',
        data: { labels: [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], datasets: [{"label": "Electoral democracy", "data": [0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.097, 0.119, 0.223, 0.306, 0.355, 0.357, 0.37, 0.402, 0.402, 0.397, 0.421, 0.426, 0.102, 0.087, 0.077, 0.08, 0.08], "borderColor": "#0f6f87", "backgroundColor": "#0f6f87", "tension": 0.25, "spanGaps": true}, {"label": "Liberal democracy", "data": [0.017, 0.017, 0.017, 0.017, 0.018, 0.018, 0.018, 0.018, 0.018, 0.018, 0.018, 0.017, 0.018, 0.018, 0.033, 0.107, 0.134, 0.157, 0.163, 0.181, 0.226, 0.229, 0.232, 0.246, 0.252, 0.02, 0.016, 0.015, 0.015, 0.015], "borderColor": "#34675c", "backgroundColor": "#34675c", "tension": 0.25, "spanGaps": true}, {"label": "Electoral integrity", "data": [0.184, 0.184, 0.183, 0.183, 0.184, 0.184, 0.185, 0.19, 0.189, 0.189, 0.188, 0.192, 0.191, 0.195, 0.286, 0.486, 0.593, 0.611, 0.626, 0.683, 0.723, 0.728, 0.729, 0.746, 0.751, 0.273, 0.23, 0.191, 0.186, 0.126], "borderColor": "#7a5c00", "backgroundColor": "#7a5c00", "tension": 0.25, "spanGaps": true}, {"label": "Judicial constraints", "data": [0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.037, 0.08, 0.204, 0.235, 0.328, 0.328, 0.373, 0.48, 0.48, 0.484, 0.484, 0.506, 0.028, 0.024, 0.024, 0.025, 0.025], "borderColor": "#8a3b4a", "backgroundColor": "#8a3b4a", "tension": 0.25, "spanGaps": true}] },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { position: 'bottom' } },
          scales: {
            x: { title: { display: true, text: 'Year' } },
            y: { min: 0, max: 1, title: { display: true, text: 'V-Dem index (0-1)' } }
          }
        }
      });
    });

The political-governance indicators should be read as a profile of constraints, not as a democracy ranking. Voice and accountability is -1.29, political stability is -1.49, rule of law is -1.13, and control of corruption is -0.85. A country may hold regular elections but still show weak judicial constraints, low corruption control, or limited legislative oversight. Conversely, a centralized political order may score comparatively well on stability while still limiting electoral competition and accountability. The analytical task is to identify which part of the political system explains policy predictability, administrative discretion, reform credibility, and the risks faced by citizens, firms, courts, local governments, and opposition actors.

### Political accountability, stability, rule of law, and corruption control

  Source: World Bank Worldwide Governance Indicators table IDs VA.EST, PV.EST, RL.EST, and CC.EST. Unit: WGI estimate, approximately -2.5 to 2.5. Processed file: MMR/processed/political_system_diagnostics.csv.

    document.addEventListener('DOMContentLoaded', function () {
      var el = document.getElementById('wgi-politics-mmr');
      if (!el || !window.Chart) return;
      new Chart(el, {
        type: 'line',
        data: { labels: [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023], datasets: [{"label": "Voice and accountability", "data": [-3.69, -3.51, -3.14, -2.75, -2.48, -2.28, -2.07, -1.35, -1.47, -1.53, -1.46, -1.6, -2.82, -2.53, -1.29], "borderColor": "#0f6f87", "backgroundColor": "#0f6f87", "tension": 0.25, "spanGaps": true}, {"label": "Political stability", "data": [-2.2, -2.19, -1.89, -1.6, -1.94, -1.85, -1.98, -1.37, -1.84, -2.15, -2.26, -2.57, -3.54, -3.09, -1.49], "borderColor": "#34675c", "backgroundColor": "#34675c", "tension": 0.25, "spanGaps": true}, {"label": "Rule of law", "data": [-2.61, -2.64, -2.45, -2.31, -2.11, -2.03, -2.14, -1.53, -1.63, -1.77, -1.83, -2.03, -2.49, -2.14, -1.13], "borderColor": "#7a5c00", "backgroundColor": "#7a5c00", "tension": 0.25, "spanGaps": true}, {"label": "Control of corruption", "data": [-2.82, -2.84, -2.71, -1.82, -1.71, -1.5, -1.44, -1.08, -1.0, -1.04, -1.09, -1.15, -1.78, -1.61, -0.85], "borderColor": "#8a3b4a", "backgroundColor": "#8a3b4a", "tension": 0.25, "spanGaps": true}] },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { position: 'bottom' } },
          scales: {
            x: { title: { display: true, text: 'Year' } },
            y: { title: { display: true, text: 'WGI estimate (-2.5 to 2.5)' } }
          }
        }
      });
    });

Sources: V-Dem vdemdata table IDs `v2x_polyarchy`, `v2x_libdem`, `v2x_electoral_integrity`, `v2xel_frefair`, `v2xps_party`, `v2xlg_legcon`, `v2x_jucon`, `v2xcl_rol`, `v2x_corr`, `v2x_pubcorr`, and `v2x_regime`; World Bank WGI table IDs `VA.EST`, `PV.EST`, `RL.EST`, and `CC.EST`. Processed file: `MMR/processed/political_system_diagnostics.csv`; source note: `MMR/sources/documents/international_diagnostics/political_system_source_note.md`.
