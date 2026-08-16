from datetime import date, timedelta
from unittest.mock import patch

from src.ingestion_policy import determine_ingestion_output_params


def test_empty_database_fetches_1000_records():
    with patch(
        "src.database.get_record_count",
        return_value=0
    ):
        result = determine_ingestion_output_params()

    assert result == {
        "outputsize": 1000
    }


def test_database_below_1000_records_fetches_1000_records():
    with patch(
        "src.database.get_record_count",
        return_value=500
    ):
        result = determine_ingestion_output_params()

    assert result == {
        "outputsize": 1000
    }


def test_database_with_1000_records_fetches_latest_30():
    with patch(
        "src.database.get_record_count",
        return_value=1000
    ):
        result = determine_ingestion_output_params()

    assert result == {
        "outputsize": 30
    }


def test_database_with_more_than_1000_records_fetches_latest_30():
    with patch(
        "src.database.get_record_count",
        return_value=5000
    ):
        result = determine_ingestion_output_params()

    assert result == {
        "outputsize": 30
    }


def test_gap_larger_than_30_days_returns_date_range():
    today = date.today()
    latest_trade_date = today - timedelta(days=31)

    with (
        patch(
            "src.database.get_record_count",
            return_value=5000
        ),
        patch(
            "src.database.get_latest_trade_date",
            return_value=latest_trade_date
        ),
    ):
        result = determine_ingestion_output_params()

    assert result == {
        "start_date": latest_trade_date,
        "end_date": today
    }