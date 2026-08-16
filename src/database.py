"""
Database util functions

"""
import logging
import sqlite3

from src.config import DB_PATH

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


def get_record_count():
    raise NotImplementedError


def get_latest_trade_date():
    raise NotImplementedError