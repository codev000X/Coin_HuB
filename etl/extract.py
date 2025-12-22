import requests
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_prices(coins, vs_currencies_list = ["usd", "pkr"]):
    """
    Fetch prices for multiple coins in selected currencies and return the raw json response.
    """
    params = {
        "ids": ",".join(coins),
        "vs_currencies": ",".join(vs_currencies_list),
        "include_market_cap": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    headers = {"x-cg-demo-api-key": API_KEY}
    resp = requests.get(BASE_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

