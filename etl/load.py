import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_batch

load_dotenv()


def load_prices(records):
    """
    Load transformed coin price records into PostgreSQL.
    Uses batch insert + UPSERT to avoid duplicates.
    """

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        cur = conn.cursor()

        insert_query = """
        INSERT INTO coin_prices (
            coin,
            usd_price,
            pkr_price,
            usd_market_cap,
            pkr_market_cap,
            usd_24h_change,
            pkr_24h_change,
            last_updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (coin)
        DO UPDATE SET
            usd_price = EXCLUDED.usd_price,
            pkr_price = EXCLUDED.pkr_price,
            usd_market_cap = EXCLUDED.usd_market_cap,
            pkr_market_cap = EXCLUDED.pkr_market_cap,
            usd_24h_change = EXCLUDED.usd_24h_change,
            pkr_24h_change = EXCLUDED.pkr_24h_change,
            last_updated_at = EXCLUDED.last_updated_at;
        """

        insert_query_history = """
        INSERT INTO coin_prices_history (

            coin, 
            usd_price, 
            pkr_price, 
            usd_market_cap, 
            pkr_market_cap, 
            usd_24h_change, 
            pkr_24h_change, 
            last_updated_at
        ) 
        
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """


        values = [(r["coin"],r["usd_price"], r["pkr_price"], r["usd_market_cap"], r["pkr_market_cap"], 
        r["usd_24h_change"], r["pkr_24h_change"], r["last_updated_at"]) for r in records]

        # Latest snapshot
        execute_batch(cur, insert_query, values)

        # Full history
        execute_batch(cur, insert_query_history, values)
        conn.commit()

        print("✅ Prices loaded successfully")

    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Error loading prices:", e)
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()