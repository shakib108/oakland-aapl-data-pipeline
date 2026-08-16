import logging

from src.ingestion import fetch_stock_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

def main():
    logger = logging.getLogger(__name__)

    data = fetch_stock_data().as_pandas()
    print(data)



if __name__ == "__main__":
    main()