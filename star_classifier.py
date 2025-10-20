import pandas as pd
import sqlite3
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# --- Configuration ---
DATABASE_FILE = 'yelp.db'
MODEL_FILE = 'star_classifier.joblib'
# ---------------------

def train_model():
    """
    This is an OFFLINE script.
    It loads a subset of the data, trains a machine learning pipeline,
    evaluates it, and saves the final model to a file for the API to use.
    """
    print(f"Connecting to {DATABASE_FILE}...")
    conn = sqlite3.connect(DATABASE_FILE)

    # 1. Load Data
    # We only use 1-star and 5-star reviews to create a clear
    # binary classification problem: "is this review extremely positive or negative?"
    print("Loading 1-star and 5-star reviews (this will take a minute)...")
    start_time = time.time()
    query = "SELECT text, stars FROM review WHERE stars = 1 OR stars = 5"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Simple data cleaning: ensure text is a string and stars are integers.
    df['text'] = df['text'].fillna('').astype(str)
    df['stars'] = df['stars'].astype(int)

    print(f"Loaded {len(df):,} rows in {time.time() - start_time:.2f}s")
    
    if len(df) < 1000:
        print("Error: Not enough data to train. Need at least 1000 rows.")
        return

    # 2. Split Data
    # We hold back 20% of the data to test the model's performance on unseen reviews.
    X = df['text']
    y = df['stars']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training on {len(X_train):,} reviews, testing on {len(X_test):,} reviews.")

    # 3. Define the Pipeline
    # A Pipeline is CRITICAL. It bundles the text vectorizer and the classifier
    # into a single object. This ensures the exact same process is used for
    # training and prediction, preventing data leakage.
    print("Defining pipeline: TfidfVectorizer -> LogisticRegression")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            stop_words='english',
            max_features=15000,  # Limit vocabulary size to keep the model file manageable
            ngram_range=(1, 2)   # Look for both single words and two-word phrases
        )),
        ('model', LogisticRegression(
            solver='saga',       # A good, fast solver for large datasets
            max_iter=200,        # Increase iterations for better convergence
            random_state=42,
            n_jobs=-1            # Use all available CPU cores
        ))
    ])

    # 4. Train the model
    print("Training model... this is the heavy part and will take several minutes.")
    start_time = time.time()
    pipeline.fit(X_train, y_train)
    print(f"Training complete in {time.time() - start_time:.2f}s")

    # 5. Evaluate the model
    # How well did it do on the unseen test data?
    print("\n--- Model Evaluation on Test Set ---")
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)
    print("------------------------------------")

    # 6. Save the trained pipeline to disk
    # joblib is the standard way to save sklearn models.
    print(f"Saving trained model pipeline to '{MODEL_FILE}'...")
    joblib.dump(pipeline, MODEL_FILE, compress=3) # Add compression to reduce file size
    print(f"--- ✅ Model saved successfully! ---")


if __name__ == "__main__":
    train_model()
