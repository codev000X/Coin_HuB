import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_schema():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

    cur = conn.cursor()

    # Read schema.sql
    with open("database/schema.sql", "r") as f:
        schema_sql = f.read()

    # Execute schema
    cur.execute(schema_sql)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Database schema initialized successfully")

if __name__ == "__main__":
    initialize_schema()
