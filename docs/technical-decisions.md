# Technical Decisions

## Stock API : Twelve Data API

Oakland have suggested Yahoo Finance for the stock API. I have also researched the Alpha Vantage and Twelve Data stock API's.

#### Yahoo Finance
The Yahoo Finance API appears to be now discontinued. Unofficial alternatives exist, but they have risks. These include inaccuracy of data and security concerns.

#### Alpha Vantage
The Alpha Vantage API is a robust API, however has restrictive premium-only access to some endpoints, especially the daily historical OHLCV data endpoint which is of interest, where each request can only request 100 data points. Paired with the rate limit of 25 requests per day on the free tier, this would use much of the rate limit to request an initial load for the application. For the requirements of this project, it would not be suitable to upgrade to the paid premium access. 

#### Twelve Data
The Twelve Data API is also a comprehensive offering. The API offers access to an endpoint that can provide daily OHCLV data, and has a generous rate limit of 800 requests per day, at 8 requests per minute, with each request able to return a maximum of 5000 data points. This is more than enough for the project requirements

### Verdict: Twelve Data



