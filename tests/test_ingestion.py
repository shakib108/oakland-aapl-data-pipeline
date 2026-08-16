from unittest.mock import Mock, patch

import pytest

from src.ingestion import fetch_stock_data, APIError

def test_ingestion_returns_api_data():
    mock_response = Mock()
    mock_response.status_code = "ok"
    mock_response.as_json.return_value = {
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

    mock_client = Mock()
    mock_client.time_series.return_value = mock_response

    with patch("src.ingestion.TDClient", return_value=mock_client):
        result = fetch_stock_data()

    assert len(result) == 1
    assert result[0]["datetime"] == "2021-09-16 15:59:00"
    assert result[0]["close"] == "148.85001"


def test_ingestion_handles_api_failure():
    mock_client = Mock()
    mock_client.time_series.side_effect = Exception("API request failed")

    with patch("src.ingestion.TDClient", return_value=mock_client):
        with pytest.raises(APIError):
            fetch_stock_data()


def test_ingestion_handles_empty_response():
    mock_response = Mock()
    mock_response.as_json.return_value = {
        "values": []
    }

    mock_client = Mock()
    mock_client.time_series.return_value = mock_response

    with patch("src.ingestion.TDClient", return_value=mock_client):
        result = fetch_stock_data()

    assert result == []
        