from datetime import date
from decimal import Decimal

from src.transformation import transform_data

def valid_record():
    return {
        "ticker": "AAPL",
        "trade_date": "2021-09-16",
        "open": "148.73500",
        "high": "148.86000",
        "low": "148.73000",
        "close": "148.85001",
        "volume": "624277",
    }


def test_transformation_returns_expected_fields():
    records = [valid_record()]

    result = transform_data(records)

    assert "ticker" in result[0]
    assert "trade_date" in result[0]
    assert "open" in result[0]
    assert "high" in result[0]
    assert "low" in result[0]
    assert "close" in result[0]
    assert "volume" in result[0]


def test_transformation_converts_datetime_to_date():
    records = [valid_record()]

    result = transform_data(records)

    assert isinstance(result[0]["date"], date)
    assert result[0]["date"] == date(2021, 9, 16)


def test_transformation_converts_prices_to_decimal():
    records = [valid_record()]

    result = transform_data(records)

    assert isinstance(result[0]["open"], Decimal)
    assert isinstance(result[0]["high"], Decimal)
    assert isinstance(result[0]["low"], Decimal)
    assert isinstance(result[0]["close"], Decimal)


def test_transformation_converts_volume_to_integer():
    records = [valid_record()]

    result = transform_data(records)

    assert isinstance(result[0]["volume"], int)