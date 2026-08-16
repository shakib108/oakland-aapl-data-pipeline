"""
Database util functions

"""
import logging
import sqlite3

from src.config import DB_PATH, TICKER

logger = logging.getLogger(__name__)

def get_connection():
    return sqlite3.connect(DB_PATH)


def initialise_database():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_data (
                ticker TEXT NOT NULL,
                trade_date DATE NOT NULL,
                open NUMERIC NOT NULL,
                high NUMERIC NOT NULL,
                low NUMERIC NOT NULL,
                close NUMERIC NOT NULL,
                volume INTEGER NOT NULL,
                UNIQUE(ticker, trade_date)
            )
            """
        )

        connection.commit()

        logger.info("Database initialised successfully")

    except Exception:
        connection.rollback()

        logger.exception(
            "Failed to initialise database"
        )

        raise

    finally:
        connection.close()


def get_record_count(ticker=TICKER):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT COUNT(*)
            FROM stock_data
            WHERE ticker = ?
            """,
            (ticker,)
        )

        record_count = cursor.fetchone()[0]

        logger.info(
            "Found %s records for %s",
            record_count,
            ticker
        )

        return record_count

    except Exception:
        logger.exception(
            "Failed to get record count for %s",
            ticker
        )
        raise

    finally:
        connection.close()


def delete_oldest_records(ticker=TICKER, records_to_delete=0):
    if records_to_delete <= 0:
        return

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM stock_data
            WHERE rowid IN (
                SELECT rowid
                FROM stock_data
                WHERE ticker = ?
                ORDER BY trade_date ASC
                LIMIT ?
            )
            """,
            (ticker, records_to_delete)
        )

        connection.commit()

        logger.info(
            "Deleted %s oldest records for %s",
            records_to_delete,
            ticker
        )

    except Exception:
        connection.rollback()
        logger.exception(
            "Failed to delete oldest records for %s",
            ticker
        )
        raise

    finally:
        connection.close()


def get_latest_trade_date(ticker=TICKER):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT MAX(trade_date)
            FROM stock_data
            WHERE ticker = ?
            """,
            (ticker,)
        )

        latest_trade_date = cursor.fetchone()[0]

        logger.info(
            "Latest trade date for %s: %s",
            ticker,
            latest_trade_date
        )

        if latest_trade_date is None:
            return None

        return date.fromisoformat(latest_trade_date)

    except Exception:
        logger.exception(
            "Failed to get latest trade date for %s",
            ticker
        )
        raise

    finally:
        connection.close()

