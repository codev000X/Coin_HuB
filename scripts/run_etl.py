from etl.extract import get_prices
from etl.transform import transform_prices
from etl.load import load_prices
import sys
from logging_config import get_logger

logger = get_logger("run_etl")

COINS = [
    "bitcoin", "ethereum", "litecoin", "bitcoin-cash", "binancecoin",
    "eos", "ripple", "stellar", "chainlink", "polkadot", "yearn-finance"
]
   
def main():
    raw_data = get_prices(COINS)
    records = transform_prices(raw_data)
    load_prices(records)

if __name__ == "__main__": 
    try:
        logger.info("Starting the pipeline")
        main()
        logger.info("Pipeline Ended Successfully.")

    except Exception as e:
        logger.info(f"Pipeline ran into an Error: {e}")
        sys.exit(1)
