#!/bin/bash

# Exit immediately on errors
set -e

mkdir -p /home/ubuntu/search_manual/logs
#echo "Launcher triggered at: $(date)" >> /home/ubuntu/search_manual/logs/searchManual_launcher_trace.log

# Define project directory
PROJECT_DIR=/home/ubuntu/search_manual/
LOG_DIR="$PROJECT_DIR/logs"

# Navigate to project directory
cd "$PROJECT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install toml
pip uninstall fitz PyMuPDF -y
pip install -r requirements.txt

# Run Flask server in background, logging output
nohup python3 flask_autoServer.py > "$LOG_DIR/flask.log" 2>&1 &

# Run Streamlit client in background, logging output
nohup streamlit run st_autoManual.py --server.port 8503 > "$LOG_DIR/streamlit.log" 2>&1 &