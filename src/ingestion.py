"""
Functions to handle ingestion of data from Twelve Data stock API

"""
import time
import logging
from twelvedata import TDClient

from src.ingestion_policy import determine_ingestion_output_params
import src.config as config

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2


class APIError(Exception):
    """Raised when stock data API fails"""


"""
Fetch stock data from Twelve Data stock API.

Default outputsize is 30
"""
def fetch_stock_data(ticker=config.TICKER, interval=config.INTERVAL):
    output_params = determine_ingestion_output_params()

    for attempt in range(0, MAX_RETRIES):
        try:
            client = TDClient(apikey=config.TWELVE_DATA_API_KEY)
            response = client.time_series(
                symbol=ticker,
                interval=interval,
                **output_params
            )

            response_size = len(response.as_json())

            logger.info(f"Fetched the latest {response_size} daily AAPL records from Twelve Data API")

            return response

        except Exception as e:
            logger.warning(
                "Twelve Data API request failed for %s (attempt %s/%s) RETRYING",
                ticker,
                attempt,
                MAX_RETRIES,
                e
            )

            if attempt == MAX_RETRIES:
                logger.warning(
                    "Failed to fetch %s data after %s attempts",
                    ticker,
                    MAX_RETRIES,
                )
                raise APIError(
                    f"Failed to fetch {ticker} data after {MAX_RETRIES} attempts"
                )

            time.sleep(RETRY_DELAY)