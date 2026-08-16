"""
Functions to handle storage of transformed stock data

"""

import src.database as db

def store_data(transformed_data):
    connection = db.get_connection()
    raise NotImplementedError