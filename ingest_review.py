import pandas as pd
import sqlite3
import os
import time

# --- Configuration ---
JSON_FILE = 'yelp_academic_dataset_review.json' # ⚠️ Double-check this filename!
DATABASE_FILE = 'yelp.db'
TABLE_NAME = 'review'
CHUNK_SIZE = 100000 
# ---------------------

def import_review_data():
    """
    Reads the massive review.json file in chunks and appends it
    to the 'review' table in our existing SQLite database.
    """
    
    if not os.path.exists(JSON_FILE):
        print(f"Error: File not found at '{JSON_FILE}'")
        print("Please check the 'JSON_FILE' variable.")
        return

    if not os.path.exists(DATABASE_FILE):
        print(f"Error: Database '{DATABASE_FILE}' not found.")
        print("Please run 'ingest_business.py' first.")
        return

    print(f"Starting import of '{JSON_FILE}'...")
    print("This... is going to take a while. Go grab a coffee. ☕")
    
    start_time = time.time()
    
    conn = sqlite3.connect(DATABASE_FILE)
    
    try:
        reader = pd.read_json(JSON_FILE, lines=True, chunksize=CHUNK_SIZE)
        
        total_rows = 0
        for i, chunk in enumerate(reader):
            # This appends to the 'review' table in the *same* yelp.db
            chunk.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
            
            total_rows += len(chunk)
            elapsed_minutes = (time.time() - start_time) / 60
            
            print(f"Processed chunk {i + 1} ({total_rows:,} total rows) in {elapsed_minutes:.2f} minutes")

        end_time = time.time()
        print(f"\n--- 🚀 Success! ---")
        print(f"Finished importing {total_rows:,} rows into '{TABLE_NAME}' table.")
        print(f"Total time: {(end_time - start_time) / 60:.2f} minutes.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    finally:
        conn.close()

# --- Main execution ---
if __name__ == "__main__":
    import_review_data()