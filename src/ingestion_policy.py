"""
Function to determine how many records should be ingested with each request

"""
import logging
from datetime import date, timedelta
import src.database as db


logger = logging.getLogger(__name__)


INITIAL_LOAD_SIZE = 1000
REGULAR_LOAD_SIZE = 30
MAX_LOAD_SIZE = 10_000
GAP_THRESHOLD_DAYS = 30


def determine_ingestion_output_params(
    latest_trade_date=None,
    today=None
):
    """
    Determine the parameters to use when requesting stock data.

    Returns either:
        {"outputsize": <number>}
    or:
        {"start_date": <date>, "end_date": <date>}
    """

    record_count = db.get_record_count()

    if today is None:
        today = date.today()

    # Database does not have enough records
    if record_count < INITIAL_LOAD_SIZE:

        # Empty database
        if record_count == 0:
            logger.info(
                "Database is empty. Requesting initial load of %s records for initial load.",
                INITIAL_LOAD_SIZE
            )

        # Database contains fewer than the initial target
        else:
            logger.info(
                "Database contains %s records, which is below the 1000 record initial load amount. Requesting %s records.",
                record_count,
                INITIAL_LOAD_SIZE
            )

        return {
            "outputsize": INITIAL_LOAD_SIZE
        }


    # Check whether there is a data gap
    if latest_trade_date is not None:
        gap_days = (today - latest_trade_date).days

        if gap_days > GAP_THRESHOLD_DAYS:
            start_date = latest_trade_date + timedelta(days=1)
            end_date = today

            logger.info(
                "Data gap of %s days detected. Requesting data from %s to %s.",
                gap_days,
                start_date,
                end_date
            )

            return {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }

    # Normal incremental load
    logger.info(
        "Database is up to date. Requesting latest %s records.",
        REGULAR_LOAD_SIZE
    )

    return {
        "outputsize": REGULAR_LOAD_SIZE
    }