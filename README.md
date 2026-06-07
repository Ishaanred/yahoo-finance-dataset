# Yahoo Finance Company Dataset

A dataset of ~81,000 stock tickers scraped from Yahoo Finance, covering companies across 93 countries and all 11 GICS sectors. Useful for finance ML projects, sector analysis, company lookups, or building screeners.

## File

`yahoo_finance_output.csv` — 81,390 rows, 13 columns

## Columns

| Column | Description |
|---|---|
| `Ticker` | Stock ticker symbol |
| `CompanyName` | Full legal company name |
| `DisplayName` | Short display name |
| `Country` | Country of incorporation |
| `Website` | Company website URL |
| `Industry` | Granular industry classification |
| `Sector` | GICS sector |
| `BusinessSummary` | Long-form business description from Yahoo Finance |
| `FullTimeEmployees` | Employee headcount |
| `MarketCap` | Market capitalisation in local currency |
| `TotalRevenue` | Annual total revenue |
| `Currency` | Currency code for financial figures |
| `ExchangeName` | Exchange the ticker is listed on |

## Coverage

- **81,390** tickers total
- **35,898** rows with market cap data
- **33,345** rows with sector classification
- **93** countries
- **11** sectors: Basic Materials, Communication Services, Consumer Cyclical, Consumer Defensive, Energy, Financial Services, Healthcare, Industrials, Real Estate, Technology, Utilities

## Notes

- **Scraped on June 16, 2025** — data reflects a point-in-time snapshot, market caps and financials will be outdated
- Rows with `N/A` across most fields are tickers Yahoo Finance returned no data for (delisted, shell companies, etc.)
- Financial figures are in the currency listed in the `Currency` column, not normalised to USD

## Quick start

```python
import pandas as pd

df = pd.read_csv("yahoo_finance_output.csv")

# Drop empty rows
df = df[df["Sector"] != "N/A"]

# Filter by sector
tech = df[df["Sector"] == "Technology"]

# Sort by market cap
df["MarketCap"] = pd.to_numeric(df["MarketCap"], errors="coerce")
top_companies = df.sort_values("MarketCap", ascending=False).head(50)
```

## License

Data sourced from Yahoo Finance. This dataset is shared for educational and research purposes.
