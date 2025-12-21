import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def create_project_database():
    # 1. Connect to the default 'postgres' database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        dbname='postgres'
    )
    conn.autocommit = True 
    cur = conn.cursor()

    # 2. Execute CREATE DATABASE
    db_name = os.getenv('DB_NAME')
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Success: Database '{db_name}' created.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Notice: Database '{db_name}' already exists.")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_project_database()