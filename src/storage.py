"""
Functions to handle storage of transformed stock data

"""
import logging
import src.database as db

logger = logging.getLogger(__name__)


MAX_RECORDS = 10000


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


def enforce_retention():
    record_count = db.get_record_count()

    if record_count <= MAX_RECORDS:
        return

    records_to_delete = record_count - MAX_RECORDS

    db.delete_oldest_records(
        records_to_delete
    )