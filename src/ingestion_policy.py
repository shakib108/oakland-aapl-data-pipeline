"""
Function to determine how many records should be ingested with each request

"""

import src.database as db


def determine_ingestion_output_params():
    current_record_count = db.get_record_count()
    raise NotImplementedError

