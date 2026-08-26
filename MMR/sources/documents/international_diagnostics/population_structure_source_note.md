# Population Structure Source Note: Myanmar

This note records the demographic source tables used in section 8.1.

Source: World Bank World Development Indicators API.

Table IDs:

- `SP.POP.TOTL`: Population, total.
- `SP.POP.TOTL.MA.ZS`: Population, male (% of total population).
- `SP.POP.GROW`: Population growth (annual %).
- `SP.DYN.TFRT.IN`: Fertility rate, total (births per woman).
- `SP.POP.0014.TO.ZS`: Population ages 0-14 (% of total).
- `SP.POP.1564.TO.ZS`: Population ages 15-64 (% of total).
- `SP.POP.65UP.TO.ZS`: Population ages 65 and above (% of total).
- `SP.POP.DPND.YG`: Age dependency ratio, young (% of working-age population).
- `SP.POP.DPND.OL`: Age dependency ratio, old (% of working-age population).

Processed file: `MMR/processed/population_structure_diagnostics.csv`.

Annual update rule: replace or supplement WDI with the latest national statistics office census, population estimates, fertility releases, and demographic yearbooks when they provide newer official values.