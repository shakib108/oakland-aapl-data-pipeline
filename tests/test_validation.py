from src.validation import validate_data

def valid_record():
    return {
        "meta": {
            "symbol": "AAPL",
            "interval": "1day",
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


def test_valid_dataset_passes_validation():
    records = [
        valid_record(),
        valid_record(),
        valid_record(),
    ]

    result = validate_data(records)

    assert result.is_valid is True
    assert len(result.invalid_records) == 0


def test_missing_required_field_fails_validation():
    records = [valid_record()]
    del records[0]["values"][0]["close"]

    result = validate_data(records)

    assert result.is_valid is False
    assert len(result.invalid_records) == 1


def test_negative_price_fails_validation():
    records = [valid_record()]
    records[0]["values"][0]["close"] = "-10.00"

    result = validate_data(records)

    assert result.is_valid is False
    assert len(result.invalid_records) == 1


def test_invalid_ohlc_values_fail_validation():
    records = [valid_record()]
    records[0]["values"][0]["high"] = "100.00"
    records[0]["values"][0]["low"] = "110.00"

    result = validate_data(records)

    assert result.is_valid is False
    assert len(result.invalid_records) == 1


def test_duplicate_records_fail_validation():
    record_1 = valid_record()
    record_2 = valid_record()

    records = [record_1, record_2]

    result = validate_data(records)

    assert result.is_valid is False
    assert len(result.invalid_records) == 1


def test_null_values_fail_validation():
    records = [valid_record()]
    records[0]["values"][0]["close"] = None

    result = validate_data(records)

    assert result.is_valid is False
    assert len(result.invalid_records) == 1