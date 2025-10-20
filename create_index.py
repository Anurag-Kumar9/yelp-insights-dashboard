import sqlite3
import time

DATABASE_FILE = 'yelp.db'

def add_index():
    print(f"Connecting to {DATABASE_FILE}...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    print("Starting to build index on 'review(business_id)'...")
    print("This will take 5-10 minutes. The database will be locked. Be patient.")

    start_time = time.time()

    try:
        # Create the index
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_review_business_id ON review (business_id)")
        conn.commit()

        end_time = time.time()
        print(f"\n--- ✅ Success! ---")
        print(f"Index created in {end_time - start_time:.2f} seconds.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_index()