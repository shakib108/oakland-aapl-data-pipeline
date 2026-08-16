import os
from dotenv import load_dotenv


load_dotenv()

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

if not TWELVE_DATA_API_KEY or TWELVE_DATA_API_KEY == "":
    raise ValueError("TWELVE_DATA_API_KEY not set")


# Source data request params
TICKER = "AAPL"
INTERVAL = "1day"

DB_PATH = os.getenv(
    "DB_PATH",
    "data/stocks.db"
)