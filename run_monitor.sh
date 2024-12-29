#!/bin/bash

# Cryptocurrency Monitor Startup Script

echo "Starting Cryptocurrency Monitoring System..."

# Check if Go and Python are installed
if ! command -v go &> /dev/null; then
    echo "Error: Go is not installed or not in PATH"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install matplotlib

# Create data directory if it doesn't exist
mkdir -p data

echo "Starting Go monitor in background..."
go run crypto_monitor.go &

echo "Starting Python chart generator..."
python3 chart_generator.py

# Cleanup when script exits
trap "pkill -f 'go run crypto_monitor.go'; exit" INT