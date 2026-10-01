"""House prices measured in gold and in S&P 500 units (question 4).

US: Census median price of new houses sold, used directly.
UK, Spain: a 2026 price level is taken back in time with the BIS index.
Euro area: no official average price exists, so it is shown only as an index.
"""
import pandas as pd

from .load import load_fx, load_houses, load_monthly, january

UK_ANCHOR_GBP = 268_000          # HM Land Registry UK average price, January 2026
ES_ANCHOR_EUR = 2_065 * 90       # Notaries' average €/m², January 2026, x a 90 m² home
ANCHOR_YEAR = 2026
PESETAS_PER_EUR = 166.386        # fixed conversion rate
DEM_PER_EUR = 1.95583            # Deutsche Mark stands in for the euro before 1999

COUNTRIES = ["us", "uk", "es", "ea"]


def house_frame(start=1975, end=ANCHOR_YEAR):
    h, fx, m = load_houses(), load_fx(), load_monthly()
    gold, spx = january(m.gold.dropna()), january(m.spx.dropna())

    rows = []
    for y in range(start, end + 1):
        usd_per_eur = fx.usd_per_eur[y] if y >= 1999 else DEM_PER_EUR / fx.dem_per_usd[y]
        uk_gbp = UK_ANCHOR_GBP * h.uk_bis_index[y] / h.uk_bis_index[ANCHOR_YEAR]
        es_eur = ES_ANCHOR_EUR * h.spain_bis_index[y] / h.spain_bis_index[ANCHOR_YEAR]
        es_usd = es_eur * (fx.usd_per_eur[y] if y >= 1999 else PESETAS_PER_EUR / fx.esp_per_usd[y])
        prices_usd = {
            "us": h.us_median_new_house_usd[y],
            "uk": uk_gbp * fx.usd_per_gbp[y],
            "es": es_usd,
            "ea": h.euro_area_bis_index[y] * usd_per_eur,   # relative only, no price level
        }
        row = {"year": y, "gold": gold[y], "spx": spx[y], "uk_gbp": uk_gbp, "es_eur": es_eur}
        for c, p in prices_usd.items():
            row[c + "_oz"] = p / gold[y]        # ounces of gold per house
            row[c + "_sp"] = p / spx[y]         # S&P 500 units per house
        rows.append(row)

    d = pd.DataFrame(rows).set_index("year")
    for c in COUNTRIES:
        d[c + "_oz_i"] = d[c + "_oz"] / d[c + "_oz"].iloc[0] * 100
        d[c + "_sp_i"] = d[c + "_sp"] / d[c + "_sp"].iloc[0] * 100
    return d


def summary(d):
    pd.set_option("display.width", 200)
    years = [y for y in (1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2026) if y in d.index]
    print("A typical house, in ounces of gold (euro area as index, first year = 100):")
    print(d.loc[years, ["us_oz", "uk_oz", "es_oz", "ea_oz_i"]].round(0).astype(int)
          .rename(columns={"us_oz": "US", "uk_oz": "UK", "es_oz": "Spain", "ea_oz_i": "Euro area idx"}), "\n")
    print("A typical house, in S&P 500 units:")
    print(d.loc[years, ["us_sp", "uk_sp", "es_sp"]].round(0).astype(int)
          .rename(columns={"us_sp": "US", "uk_sp": "UK", "es_sp": "Spain"}), "\n")
    last = d.index.max()
    gold_wins = [y for y in d.index[:-1] if d.us_oz[y] / d.us_oz[last] > d.us_sp[y] / d.us_sp[last]]
    print(f"Start years where holding gold bought more house by {last} than the S&P 500: {gold_wins}\n")


def chart_data(d):
    keep = ["gold", "spx"] + [f"{c}{s}" for c in ("us", "uk", "es") for s in ("_oz", "_sp", "_oz_i")] + ["ea_oz_i"]
    out = {k: [round(float(v), 3) for v in d[k]] for k in keep}
    out["years"] = [int(y) for y in d.index]
    return out
