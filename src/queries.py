import logging

from src.config import TICKER
from src.database import get_connection


logger = logging.getLogger(__name__)


def get_latest_close(ticker=TICKER):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT close
            FROM stock_data
            WHERE ticker = ?
            ORDER BY trade_date DESC
            LIMIT 1
            """,
            (ticker,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        latest_close = result[0]

        logger.info(
            "Latest close price for %s: %s",
            ticker,
            latest_close
        )

        return latest_close

    except Exception:
        logger.exception(
            "Failed to get latest close price for %s",
            ticker
        )
        raise

    finally:
        connection.close()


def get_daily_change(ticker="AAPL"):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT close
            FROM stock_data
            WHERE ticker = ?
            ORDER BY trade_date DESC
            LIMIT 2
            """,
            (ticker,)
        )

        rows = cursor.fetchall()

        if len(rows) < 2:
            return {
                "absolute_change": None,
                "percentage_change": None
            }

        latest_close = rows[0][0]
        previous_close = rows[1][0]

        absolute_change = latest_close - previous_close

        if absolute_change > 0:
            plusminus = "+"
        else:
            plusminus = "-"

        if previous_close == 0:
            percentage_change = None
        else:
            percentage_change = (
                absolute_change / previous_close
            ) * 100

        logger.info(
            "Daily change for %s: %s$%.2f (%s%.2f%%)",
            ticker,
            plusminus,
            absolute_change,
            plusminus,
            percentage_change
        )

        return {
            "latest_close": latest_close,
            "absolute_change": absolute_change,
            "percentage_change": percentage_change
        }

    except Exception:
        logger.exception(
            "Failed to calculate daily change for %s",
            ticker
        )
        raise

    finally:
        connection.close()