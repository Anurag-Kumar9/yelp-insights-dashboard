#!/bin/bash

# Yelp Insights Dashboard - Quick Start Script
# This script helps you set up the project quickly

set -e  # Exit on error

echo "🍽️  Yelp Insights Dashboard - Quick Start"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Check for required files
echo ""
echo "📂 Checking for Yelp dataset files..."
MISSING_FILES=0

if [ ! -f "yelp_academic_dataset_business.json" ]; then
    echo -e "${YELLOW}⚠️  Missing: yelp_academic_dataset_business.json${NC}"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ ! -f "yelp_academic_dataset_review.json" ]; then
    echo -e "${YELLOW}⚠️  Missing: yelp_academic_dataset_review.json${NC}"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ ! -f "yelp_academic_dataset_user.json" ]; then
    echo -e "${YELLOW}⚠️  Missing: yelp_academic_dataset_user.json${NC}"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ $MISSING_FILES -gt 0 ]; then
    echo ""
    echo -e "${RED}❌ Missing $MISSING_FILES dataset file(s)${NC}"
    echo ""
    echo "📥 Download the Yelp Open Dataset from:"
    echo "   https://www.yelp.com/dataset"
    echo ""
    echo "📁 Place the JSON files in this directory:"
    echo "   $(pwd)"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ All dataset files found${NC}"

# Create virtual environment
echo ""
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "restaurent" ]; then
    python3 -m venv restaurent
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}ℹ️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source restaurent/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Ask user if they want to run the full pipeline
echo ""
echo "⚙️  Setup Options:"
echo ""
echo "1. Run FULL pipeline (recommended for first-time setup)"
echo "   - ETL ingestion (~30-45 min)"
echo "   - Create indexes (~5 min)"
echo "   - User clustering (~10-15 min)"
echo "   - NLP processing (~60-90 min)"
echo "   - Train ML model (~5-10 min)"
echo "   Total time: ~2-4 hours"
echo ""
echo "2. Run QUICK setup (for testing/development)"
echo "   - Skip data processing"
echo "   - Start server immediately"
echo "   - Requires existing database"
echo ""
echo "3. Exit (manual setup)"
echo ""
read -p "Choose option (1/2/3): " SETUP_CHOICE

case $SETUP_CHOICE in
    1)
        echo ""
        echo "🚀 Starting FULL pipeline setup..."
        echo "⏱️  This will take approximately 2-4 hours. Grab some coffee! ☕"
        echo ""
        
        echo "Step 1/5: Ingesting business data..."
        python ingest_business.py
        
        echo "Step 2/5: Ingesting review data..."
        python ingest_review.py
        
        echo "Step 3/5: Ingesting user data..."
        python ingest_user.py
        
        echo "Step 4/5: Creating database indexes..."
        python create_index.py
        
        echo "Step 5/5: Pre-computing user clusters..."
        python precompute_clusters.py
        
        echo "Step 6/7: Pre-computing NLP features..."
        python precompute_nlp.py
        
        echo "Step 7/7: Training star classifier..."
        python star_classifier.py
        
        echo -e "${GREEN}✅ Pipeline completed successfully!${NC}"
        echo ""
        echo "🎉 Setup complete! Starting the server..."
        echo ""
        echo "📊 Dashboard will be available at: http://127.0.0.1:8000"
        echo "📚 API docs will be available at: http://127.0.0.1:8000/docs"
        echo ""
        uvicorn main:app --reload
        ;;
        
    2)
        echo ""
        if [ ! -f "yelp.db" ]; then
            echo -e "${RED}❌ Database not found. Please run the full setup (option 1) first.${NC}"
            exit 1
        fi
        
        echo "🚀 Starting server in QUICK mode..."
        echo ""
        echo "📊 Dashboard: http://127.0.0.1:8000"
        echo "📚 API docs: http://127.0.0.1:8000/docs"
        echo ""
        uvicorn main:app --reload
        ;;
        
    3)
        echo ""
        echo "📖 For manual setup, follow the instructions in README.md"
        echo ""
        echo "Quick commands:"
        echo "  source restaurent/bin/activate"
        echo "  python ingest_business.py"
        echo "  python ingest_review.py"
        echo "  python ingest_user.py"
        echo "  python create_index.py"
        echo "  python precompute_clusters.py"
        echo "  python precompute_nlp.py"
        echo "  python star_classifier.py"
        echo "  uvicorn main:app --reload"
        echo ""
        exit 0
        ;;
        
    *)
        echo -e "${RED}❌ Invalid option${NC}"
        exit 1
        ;;
esac
