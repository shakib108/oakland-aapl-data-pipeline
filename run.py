import logging

from src.ingestion import fetch_stock_data
from src.validation import validate_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

def main():
    logger = logging.getLogger(__name__)

    # Extract
    source_df = fetch_stock_data().as_pandas()
    source_df = source_df.reset_index()
    is_valid = validate_data(source_df)




if __name__ == "__main__":
    main()