"""
Functions to handle validation of data ingested from Twelve Data stock API

"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {
    "datetime",
    "open",
    "high",
    "low",
    "close",
    "volume",
}


def validate_required_fields(source_df):
    missing_fields = REQUIRED_FIELDS - set(source_df.columns)

    if missing_fields:
        logger.error(
            "Validation failed: missing required fields: %s",
            missing_fields
        )
        raise ValueError(
            f"Missing required fields: {missing_fields}"
        )

    return True


def validate_no_nulls(source_df):
    null_counts = source_df[list(REQUIRED_FIELDS)].isnull().sum()
    fields_with_nulls = null_counts[null_counts > 0]

    if not fields_with_nulls.empty:
        logger.error(
            "Validation failed: null values found: %s",
            fields_with_nulls.to_dict()
        )
        raise ValueError(
            f"Null values found: {fields_with_nulls.to_dict()}"
        )

    return True


def validate_no_duplicates(source_df):
    duplicate_count = source_df.duplicated(
        subset=["datetime"]
    ).sum()

    if duplicate_count > 0:
        logger.error(
            "Validation failed: %s duplicate records found",
            duplicate_count
        )
        raise ValueError(
            f"{duplicate_count} duplicate records found"
        )

    return True


def validate_dates(source_df):
    dates = pd.to_datetime(
        source_df["datetime"],
        errors="coerce"
    )

    invalid_count = dates.isna().sum()

    if invalid_count > 0:
        logger.error(
            "Validation failed: %s invalid dates found",
            invalid_count
        )
        raise ValueError(
            f"{invalid_count} invalid dates found"
        )

    return True


def validate_numeric_fields(source_df):
    numeric_fields = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for field in numeric_fields:
        values = pd.to_numeric(
            source_df[field],
            errors="coerce"
        )

        invalid_count = values.isna().sum()

        if invalid_count > 0:
            logger.error(
                "Validation failed: %s invalid numeric values found in %s",
                invalid_count,
                field
            )
            raise ValueError(
                f"{invalid_count} invalid numeric values found in {field}"
            )

    return True


def validate_ohlc(source_df):
    invalid_rows = (
        (source_df["high"] < source_df["open"]) |
        (source_df["high"] < source_df["close"]) |
        (source_df["high"] < source_df["low"]) |
        (source_df["low"] > source_df["open"]) |
        (source_df["low"] > source_df["close"])
    )

    invalid_count = invalid_rows.sum()

    if invalid_count > 0:
        logger.error(
            "Validation failed: %s records contain invalid OHLC relationships",
            invalid_count
        )
        raise ValueError(
            f"{invalid_count} records contain invalid OHLC relationships"
        )

    return True


def validate_volume(source_df):
    invalid_rows = source_df["volume"] < 0
    invalid_count = invalid_rows.sum()

    if invalid_count > 0:
        logger.error(
            "Validation failed: %s records contain negative volume",
            invalid_count
        )
        raise ValueError(
            f"{invalid_count} records contain negative volume"
        )

    return True


def validate_data(source_df):
    validate_required_fields(source_df)
    validate_no_nulls(source_df)
    validate_no_duplicates(source_df)
    validate_dates(source_df)
    validate_numeric_fields(source_df)
    validate_ohlc(source_df)
    validate_volume(source_df)

    logger.info(
        "Validation passed: %s records validated successfully",
        len(source_df)
    )

    return True