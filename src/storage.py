"""
Functions to handle storage of transformed stock data

"""
import logging
import src.database as db

logger = logging.getLogger(__name__)


def store_data(transformed_df):
    connection = db.get_connection()

    try:
        records = transformed_df.to_records(index=False)

        connection.executemany(
            """
            INSERT INTO stock_data (
                ticker,
                trade_date,
                open,
                high,
                low,
                close,
                volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ticker, trade_date)
            DO UPDATE SET
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                close = excluded.close,
                volume = excluded.volume
            """,
            records
        )

        connection.commit()

        logger.info(
            "Stored %s records successfully",
            len(transformed_df)
        )

    except Exception:
        connection.rollback()

        logger.exception(
            "Failed to store %s records",
            len(transformed_df)
        )

        raise

    finally:
        connection.close()