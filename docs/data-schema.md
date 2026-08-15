# Data Schema

## Grain

One row represents one stock's trading data for one trading day

## Table: `stock_prices`

| Column | Type | Nullable | Description |
|---|---|---|---|
| `ticker` | TEXT | No | Stock ticker symbol |
| `trade_date` | TEXT | No | Trading date |
| `open` | NUMERIC | No | Opening price |
| `high` | NUMERIC | No | Highest price |
| `low` | NUMERIC | No | Lowest price |
| `close` | NUMERIC | No | Closing price |
| `volume` | INTEGER | No | Number of shares traded |

For the OHLCV values, the types are `NUMERIC` in the database as they have decimal values for precision. In Python, I will be using the `Decimal` data type before storing, as this avoids floating point errors.

## Primary Key

`(ticker, trade_date)`

This uniquely identifies each stock observation for a trading day

## Derived Metrics

`latest_close` is the `close` value of the most recent trading day. This will not be stored, and instead evaluated using the most recent record

Daily Change has 2 values, 

- `daily_change_absolute`: the exact change in price from the previous close price
- `daily_change_percentage`: the percentage change in price from the previous close price

These are displayed in the format `±X.XX (±X%)`, and this value will not be stored. It will be calculated from the latest 2 available closing prices. 

- `daily_change_absolute = latest_close - previous_close`
- `daily_change_percentage = daily_change_absolute * 100 / latest_close`


## Data Quality Constraints

- Required fields must not be NULL
- Prices must be non-negative
- `volume` must be non-negative
- `(ticker, trade_date)` must be unique


