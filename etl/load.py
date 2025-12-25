import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_batch
from logging_config import get_logger
from etl.retrying_logic import retry


load_dotenv()

logger = get_logger("load")


@retry(max_retries=5, delay=2)
def load_prices(records):
    """
    Load transformed coin price records into PostgreSQL.
    Uses batch insert + UPSERT to avoid duplicates.
    """

    logger.info("Starting to load data into the database")


    conn = None
    cur = None

    try:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS")
            )

        except Exception as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            raise

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

        logger.info(f"Prepared {len(values)} records for insertion")

        if not records:
            logger.warning("No records to insert, skipping load")
            return

        # Latest snapshot
        execute_batch(cur, insert_query, values)
        logger.info(f"Inserted {len(values)} records into coin_prices (snapshot)")


        # Full history
        execute_batch(cur, insert_query_history, values)
        logger.info(f"Inserted {len(values)} records into coin_prices_history")

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Data loading failed: {e}" , exc_info=True)
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()