"""
Functions to handle validation of data ingested from Twelve Data stock API

"""
import logging
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd

import src.config as config


logger = logging.getLogger(__name__)

PRICE_PRECISION = Decimal("0.01")

TARGET_COLUMNS = [
    "ticker",
    "trade_date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def transform_stock_data(source_df, ticker=config.TICKER):
    transformed_df = source_df.copy()

    # Rename API field to database field
    transformed_df = transformed_df.rename(
        columns={
            "datetime": "trade_date"
        }
    )

    # Convert datetime to date because pipeline uses daily data
    transformed_df["trade_date"] = pd.to_datetime(
        transformed_df["trade_date"]
    ).dt.date

    # Convert price fields to Decimal for NUMERIC storage
    price_columns = [
        "open",
        "high",
        "low",
        "close",
    ]

    for column in price_columns:
        transformed_df[column] = pd.to_numeric(
            transformed_df[column]
        ).round(2)

    # Convert volume to integer
    transformed_df["volume"] = pd.to_numeric(
        transformed_df["volume"]
    ).astype(int)

    # Add ticker supplied to the ingestion request
    transformed_df["ticker"] = ticker

    # Select and order columns according to target schema
    transformed_df = transformed_df[TARGET_COLUMNS]

    logger.info(
        "Transformation completed: %s records transformed for %s",
        len(transformed_df),
        ticker
    )

    return transformed_df