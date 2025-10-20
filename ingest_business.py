import pandas as pd
import sqlite3
import os

# --- Configuration ---
JSON_FILE = 'yelp_academic_dataset_business.json' 
DATABASE_FILE = 'yelp.db'
TABLE_NAME = 'business'
CHUNK_SIZE = 50000 
# ---------------------

def import_business_data():
    """
    Reads the business.json file and imports it into
    the 'business' table in our SQLite database.
    """
    
    if os.path.exists(DATABASE_FILE):
        print(f"'{DATABASE_FILE}' already exists. Deleting to start fresh.")
        os.remove(DATABASE_FILE)

    if not os.path.exists(JSON_FILE):
        print(f"Error: File not found at '{JSON_FILE}'")
        print("Make sure the file is in the same folder as this script.")
        print("Please check the 'JSON_FILE' variable.")
        return

    print(f"Starting import of '{JSON_FILE}'...")
    
    conn = sqlite3.connect(DATABASE_FILE)
    
    try:
        reader = pd.read_json(JSON_FILE, lines=True, chunksize=CHUNK_SIZE)
        
        total_rows = 0
        for i, chunk in enumerate(reader):
            
            # --- 💡 NEW LINES START 💡 ---
            # Convert columns that are dicts into simple strings (JSON strings)
            # This solves the "type 'dict' is not supported" error
            if 'attributes' in chunk.columns:
                chunk['attributes'] = chunk['attributes'].astype(str)
            if 'hours' in chunk.columns:
                chunk['hours'] = chunk['hours'].astype(str)
            # --- 💡 NEW LINES END 💡 ---

            # Now, write this cleaned chunk to the 'business' table
            chunk.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
            
            total_rows += len(chunk)
            print(f"Processed chunk {i + 1} ({total_rows} total rows)")

        print(f"\n--- Success! ---")
        print(f"Finished importing {total_rows} rows into '{TABLE_NAME}' table.")
        print(f"Your database is ready: '{DATABASE_FILE}'")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    finally:
        conn.close()

# --- This makes the script runnable ---
if __name__ == "__main__":
    import_business_data()