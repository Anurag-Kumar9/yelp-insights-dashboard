import joblib

# --- Configuration ---
MODEL_FILE = 'star_classifier.joblib'
POSITIVE_TEXT = "This was the best meal of my life, the service was fast and the food was amazing."
NEGATIVE_TEXT = "I will never return, the waiter was rude and my food was cold and disgusting."
# ---------------------

def test_model_directly():
    """
    Loads the saved model file and tests it on two sample sentences
    to see if the model itself is the problem.
    """
    print(f"--- Direct Model Debugger ---")
    try:
        model = joblib.load(MODEL_FILE)
        print(f"Successfully loaded '{MODEL_FILE}'")
    except FileNotFoundError:
        print(f"ERROR: '{MODEL_FILE}' not found. Cannot debug.")
        return
    except Exception as e:
        print(f"An error occurred loading the model: {e}")
        return

    # --- Test 1: The Positive Review ---
    print(f"\n[1] Testing Positive Text: '{POSITIVE_TEXT}'")
    
    # We must wrap the string in a list, just like the API does
    pos_pred = model.predict([POSITIVE_TEXT])
    pos_proba = model.predict_proba([POSITIVE_TEXT])
    
    print(f"    -> Prediction: {pos_pred[0]} star(s)")
    print(f"    -> Probabilities (1-star, 5-star): {pos_proba[0]}")
    print(f"    -> Confidence: {pos_proba.max():.2f}")

    # --- Test 2: The Negative Review ---
    print(f"\n[2] Testing Negative Text: '{NEGATIVE_TEXT}'")
    
    neg_pred = model.predict([NEGATIVE_TEXT])
    neg_proba = model.predict_proba([NEGATIVE_TEXT])
    
    print(f"    -> Prediction: {neg_pred[0]} star(s)")
    print(f"    -> Probabilities (1-star, 5-star): {neg_proba[0]}")
    print(f"    -> Confidence: {neg_proba.max():.2f}")


if __name__ == "__main__":
    test_model_directly()