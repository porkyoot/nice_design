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

# Update pip and install/verify dependencies
echo "📥 Checking dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ..

echo "✨ Starting NiceGUI with Hot Reload..."
echo "📂 Watching: test/ and nice_design/"

# Run the application with watchfiles to restart when either the app 
# or the library code (including CSS/Assets) changes.
python3 -m watchfiles "python3 main.py" . ../nice_design
