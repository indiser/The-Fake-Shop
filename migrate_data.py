import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = 'instance/Product.db' 
NEON_PG_URL = os.environ.get("NEON_POSTGRES_DB_URL")

def run_migration():
    print("Connecting to databases...")
    
    try:
        # Open local connection
        sqlite_conn = sqlite3.connect(SQLITE_PATH)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Open remote connection
        pg_conn = psycopg2.connect(NEON_PG_URL)
        pg_cursor = pg_conn.cursor()
        
        print("Extracting products from local SQLite...")
        # We only grab the core data, letting Postgres generate new IDs to avoid sequence errors
        sqlite_cursor.execute("SELECT title, price, description, image_url FROM product")
        products = sqlite_cursor.fetchall()
        
        if not products:
            print("No products found in the local database. Check your SQLITE_PATH.")
            return

        print(f"Found {len(products)} products. Loading into Render...")
        
        # Insert each product into the cloud database
        for product in products:
            pg_cursor.execute(
                """
                INSERT INTO product (title, price, description, image_url) 
                VALUES (%s, %s, %s, %s)
                """,
                (product[0], product[1], product[2], product[3])
            )
            
        # Commit the transaction to save the data permanently
        pg_conn.commit()
        print(f"✅ SUCCESS: {len(products)} products successfully migrated to the cloud!")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    finally:
        # Always close your connections
        if 'sqlite_conn' in locals(): sqlite_conn.close()
        if 'pg_conn' in locals(): pg_conn.close()

if __name__ == "__main__":
    run_migration()
