## 5.4 Financial Administration, Procurement, Audit, and Inspection

<!-- asean-comparative-lens-2026:start -->
**ASEAN comparative lens (2026).** Myanmar should be read in ASEAN comparison as ASEAN's most fragile contemporary state-capacity and conflict-governance case. It differs from the developmental trajectories of Vietnam, Thailand, Malaysia, and Indonesia because regime conflict, armed fragmentation, sanctions, and administrative breakdown dominate the policy environment. For this section, the regional comparison should compare the administrative machinery with ASEAN peers by asking whether coordination relies on central ministries, local governments, party structures, federal bargains, or compact city-state capacity. Local comparable indicators show: population 54.50 million (2024), rank 5 among the nine ASEAN reports in this workspace; GDP US$74.07 billion (2024), rank 7 among the nine ASEAN reports in this workspace; GDP per capita US$1,359 (2024), rank 9 among the nine ASEAN reports in this workspace; real GDP growth -0.97% (2024), rank 9 among the nine ASEAN reports in this workspace; government effectiveness -1.23 (2023), rank 9 among the nine ASEAN reports in this workspace; internet use 45.45% (2020), rank 9 among the nine ASEAN reports in this workspace. Use `sources/documents/regional/asean_comparative_lens_2026.md` together with ASEANstats, ASEAN Secretariat materials, and the country processed-indicator files before making cross-ASEAN claims.
<!-- asean-comparative-lens-2026:end -->

Financial administration in Myanmar links political promises to authorized spending, contracts, payments, accounting, and audit. The latest comparable IMF value for the general-government balance is -4.9 percent of GDP in 2025, indicating a sizeable general-government deficit. The approximate five-year movement is 1.6 percentage points, so the fiscal trend must be read together with revenue capacity, expenditure pressure, interest burden, and the credibility of budget execution.

| Financial administration stage | Main institution or procedure | Administrative meaning |
| Executive budget preparation | The Ministry of Planning and Finance prepares the Union budget and fiscal administration under the military-led state administration. | Shows where fiscal priorities, ceilings, macro assumptions, and policy commitments enter the executive budget. |
| Legislative budget scrutiny | The elected parliamentary budget process has not operated normally since the 2021 coup; budget authorization is handled through executive-military structures. | Determines whether the budget is only approved formally or receives substantive parliamentary review. |
| Budget execution and treasury control | Treasury, finance ministry, spending ministries, and line-agency accounting systems execute appropriations and control commitments, payments, arrears, and cash management. | Connects policy promises to actual spending discipline. |
| Procurement and contract management | Procurement is governed through Union financial rules and sector contracting procedures, with transparency affected by conflict and sanctions. | Converts budget allocations into contracts and service inputs, making transparency and competition central to implementation capacity. |
| Final accounts, external audit, and inspection | The Office of the Auditor General of the Union is the formal external audit institution. | Checks whether expenditure was legal, regular, efficient, and reported to the legislature and public. |
| Fiscal indicator | Source table ID | Latest year | Latest value | Unit | Five-year change |
| General government net lending/borrowing | `GGXCNL_NGDP` | 2025 | -4.9 | % of GDP | 1.6 |
| General government primary net lending/borrowing | `GGXONLB_NGDP` | n/a | n/a | % of GDP | n/a |
| General government revenue | `rev` | 2024 | 15.6 | % of GDP | -0.2 |
| General government expenditure | `GGX_NGDP` | n/a | n/a | % of GDP | n/a |
| Interest payments | `GC.XPN.INTP.RV.ZS` | 2019 | 9.6 | % of revenue | 3.5 |

### General government fiscal balance trend

Source: IMF DataMapper table ID GGXCNL_NGDP, general government net lending/borrowing, percent of GDP. Processed file: MMR/processed/financial_administration_diagnostics.csv.

    document.addEventListener('DOMContentLoaded', function () {
      var el = document.getElementById('fiscal-balance-mmr');
      if (!el || !window.Chart) return;
      new Chart(el, {
        type: 'line',
        data: {
          labels: [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
          datasets: [{ label: 'General government net lending/borrowing (% of GDP)', data: [-4.8, -2.7, -1.5, -1.1, -4.3, -2.5, -3.4, -2.8, -4.7, -6.5, -2.2, -2.8, -2.8, -4.1, -4.9], borderColor: '#0f6f87', backgroundColor: 'rgba(15,111,135,.14)', tension: .25, fill: true }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { position: 'bottom' } },
          scales: {
            x: { title: { display: true, text: 'Year' } },
            y: { title: { display: true, text: 'Percent of GDP' } }
          }
        }
      });
    });
