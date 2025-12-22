CREATE TABLE IF NOT EXISTS coin_prices (

    id SERIAL PRIMARY KEY,

    coin TEXT NOT NULL UNIQUE,

    usd_price NUMERIC,
    pkr_price NUMERIC,

    usd_market_cap NUMERIC,
    pkr_market_cap NUMERIC,

    usd_24h_change NUMERIC,
    pkr_24h_change NUMERIC,

    last_updated_at BIGINT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coin_prices_history (
    id SERIAL PRIMARY KEY,
    coin TEXT NOT NULL,
    usd_price NUMERIC,
    pkr_price NUMERIC,
    usd_market_cap NUMERIC,
    pkr_market_cap NUMERIC,
    usd_24h_change NUMERIC,
    pkr_24h_change NUMERIC,
    last_updated_at BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
