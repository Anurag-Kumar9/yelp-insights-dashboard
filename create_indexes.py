import sqlite3
import time

DATABASE_FILE = 'yelp.db'

# Define all the indexes we want in our database
# Format: (index_name, table_name, column_name)
INDEXES_TO_CREATE = [
    ('idx_review_business_id', 'review', 'business_id'),
    ('idx_review_user_id', 'review', 'user_id'), # Also useful for our JOIN
    ('idx_user_clusters_user_id', 'user_clusters', 'user_id'),
]

def add_indexes():
    print(f"Connecting to {DATABASE_FILE} to ensure all indexes are built...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    for index_name, table_name, column_name in INDEXES_TO_CREATE:
        print(f"Checking for index '{index_name}' on '{table_name}({column_name})'...")
        
        # Check if index already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index_name,))
        if cursor.fetchone():
            print(" -> Index already exists. Skipping.")
            continue

        # If it doesn't exist, create it
        print(" -> Index not found. Creating it now (this may take a few minutes)...")
        start_time = time.time()
        
        try:
            cursor.execute(f"CREATE INDEX {index_name} ON {table_name} ({column_name})")
            conn.commit()
            end_time = time.time()
            print(f"    -> Success! Created in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            print(f"    -> ERROR creating index: {e}")
            
    print("\n--- ✅ All necessary indexes checked/created. ---")
    conn.close()

if __name__ == "__main__":
    add_indexes()