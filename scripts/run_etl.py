# scripts/run_etl.py

from etl.extract import get_prices
from etl.transform import transform_prices

COINS = [
    "bitcoin", "ethereum", "litecoin", "bitcoin-cash", "binancecoin",
    "eos", "ripple", "stellar", "chainlink", "polkadot", "yearn-finance"
]
   
def main():
    raw_data = get_prices(COINS)
    records = transform_prices(raw_data)

    for r in records:
        print(r)

if __name__ == "__main__":
    main()
