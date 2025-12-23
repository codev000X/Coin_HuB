from 

def transform_prices(raw_data):
    """
    Transform raw API response into flat, DB-ready records.
    """
    records = []

    for coin, details in raw_data.items():
        records.append({
            "coin": coin,
            "usd_price": details.get("usd"),
            "pkr_price": details.get("pkr"),
            "usd_market_cap": details.get("usd_market_cap"),
            "pkr_market_cap": details.get("pkr_market_cap"),
            "usd_24h_change": details.get("usd_24h_change"),
            "pkr_24h_change": details.get("pkr_24h_change"),
            "last_updated_at": details.get("last_updated_at")
        })

    return records

