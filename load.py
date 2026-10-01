"""Read the raw CSV files in data/."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"


def _series(file, column, name):
    df = pd.read_csv(DATA / file)
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")[column].rename(name)


def load_monthly():
    """Gold (USD/oz), S&P 500, US 10-year yield (%) and US CPI, one row per month."""
    return pd.concat([
        _series("gold_monthly_usd.csv", "Price", "gold"),
        _series("sp500_monthly.csv", "SP500", "spx"),
        _series("us_10y_yield_monthly.csv", "Rate", "y10"),
        _series("cpi_us_monthly.csv", "Index", "cpi"),
    ], axis=1)


def load_m2():
    """US M2 money stock, billions of USD, January of each year."""
    return pd.read_csv(DATA / "m2_january.csv")


def load_houses():
    """US median new-house price and BIS price indexes (2010 = 100), Q1 of each year."""
    return pd.read_csv(DATA / "house_prices_q1.csv").set_index("year")


def load_fx():
    """January spot exchange rates."""
    return pd.read_csv(DATA / "fx_january.csv").set_index("year")


def january(series):
    """January value of a monthly series, indexed by year."""
    s = series[series.index.month == 1]
    return pd.Series(s.values, index=s.index.year)
