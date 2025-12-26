#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

VENV_DIR=".venv"
PORT=8080
PID_FILE=".nicegui.pid"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    # Kill the watchfiles process and its children
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            # Kill process group
            PGRP=$(ps -o pgid= -p "$PID" | tr -d ' ')
            if [ ! -z "$PGRP" ]; then
                kill -TERM -"$PGRP" 2>/dev/null || true
                sleep 0.5
                kill -KILL -"$PGRP" 2>/dev/null || true
            else
                kill "$PID" 2>/dev/null || true
            fi
        fi
        rm -f "$PID_FILE"
    fi
    # Final port cleanup
    fuser -k -9 $PORT/tcp 2>/dev/null || true
    echo "✨ Cleanup complete"
    exit 0
}

# Set up trap to catch SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM EXIT

echo "�🚀 Setting up NiceGUI Environment..."

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
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install -e . -q

# Kill any processes using the port
echo "🔍 Checking for processes on port $PORT..."
fuser -k $PORT/tcp 2>/dev/null || true
sleep 0.2
lsof -t -i :$PORT | xargs kill -9 2>/dev/null || true

# Wait for port to be released (max 5 seconds)
for i in {1..20}; do
    if ! lsof -i :$PORT > /dev/null 2>&1; then
        break
    fi
    echo "⏳ Waiting for port $PORT to be released... ($i/20)"
    fuser -k -9 $PORT/tcp 2>/dev/null || true
    sleep 0.25
done


# Final check
if lsof -i :$PORT > /dev/null 2>&1; then
    echo "❌ Port $PORT is still in use after cleanup attempt!"
    echo "Run this command manually to see what's using it:"
    echo "   lsof -i :$PORT"
    exit 1
fi

echo "✅ Port $PORT is available"
echo "✨ Starting NiceGUI with Hot Reload..."
echo "📂 Watching: test/, nice_design/"

# Run the application with watchfiles to restart when either the app 
# or the library code (including CSS/Assets) changes.
# We add a small sleep before the start to ensure the port is fully released by the OS.
python3 -m watchfiles "sh -c 'sleep 0.1 && python3 test/main.py'" test nice_design &

# Save the PID
echo $! > "$PID_FILE"

# Wait for the background process
wait $!
