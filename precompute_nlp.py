import pandas as pd
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from tqdm import tqdm
import numpy as np

DATABASE_FILE = 'yelp.db'

def get_top_keywords(texts, n_terms=5):
    """
    Uses TF-IDF to extract top keywords from a list of texts.
    Returns a list of top n_terms keywords (strings).
    """
    if not texts:
        return []

    # Simple text cleaning: remove non-alphanumeric, lower, strip
    clean_texts = [re.sub(r'[^a-zA-Z0-9\s]', '', t).lower().strip() for t in texts]

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=1000
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(clean_texts)
    except ValueError:
        return []

    feature_names = vectorizer.get_feature_names_out()
    # convert sparse matrix sum to a flat numpy array
    summed_tfidf = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
    top_n_indices = summed_tfidf.argsort()[-n_terms:]
    top_n_indices = top_n_indices[::-1]
    return [feature_names[i] for i in top_n_indices]

def precompute_nlp_data():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 1. Create the new table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_nlp (
        business_id TEXT PRIMARY KEY,
        positivity_score REAL,
        positive_keywords TEXT,
        negative_keywords TEXT
    );
    """)

    # 2. Get all businesses to loop over
    business_df = pd.read_sql("SELECT business_id, name FROM business", conn)

    # 3. Load VADER
    sia = SentimentIntensityAnalyzer()

    print(f"Starting NLP pre-computation for {len(business_df)} businesses...")

    # 4. Loop through every business (use tqdm for a progress bar)
    for index, row in tqdm(business_df.iterrows(), total=business_df.shape[0]):
        business_id = row['business_id']

        # a. Fetch all reviews for this business_id
        reviews_df = pd.read_sql("SELECT text, stars FROM review WHERE business_id = ?", conn, params=(business_id,))

        # b. Calculate positivity_score (handle 0 reviews!)
        positivity_score = 0.0
        if not reviews_df.empty:
            # ensure text column is string and fill missing
            texts_series = reviews_df['text'].fillna('').astype(str)
            scores = texts_series.apply(lambda t: sia.polarity_scores(t)['compound'])
            positivity_score = float(scores.mean()) if not scores.empty else 0.0

        # c. Calculate keywords (handle 0 reviews!)
        positive_texts = []
        negative_texts = []
        if not reviews_df.empty:
            positive_texts = reviews_df[reviews_df['stars'].isin([4, 5])]['text'].dropna().astype(str).tolist()
            negative_texts = reviews_df[reviews_df['stars'].isin([1, 2])]['text'].dropna().astype(str).tolist()

        pos_keywords_list = get_top_keywords(positive_texts)
        neg_keywords_list = get_top_keywords(negative_texts)

        # ensure keywords are strings before joining
        pos_keywords_str = ",".join(map(str, pos_keywords_list))
        neg_keywords_str = ",".join(map(str, neg_keywords_list))

        # e. Insert results into the new table
        cursor.execute(
            """
            INSERT OR REPLACE INTO business_nlp (business_id, positivity_score, positive_keywords, negative_keywords)
            VALUES (?, ?, ?, ?)
            """,
            (business_id, positivity_score, pos_keywords_str, neg_keywords_str),
        )

    # 5. Commit all changes and close
    conn.commit()
    conn.close()
    print("NLP pre-computation complete.")

if __name__ == "__main__":
    precompute_nlp_data()