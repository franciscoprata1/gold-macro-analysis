"""Gold vs money supply, bond yields and the S&P 500 (questions 1-3)."""
import numpy as np
import pandas as pd

from .load import load_monthly, load_m2


def monthly_frame(start="1971-01", end=None):
    """One monthly table: gold, S&P 500, 10-year yield, CPI and derived columns."""
    m = load_monthly().loc[start:end].dropna()
    m["inflation"] = m.cpi.pct_change(12) * 100          # trailing 12-month CPI inflation, %
    m["real_yield"] = m.y10 - m.inflation                 # 10-year yield minus inflation
    m["spx_in_gold"] = m.spx / m.gold                     # ounces of gold per S&P 500 unit
    return m


def annual_frame(m):
    """January values each year, joined with M2 (published here as January values)."""
    jan = m[m.index.month == 1].copy()
    jan["year"] = jan.index.year
    return jan.merge(load_m2(), on="year").set_index("year")


def summary(m, a):
    """Print the statistics quoted on the dashboard."""
    growth = np.log(a[["gold", "m2", "cpi", "spx"]]).diff().dropna()
    print("Yearly growth correlations (January to January):")
    print(growth.corr().round(2), "\n")

    for w in (5, 10):
        g = np.log(a[["gold", "m2", "cpi"]]).diff(w).dropna()
        print(f"{w}-year growth correlation  gold~M2: {g.gold.corr(g.m2):.2f}   gold~CPI: {g.gold.corr(g.cpi):.2f}")

    first, last = a.index.min(), a.index.max()
    years = last - first
    print(f"\nCompound annual growth {first}-{last}:")
    for col, name in [("gold", "Gold"), ("spx", "S&P 500 (price)"), ("m2", "M2"), ("cpi", "CPI")]:
        mult = a[col].loc[last] / a[col].loc[first]
        print(f"  {name:16s} {(mult ** (1 / years) - 1) * 100:5.1f}% per year   x{mult:,.1f}")

    chg = pd.DataFrame({
        "gold": np.log(m.gold).diff(12),
        "real": m.real_yield.diff(12),
        "nominal": m.y10.diff(12),
    }).dropna()
    print(f"\n12-month change correlation  gold~real yield: {chg.gold.corr(chg.real):.2f}"
          f"   gold~nominal yield: {chg.gold.corr(chg.nominal):.2f}")

    r = np.log(m[["gold", "spx"]]).diff().dropna()
    print(f"Monthly return correlation gold~S&P 500: {r.gold.corr(r.spx):.2f}")
    print(f"S&P 500 in gold: max {m.spx_in_gold.max():.2f} oz ({m.spx_in_gold.idxmax():%b %Y}), "
          f"min {m.spx_in_gold.min():.2f} oz ({m.spx_in_gold.idxmin():%b %Y})\n")


def chart_data(m, a):
    """Series for the dashboard charts."""
    r = np.log(m[["gold", "spx"]]).diff()
    rolling = r.gold.rolling(36).corr(r.spx)
    clean = lambda s, d: [None if pd.isna(x) else round(float(x), d) for x in s]
    base = a.loc[a.index.min()]
    gold_m2 = a.gold / a.m2
    return {
        "monthly": {
            "dates": [d.strftime("%Y-%m") for d in m.index],
            "gold": clean(m.gold, 1),
            "spx": clean(m.spx, 1),
            "y10": clean(m.y10, 2),
            "real": clean(m.real_yield, 2),
            "spx_in_gold": clean(m.spx_in_gold, 3),
            "roll": clean(rolling, 3),
        },
        "annual": {
            "years": [int(y) for y in a.index],
            "gold": clean(a.gold / base.gold * 100, 1),
            "m2": clean(a.m2 / base.m2 * 100, 1),
            "cpi": clean(a.cpi / base.cpi * 100, 1),
            "spx": clean(a.spx / base.spx * 100, 1),
            "gold_m2": clean(gold_m2 / gold_m2.iloc[0] * 100, 1),
        },
    }
