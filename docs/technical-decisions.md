# Technical Questions and Decisions

## Stock API : Twelve Data API

Oakland have suggested Yahoo Finance for the stock API. I have also researched the Alpha Vantage and Twelve Data stock API's.

#### Yahoo Finance
The Yahoo Finance API appears to be now discontinued. Unofficial alternatives exist, but they have risks. These include inaccuracy of data and security concerns.

#### Alpha Vantage
The Alpha Vantage API is a robust API, however has restrictive premium-only access to some endpoints, especially the daily historical OHLCV data endpoint which is of interest, where each request can only request 100 data points. Paired with the rate limit of 25 requests per day on the free tier, this would use much of the rate limit to request an initial load for the application. For the requirements of this project, it would not be suitable to upgrade to the paid premium access. 

#### Twelve Data
The Twelve Data API is also a comprehensive offering. The API offers access to an endpoint that can provide daily OHCLV data, and has a generous rate limit of 800 requests per day, at 8 requests per minute, with each request able to return a maximum of 5000 data points. This is more than enough for the project requirements

**Verdict: Twelve Data**


## What data is provided in the API?

Twelve Data's API has a `/time_series` API endpoint. This endpoint provides historical OHCLV stock data for any financial instrument.

Important parameters we can specify:


| Parameter | Type | Description |
|---|---|---|
| `symbol` | String | Symbol ticker of instrument, e.g. `AAPL` |
| `interval` | String | interval between consecutive data points |
| `outputsize` | Integer | Number of data points requested. Can choose in range of `1` to `5000`, and default is `30` |
| `start_date` | String | Used together with `end_date` to specify a range for the requested data |
| `end_date` | String | Used together with `start_date` to specify a range for the requested data |
| `timezone` | String | Timezone at which output datetime will be displayed |


The output format is a JSON response, for example:

```
{
    "meta": {
        "symbol": "AAPL",
        "interval": "1min",
        "currency": "USD",
        "exchange_timezone": "America/New_York",
        "exchange": "NASDAQ",
        "mic_code": "XNAS",
        "type": "Common Stock"
    },
    "values": [
        {
            "datetime": "2021-09-16 15:59:00",
            "open": "148.73500",
            "high": "148.86000",
            "low": "148.73000",
            "close": "148.85001",
            "volume": "624277"
        }
    ],
    "status": "ok"
}
```
