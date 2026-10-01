"""Run the full analysis and build the dashboard.

    python build.py

Prints the key statistics and writes docs/index.html.
"""
import json
from pathlib import Path

from src import housing, markets

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "templates" / "dashboard_template.html"
OUTPUT = ROOT / "docs" / "index.html"


def main():
    m = markets.monthly_frame(start="1971-01")
    a = markets.annual_frame(m)
    markets.summary(m, a)

    h = housing.house_frame(start=1975)
    housing.summary(h)

    compact = lambda obj: json.dumps(obj, separators=(",", ":"))
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__DATA__", compact(markets.chart_data(m, a)))
    html = html.replace("__HOUSES__", compact(housing.chart_data(h)))
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Dashboard written to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
