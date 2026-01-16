#!/bin/bash

# YouTube Learning Assistant - Quick Start Script

echo "🎓 Starting YouTube Learning Assistant..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/Update dependencies
echo "Checking dependencies..."
pip install -r requirements.txt --quiet

# Run the application
echo ""
echo "✅ Launching application..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
