"""
Database util functions

"""

import sqlite3

from src.config import DB_PATH


def initialise_database():
    raise NotImplementedError


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_record_count():
    raise NotImplementedError


def get_latest_trade_date():
    raise NotImplementedError