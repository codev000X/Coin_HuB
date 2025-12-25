import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from logging_config import get_logger
from etl.retrying_logic import retry


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

# Initializing the logger 
logger = get_logger("extract")

@retry(max_retries=5, delay=2)
def get_prices(coins, vs_currencies_list = ["usd", "pkr"]):
    """
    Fetch prices for multiple coins in selected currencies and return the raw json response.
    """
    # info logging
    logger.info("Starting data extraction from CoinGecko")

    params = {
        "ids": ",".join(coins),
        "vs_currencies": ",".join(vs_currencies_list),
        "include_market_cap": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    headers = {"x-cg-demo-api-key": API_KEY}

    try:
        logger.info(f"Requesting prices for coins: {coins} in {vs_currencies_list}")

        resp = requests.get(BASE_URL, headers=headers, params=params)
        resp.raise_for_status()

        logger.info(f"Data Extraction Successful -- received {len(resp.json())} records.")

        return resp.json()

    except Exception as e:
        logger.error(f"Data extraction failed: {e}" , exc_info=True)
        raise

