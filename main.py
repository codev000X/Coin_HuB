import requests
api_key = "CG-YwvwcWdqRZh2znsHdPHHVKp2"
url = "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&names=Bitcoin&symbols=btc"

headers = {"x-cg-demo-api-key": "CG-YwvwcWdqRZh2znsHdPHHVKp2"}
parameters = {
              "include-tokens": "true",
              "include_last_updated_at": "true",
              "include_24hr_change": "true",
              "include_market_cap": "true",
              "precision": "full"
              }
response = requests.get(url, headers=headers , params=parameters)
response.raise_for_status()

print(response.text)


