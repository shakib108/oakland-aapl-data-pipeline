import logging

from src.ingestion import fetch_stock_data
from src.validation import validate_data
from src.transformation import transform_stock_data
from src.database import initialise_database
from src.storage import store_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

def main():
    logger = logging.getLogger(__name__)

    initialise_database()

    # Extract
    source_df = fetch_stock_data().as_pandas()
    source_df = source_df.reset_index()
    is_valid = validate_data(source_df)
    transformed_df = transform_stock_data(source_df)
    store_data(transformed_df)

    print(transformed_df)




if __name__ == "__main__":
    main()