from etl.extract import get_prices
from etl.transform import transform_prices
from etl.load import load_prices
import sys

COINS = [
    "bitcoin", "ethereum", "litecoin", "bitcoin-cash", "binancecoin",
    "eos", "ripple", "stellar", "chainlink", "polkadot", "yearn-finance"
]
   
def main():
    raw_data = get_prices(COINS)
    records = transform_prices(raw_data)
    load_prices(records)

    print("✅ ETL completed successfully")
if __name__ == "__main__": 
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
