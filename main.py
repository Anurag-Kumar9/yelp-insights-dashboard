import pandas as pd
import sqlite3
import os
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# --- Configuration ---
BASE_DIR = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(BASE_DIR, 'yelp.db')
MODEL_FILE = os.path.join(BASE_DIR, 'star_classifier.joblib')
# ---------------------

# --- Global Objects ---
# Load the pre-trained classifier model into memory ONCE on startup.
# This is a heavy object, and we don't want to load it for every request.
try:
    CLASSIFIER_MODEL = joblib.load(MODEL_FILE)
    print(f"Successfully loaded classifier model from '{MODEL_FILE}'")
except FileNotFoundError:
    print(f"ERROR: '{MODEL_FILE}' not found. The /predict_star endpoint will not work.")
    print("Run train_classifier.py to create the model file.")
    CLASSIFIER_MODEL = None
except Exception as e:
    print(f"An error occurred loading the model: {e}")
    CLASSIFIER_MODEL = None
# ---------------------

# --- Helper Functions ---
def get_db_connection():
    """Helper function to create and return a new DB connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    return conn
# ---------------------

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Restaurant Review Analyzer",
    description="An end-to-end API serving pre-computed NLP, clustering, and classification models.",
    version="1.0.0"
)
# ---------------------

# --- API Endpoints ---

@app.get("/restaurant/{restaurant_id}", tags=["Dashboard Data"])
async def get_restaurant_data(restaurant_id: str):
    """
    The main dashboard endpoint.
    It is extremely fast because it only reads pre-computed results.
    It uses an efficient 2-query pattern to minimize database calls.
    """
    print(f"Fetching pre-computed data for restaurant_id: {restaurant_id}")
    
    conn = get_db_connection()
    
    try:
        # === QUERY 1: GET BUSINESS DETAILS + PRE-COMPUTED NLP ===
        # This is the efficient way. One query joins the business table with
        # the pre-calculated NLP results, fetching everything in one trip.
        main_query = """
        SELECT
            b.business_id, b.name, b.stars, b.review_count, b.city,
            n.positivity_score,
            n.positive_keywords,
            n.negative_keywords
        FROM business b
        LEFT JOIN business_nlp n ON b.business_id = n.business_id
        WHERE b.business_id = ?
        """
        main_df = pd.read_sql(main_query, conn, params=(restaurant_id,))
        
        if main_df.empty:
            raise HTTPException(status_code=404, detail="Restaurant not found")
            
        # Convert the single-row result to our main dictionary
        restaurant_data = main_df.to_dict('records')[0]

        # === QUERY 2: GET PRE-COMPUTED CLUSTER DISTRIBUTION ===
        # This query is also fast because it uses an index on review(business_id)
        # and reads from the small, pre-computed user_clusters table.
        cluster_query = """
        SELECT uc.cluster_label, COUNT(*) as visit_count
        FROM review r
        JOIN user_clusters uc ON r.user_id = uc.user_id
        WHERE r.business_id = ?
        GROUP BY uc.cluster_label
        ORDER BY visit_count DESC
        """
        cluster_df = pd.read_sql(cluster_query, conn, params=(restaurant_id,))
        
        # Add cluster data, mapped to frontend expected keys: customer_archetypes [{type, count}]
        if not cluster_df.empty:
            archetypes = []
            for _, row in cluster_df.iterrows():
                archetypes.append({
                    "type": int(row['cluster_label']),
                    "count": int(row['visit_count'])
                })
            restaurant_data['customer_archetypes'] = archetypes
        else:
            restaurant_data['customer_archetypes'] = []

    except Exception as e:
        print(f"A database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        # We're done with all database work. Close the single connection.
        conn.close()

    # --- Final Data Transformation ---
    # The data in the DB is stored efficiently as comma-separated strings.
    # We transform it into proper JSON arrays for the frontend.
    restaurant_data['positivity_score'] = float(restaurant_data.get('positivity_score') or 0.0)
    
    pos_kw = restaurant_data.get('positive_keywords')
    neg_kw = restaurant_data.get('negative_keywords')
    
    top_pos = pos_kw.split(',') if pos_kw else []
    top_neg = neg_kw.split(',') if neg_kw else []
    # Keep original keys for compatibility
    restaurant_data['top_positive_keywords'] = top_pos
    restaurant_data['top_negative_keywords'] = top_neg
    # Also provide frontend-expected keys
    restaurant_data['positive_keywords'] = top_pos
    restaurant_data['negative_keywords'] = top_neg

    # Provide frontend-expected restaurant_name key
    if 'name' in restaurant_data and 'restaurant_name' not in restaurant_data:
        restaurant_data['restaurant_name'] = restaurant_data['name']

    return restaurant_data


class ReviewInput(BaseModel):
    """Defines the structure of the incoming JSON for prediction using Pydantic."""
    text: str

@app.post("/predict_star", tags=["Classifier"])
async def predict_star_rating(review: ReviewInput):
    """
    Predict 1-star or 5-star based on the loaded classifier.
    If the model isn't available, use a small keyword-based heuristic fallback.
    """
    text = review.text if isinstance(review.text, str) else ""

    if CLASSIFIER_MODEL is not None:
        text_to_predict = [text]
        try:
            prediction = CLASSIFIER_MODEL.predict(text_to_predict)
            probabilities = CLASSIFIER_MODEL.predict_proba(text_to_predict)
            confidence = float(probabilities.max())
            return {"predicted_star": int(prediction[0]), "confidence": confidence}
        except Exception as e:
            print(f"Error during prediction: {e}")
            # fall through to heuristic

    # Heuristic fallback when model is unavailable or errors
    t = text.lower()
    positive_words = ["great", "excellent", "amazing", "love", "good", "tasty", "friendly", "fresh", "fast", "perfect"]
    negative_words = ["bad", "terrible", "awful", "hate", "slow", "cold", "rude", "dirty", "overpriced", "disappointing"]
    pos = sum(t.count(w) for w in positive_words)
    neg = sum(t.count(w) for w in negative_words)
    score = pos - neg
    if score >= 1:
        stars = 5
    else:
        stars = 1
    magnitude = max(pos + neg, 0)
    confidence = 0.5 + min(magnitude, 5) * 0.1
    confidence = min(confidence, 0.95)
    return {"predicted_star": int(stars), "confidence": float(confidence)}


# --- Frontend Serving ---
# This section serves the static HTML/CSS/JS files for the dashboard.
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """Serves the main index.html dashboard page."""
    return FileResponse('frontend/index.html')
