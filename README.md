End-to-End Restaurant Insights DashboardA full-stack data pipeline that analyzes a 10GB, 7-million-review Yelp dataset to provide instant, actionable insights for restaurant owners.GitHub Repo: Anurag-Kumar9/yelp-insights-dashboardLive Demo GIF(A short, 10-second GIF of you using the final dashboard. Show yourself pasting an ID, clicking search, and the results appearing instantly. This is the single most effective way to make your project look professional. Use a tool like ScreenToGif or Kap.)The ProblemAnalyzing millions of user reviews is computationally expensive and slow. A real-time dashboard that runs live NLP and clustering would be unusable, taking minutes or hours to load. This project solves the challenge of serving complex data insights from a massive dataset with millisecond latency.The Architecture: Offline Pre-computationThe core of this project is a robust data engineering pipeline that separates heavy offline computation from the lightweight online API.graph TD
    subgraph "OFFLINE: One-Time Batch Jobs (Hours)"
        direction LR
        A[Raw Yelp JSON<br/>(10GB)] --> B(ETL and Indexing Scripts<br/>ingest_*.py, create_index.py);
        B --> C((SQLite DB<br/>yelp.db));
        C --> D[Offline Pre-computation Scripts<br/>precompute_*.py, train_classifier.py];
        D --> E((Pre-computed Tables<br/>business_nlp<br/>user_clusters));
        D --> F[ML Model File<br/>star_classifier.joblib];
    end

    subgraph "ONLINE: Real-Time Serving (Milliseconds)"
        direction LR
        H{FastAPI Server<br/>main.py} <--> I[User Dashboard<br/>(Browser)];
    end
    
    %% Connections between stages
    C -- Fast Read --> H;
    E -- Fast Read --> H;
    F -- Load on Startup --> H;

    %% Styling
    style A fill:#D2B48C,stroke:#333,stroke-width:2px
    style C fill:#ADD8E6,stroke:#333,stroke-width:2px
    style E fill:#ADD8E6,stroke:#333,stroke-width:2px
    style F fill:#90EE90,stroke:#333,stroke-width:2px
    style I fill:#F0E68C,stroke:#333,stroke-width:2px
The Money Shot: The 43-Day ProblemThe initial offline NLP script had a critical performance bottleneck. Due to an N+1 query pattern on the 7-million-row review table without an index, each business took ~25 seconds to process.Projected Runtime: 150,000 businesses * 25 sec/business = 43 days.Diagnosis: Full table scans were being performed on every lookup.Solution: I created a database index on review(business_id) using a one-time script (create_index.py).Result: The query time dropped from 25 seconds to ~0.05 seconds. The total pre-computation time fell from 43 days to 2 hours, a 500x performance increase.How to Run This ProjectPrerequisites: You must download the official Yelp Open Dataset JSON files and place them in the root of this repository.Setup:# Clone the repo
git clone [https://github.com/Anurag-Kumar9/yelp-insights-dashboard.git](https://github.com/Anurag-Kumar9/yelp-insights-dashboard.git)
cd yelp-insights-dashboard

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Run Offline Scripts (This will take ~3-4 hours):# 1. Ingest the raw data (run these three in order)
python ingest_business.py
python ingest_review.py
python ingest_user.py

# 2. Create the critical database index
python create_index.py

# 3. Pre-compute the clusters and NLP data
python precompute_clusters.py
python precompute_nlp.py

# 4. Train the classification model
python train_classifier.py
Run the API Server:uvicorn main:app --reload
The dashboard will be available at http://12-7.0.0.1:8000.