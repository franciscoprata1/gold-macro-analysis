# Gold, Stocks, Bonds and Housing (1971–2026)

A data analysis of how gold has behaved against the US money supply, bond yields, the S&P 500 and house prices in the US, UK, Spain and the euro area, using 55 years of monthly data.

**Live dashboard:** `https://<your-username>.github.io/gold-macro-analysis/`

## Questions

1. **Does money printing drive the gold price?**
   Over decades, partly. Gold grew 9.2% a year since 1971, against 6.7% for the M2 money supply and 3.9% for consumer prices. Year to year, gold and M2 growth are uncorrelated (−0.01). From 1980 to 2001, M2 more than tripled while gold lost 61%.
2. **How does gold relate to bond yields?**
   Through real yields (the 10-year rate minus inflation). The correlation of 12-month changes is −0.43 for real yields and 0.06 for nominal yields. The link has weakened since 2022.
3. **Do gold and the S&P 500 move together?**
   No. Monthly returns have zero correlation over the full period. The S&P 500 cost 5.4 oz of gold at its peak in 2000 and 0.16 oz at its low in 1980.
4. **What does a house cost in gold, and in stocks?**
   In money, house prices rose 11× (US) to 50× (Spain) since 1975. In gold, a house is cheaper today than in 1975 in every region, but its gold price swung more than sixfold along the way.

| Typical house, oz of gold | 1975 | 1980 | 1990 | 2000 | 2010 | 2020 | 2026 |
|---|---|---|---|---|---|---|---|
| United States | 216 | 94 | 302 | 582 | 199 | 211 | 86 |
| United Kingdom | 115 | 60 | 219 | 456 | 222 | 178 | 76 |
| Spain | 62 | 33 | 139 | 204 | 164 | 86 | 46 |

## How to run

Requires Python 3.9 or newer.

```bash
git clone https://github.com/<your-username>/gold-macro-analysis.git
cd gold-macro-analysis
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python build.py
```

`build.py` prints the statistics above and writes the dashboard to `docs/index.html`. Open that file in a browser to view it (an internet connection is needed to load the charting library).

## Project structure

```
gold-macro-analysis/
├── build.py                  # runs the analysis and builds the dashboard
├── requirements.txt
├── data/                     # raw input data (CSV)
├── src/
│   ├── load.py               # reads the CSV files
│   ├── markets.py            # questions 1–3: M2, yields, S&P 500
│   └── housing.py            # question 4: house prices in gold and stocks
├── templates/
│   └── dashboard_template.html
└── docs/
    └── index.html            # the built dashboard (served by GitHub Pages)
```

## Data sources

| File | Content | Source |
|---|---|---|
| `gold_monthly_usd.csv` | Gold, USD per troy ounce, monthly average | [datasets/gold-prices](https://github.com/datasets/gold-prices) |
| `sp500_monthly.csv` | S&P 500 price index | [datasets/s-and-p-500](https://github.com/datasets/s-and-p-500) (Robert Shiller) |
| `us_10y_yield_monthly.csv` | US 10-year Treasury yield | [datasets/bond-yields-us-10y](https://github.com/datasets/bond-yields-us-10y) |
| `cpi_us_monthly.csv` | US CPI-U | [datasets/cpi-us](https://github.com/datasets/cpi-us) (BLS) |
| `m2_january.csv` | US M2 money stock, January of each year | [FRED M2SL](https://fred.stlouisfed.org/series/M2SL) |
| `house_prices_q1.csv` | US median new-house price; BIS property price indexes for the UK, Spain and euro area | [FRED MSPUS](https://fred.stlouisfed.org/series/MSPUS), [BIS via FRED](https://fred.stlouisfed.org/series/QGBN628BIS) |
| `fx_january.csv` | GBP, EUR, peseta and Deutsche Mark against USD | [FRED exchange rates](https://fred.stlouisfed.org/categories/94) |

## Method and limitations

- Correlations use log returns. Correlation shows co-movement, not cause.
- Real yield = 10-year yield minus trailing 12-month CPI inflation.
- The S&P 500 series is the price index and excludes dividends, which would add roughly 2–3 percentage points a year.
- **US house prices** are the Census median price of *new* houses sold.
- **UK house prices** take the HM Land Registry average of £268,000 (January 2026) back in time with the BIS index.
- **Spanish house prices** assume a 90 m² home at the notaries' January 2026 average of €2,065/m² (about €186,000), taken back with the BIS index. Pesetas are converted at the fixed rate of 166.386 per euro.
- **Euro area** has no official average house price, so it is shown only as an index. Before 1999 the Deutsche Mark stands in for the euro.
- Early UK and Spanish price levels are estimates and may be off by around 20%; the trends are reliable.

## Author

[Your Name] · Biomedical engineer interested in data analysis and visualization.
