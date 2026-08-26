## 5.6 Digital Government and Administrative Accountability

<!-- asean-comparative-lens-2026:start -->
**ASEAN comparative lens (2026).** Myanmar should be read in ASEAN comparison as ASEAN's most fragile contemporary state-capacity and conflict-governance case. It differs from the developmental trajectories of Vietnam, Thailand, Malaysia, and Indonesia because regime conflict, armed fragmentation, sanctions, and administrative breakdown dominate the policy environment. For this section, the regional comparison should compare the administrative machinery with ASEAN peers by asking whether coordination relies on central ministries, local governments, party structures, federal bargains, or compact city-state capacity. Local comparable indicators show: population 54.50 million (2024), rank 5 among the nine ASEAN reports in this workspace; GDP US$74.07 billion (2024), rank 7 among the nine ASEAN reports in this workspace; GDP per capita US$1,359 (2024), rank 9 among the nine ASEAN reports in this workspace; real GDP growth -0.97% (2024), rank 9 among the nine ASEAN reports in this workspace; government effectiveness -1.23 (2023), rank 9 among the nine ASEAN reports in this workspace; internet use 45.45% (2020), rank 9 among the nine ASEAN reports in this workspace. Use `sources/documents/regional/asean_comparative_lens_2026.md` together with ASEANstats, ASEAN Secretariat materials, and the country processed-indicator files before making cross-ASEAN claims.
<!-- asean-comparative-lens-2026:end -->

Digital government and administrative accountability in Myanmar depend on two conditions: citizens and firms must be able to reach the state digitally, and public organizations must be capable enough to process, protect, audit, and answer for digital transactions. The composite diagnostic places Myanmar in the constrained readiness band, with a score of 35.6 on a 0-100 scale. The latest comparable data show internet use at 45.4 percent of the population and mobile subscriptions at 114.3 per 100 people, while WGI government effectiveness is -1.2 and control of corruption is -0.9.

| Indicator | Source table ID | Latest year | Latest value | Unit | Five-year change | Normalized score |
| Internet users | `IT.NET.USER.ZS` | 2020 | 45.4 | % of population | 34.5 | 45.4 |
| Mobile cellular subscriptions | `IT.CEL.SETS.P2` | 2024 | 114.3 | per 100 people | -41.3 | 76.2 |
| Fixed broadband subscriptions | `IT.NET.BBND.P2` | 2024 | 2.9 | per 100 people | 1.9 | 7.2 |
| Secure internet servers | `IT.NET.SECR.P6` | 2024 | 23.6 | per 1 million people | 11.0 | 34.8 |
| Government effectiveness | `GE.EST` | 2023 | -1.2 | WGI estimate | 0.6 | 25.5 |
| Regulatory quality | `RQ.EST` | 2023 | -1.0 | WGI estimate | 0.3 | 29.9 |
| Control of corruption | `CC.EST` | 2023 | -0.9 | WGI estimate | 0.2 | 33.0 |
| General government revenue | `rev` | 2024 | 15.6 | % of GDP | -0.2 | 39.0 |

### Digital-government readiness profile

  Sources: World Bank Indicators API table IDs IT.NET.USER.ZS, IT.CEL.SETS.P2, IT.NET.BBND.P2, IT.NET.SECR.P6, GE.EST, RQ.EST, CC.EST; IMF DataMapper table ID rev. Scores are normalized to a 0-100 readiness scale. Processed file: MMR/processed/digital_government_readiness.csv.

    document.addEventListener('DOMContentLoaded', function () {
      var el = document.getElementById('digital-readiness-mmr');
      if (!el || !window.Chart) return;
      new Chart(el, {
        type: 'bar',
        data: {
          labels: ["Internet use", "Mobile", "Fixed broadband", "Secure servers", "Gov effectiveness", "Reg quality", "Corruption control", "Revenue capacity"],
          datasets: [{ label: 'Normalized readiness score (0-100)', data: [45.4, 76.2, 7.2, 34.8, 25.5, 29.9, 33.0, 39.0], backgroundColor: '#0f6f87' }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { autoSkip: false, maxRotation: 45, minRotation: 0 } },
            y: { min: 0, max: 100, title: { display: true, text: 'Readiness score (0-100)' } }
          }
        }
      });
    });

For Myanmar, the figure separates access infrastructure from institutional readiness. High internet or mobile penetration is not enough if ministries cannot share data, procurement is opaque, cybersecurity is weak, or citizens lack appeal channels when automated services fail. Conversely, a country with modest connectivity can still build credible digital administration when identity systems, treasury platforms, procurement portals, audit trails, complaint mechanisms, and privacy safeguards are linked to real administrative workflows. The readiness score is therefore best read as a diagnostic prompt for the digital-government section, not as a ranking: it identifies whether the binding constraint is connectivity, secure infrastructure, institutional quality, fiscal capacity, or administrative accountability.

Sources: World Bank Indicators API table IDs `IT.NET.USER.ZS`, `IT.CEL.SETS.P2`, `IT.NET.BBND.P2`, `IT.NET.SECR.P6`; Worldwide Governance Indicators table IDs `GE.EST`, `RQ.EST`, `CC.EST`; IMF DataMapper table ID `rev`. Raw files are stored under `MMR/raw/world_bank_digital` and `MMR/raw/imf_digital`; processed file is `MMR/processed/digital_government_readiness.csv`.
