import pandas as pd
import sqlite3
import os
import time

# --- Configuration ---
JSON_FILE = 'yelp_academic_dataset_user.json' # ⚠️ Check this filename!
DATABASE_FILE = 'yelp.db'
TABLE_NAME = 'user'
CHUNK_SIZE = 100000 
# ---------------------

def import_user_data():
    """
    Reads the user.json file in chunks, flattens complex columns, 
    and appends it to the 'user' table.
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
    print("This is the last data file. Given your speed, it should be quick.")
    
    start_time = time.time()
    
    conn = sqlite3.connect(DATABASE_FILE)
    
    try:
        reader = pd.read_json(JSON_FILE, lines=True, chunksize=CHUNK_SIZE)
        
        total_rows = 0
        for i, chunk in enumerate(reader):
            
            # --- 💡 NEW FIX START 💡 ---
            # This is a more general fix than before.
            # It finds ALL columns of type 'object' (like dicts or lists)
            # and converts them to strings. 'user_id', 'name' etc. are
            # also 'object' type but .astype(str) doesn't hurt them.
            
            for col in chunk.columns:
                if chunk[col].dtype == 'object':
                    chunk[col] = chunk[col].astype(str)
            # --- 💡 NEW FIX END 💡 ---

            # This appends to the 'user' table
            chunk.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
            
            total_rows += len(chunk)
            elapsed_minutes = (time.time() - start_time) / 60
            
            print(f"Processed chunk {i + 1} ({total_rows:,} total rows) in {elapsed_minutes:.2f} minutes")

        end_time = time.time()
        print(f"\n--- ✅ Success! ---")
        print(f"Finished importing {total_rows:,} rows into '{TABLE_NAME}' table.")
        print(f"Total time: {(end_time - start_time) / 60:.2f} minutes.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    finally:
        conn.close()

# --- Main execution ---
if __name__ == "__main__":
    import_user_data()