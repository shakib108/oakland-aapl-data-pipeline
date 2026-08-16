"""
Database util functions

"""

import sqlite3

from src.config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_record_count():
    return NotImplementedError


def get_latest_trade_date():
    return NotImplementedError