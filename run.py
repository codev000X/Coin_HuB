# run.py
from etl.extract import get_prices
from etl.transform import transform_prices
"

# Optional: define the coins you want to fetch
coins = [
    "bitcoin", "ethereum", "litecoin", "bitcoin-cash", "binancecoin",
    "eos", "ripple", "stellar", "chainlink", "polkadot", "yearn-finance"
]

def main():
    # 1️⃣ Extract
    raw_data = get_prices(api_key=API_KEY, BASE_URL=BASE_URL, coins=coins)

    # 2️⃣ Transform
    structured_data = transform_prices(raw_data)

    # 3️⃣ For now, just print it
    for coin, metrics in structured_data.items():
        print(f"{coin}: {metrics}")

if __name__ == "__main__":
    main()
