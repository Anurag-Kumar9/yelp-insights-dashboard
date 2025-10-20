import argparse
import time
import sqlite3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def precompute_clusters(db_path: str = "yelp.db", k: int = 5, limit: int | None = None) -> None:
    """Load users from SQLite, cluster them and write cluster labels back to a new table.

    Args:
        db_path: path to sqlite database file.
        k: number of clusters for KMeans.
        limit: optional SQL LIMIT to use for quick testing.
    """
    features_list = ["review_count", "useful", "funny", "cool", "average_stars"]

    conn = sqlite3.connect(db_path)
    try:
        sql = (
            "SELECT user_id, review_count, useful, funny, cool, average_stars FROM user"
        )
        if limit is not None:
            sql = sql + f" LIMIT {int(limit)}"

        start = time.time()
        print(f"Loading users from {db_path}...")
        users_df = pd.read_sql_query(sql, conn)
        print(f"Loaded {len(users_df):,} rows in {time.time() - start:.2f}s")

        if users_df.empty:
            print("No user rows found. Exiting.")
            return

        # keep ids separate
        user_ids = users_df["user_id"].copy()
        user_features = users_df[features_list].copy()

        # enforce numeric and fill missing values with zeros (safe default for counts/ratings)
        user_features = user_features.apply(pd.to_numeric, errors="coerce").fillna(0)

        print("Scaling features...")
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(user_features)

        print(f"Running KMeans with k={k} (this may take a while on full data)...")
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        t0 = time.time()
        kmeans.fit(scaled_features)
        duration = time.time() - t0
        print(f"KMeans finished in {duration:.2f}s")

        labels = kmeans.labels_

        results_df = pd.DataFrame({"user_id": user_ids, "cluster_label": labels})

        print("Writing results to table 'user_clusters' (if_exists=replace)...")
        results_df.to_sql("user_clusters", conn, if_exists="replace", index=False)
        print("Write complete.")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Precompute user clusters and save to SQLite table 'user_clusters'.")
    parser.add_argument("--db", default="yelp.db", help="Path to sqlite3 database (default: yelp.db)")
    parser.add_argument("--k", type=int, default=5, help="Number of clusters (default: 5)")
    parser.add_argument("--limit", type=int, default=None, help="Optional LIMIT for quick runs (for testing)")

    args = parser.parse_args()

    start_all = time.time()
    precompute_clusters(db_path=args.db, k=args.k, limit=args.limit)
    print(f"Total elapsed: {time.time() - start_all:.2f}s")


if __name__ == "__main__":
    main()
