import sqlite3
import pytest
from decimal import Decimal
from datetime import date
from unittest.mock import Mock, patch

from src.storage import store_data


def valid_record():
    return {
        "ticker": "AAPL",
        "trade_date": date(2021, 9, 16),
        "open": Decimal("148.73500"),
        "high": Decimal("148.86000"),
        "low": Decimal("148.73000"),
        "close": Decimal("148.85001"),
        "volume": 624277,
    }


@pytest.fixture
def connection():
    connection = sqlite3.connect(":memory:")

    connection.execute("""
        CREATE TABLE stock_data (
            ticker TEXT NOT NULL,
            trade_date DATE NOT NULL,
            open DECIMAL NOT NULL,
            high DECIMAL NOT NULL,
            low DECIMAL NOT NULL,
            close DECIMAL NOT NULL,
            volume INTEGER NOT NULL,
            UNIQUE(ticker, trade_date)
        )
    """)

    yield connection

    connection.close()


def test_valid_record_is_stored(connection):
    records = [valid_record()]

    with patch("src.database.get_connection", return_value=connection):
        store_data(records)

    result = connection.execute(
        "SELECT * FROM stock_data"
    ).fetchall()

    assert len(result) == 1
    assert result[0][0] == "AAPL"
    assert result[0][1] == "2021-09-16"


def test_multiple_records_are_stored(connection):
    records = [
        valid_record(),
        {
            **valid_record(),
            "trade_date": date(2021, 9, 17),
        },
    ]

    with patch("src.database.get_connection", return_value=connection):
        store_data(records)

    result = connection.execute(
        "SELECT * FROM stock_data"
    ).fetchall()

    assert len(result) == 2


def test_existing_record_is_updated(connection):
    original = valid_record()

    updated = {
        **original,
        "close": Decimal("205.00"),
    }

    with patch("src.database.get_connection", return_value=connection):
        store_data([original])
        store_data([updated])

    result = connection.execute(
        """
        SELECT close
        FROM stock_data
        WHERE ticker = 'AAPL'
        AND trade_date = '2021-09-16'
        """
    ).fetchone()

    assert result[0] == 205


def test_different_tickers_on_same_date_are_stored(connection):
    aapl = valid_record()

    msft = {
        **valid_record(),
        "ticker": "MSFT",
    }

    with patch("src.database.get_connection", return_value=connection):
        store_data([aapl, msft])

    result = connection.execute(
        "SELECT * FROM stock_data"
    ).fetchall()

    assert len(result) == 2
