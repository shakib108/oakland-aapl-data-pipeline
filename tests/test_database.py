from unittest.mock import patch

from src.database import get_connection, initialise_database


def test_initialise_database_creates_stock_table(tmp_path):
    db_path = tmp_path / "test.db"

    with patch("src.config.DB_PATH", str(db_path)):
        initialise_database()

        connection = get_connection()

        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'stock_data'
        """).fetchone()

        connection.close()

    assert result is not None
    assert result[0] == "stock_data"


def test_initialise_database_can_run_when_database_already_exists(tmp_path):
    db_path = tmp_path / "test.db"

    with patch("src.config.DB_PATH", str(db_path)):
        initialise_database()
        initialise_database()

        connection = get_connection()

        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'stock_data'
        """).fetchone()

        connection.close()

    assert result is not None


def test_initialise_database_creates_expected_columns(tmp_path):
    db_path = tmp_path / "test.db"

    with patch("src.config.DB_PATH", str(db_path)):
        initialise_database()

        connection = get_connection()

        columns = connection.execute(
            "PRAGMA table_info(stock_data)"
        ).fetchall()

        connection.close()

    column_names = [column[1] for column in columns]

    assert column_names == [
        "ticker",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]