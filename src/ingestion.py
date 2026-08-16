"""
Functions to handle ingestion of data from Twelve Data stock API

"""

from twelvedata import TDClient

class APIError(Exception):
    """Raised when stock data API fails"""
    pass

def fetch_stock_data():
    raise NotImplementedError

