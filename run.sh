#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

VENV_DIR=".venv"

echo "🚀 Setting up NiceGUI Environment..."

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Clean Python cache to prevent stale bytecode issues
echo "🧹 Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Update pip and install/verify dependencies
echo "📥 Checking dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
pip install -e ./nd-solarized

echo "✨ Starting NiceGUI with Hot Reload..."
echo "📂 Watching: test/, nice_design/, and nd-solarized/"

# Run the application with watchfiles to restart when either the app 
# or the library code (including CSS/Assets) changes.
python3 -m watchfiles "python3 test/main.py" test nice_design nd-solarized
