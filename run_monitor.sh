#!/bin/bash

# Build and run the Go monitor
echo "Building Go crypto monitor..."
go build -o crypto_monitor crypto_monitor.go

echo "Starting crypto monitor..."
./crypto_monitor &
MONITOR_PID=$!

echo "Monitor started with PID: $MONITOR_PID"

# Wait for some data to be collected
echo "Waiting for data collection (30 seconds)..."
sleep 30

# Generate initial charts
echo "Generating initial charts..."
python3 chart_generator.py --summary

echo "Monitor is running in background (PID: $MONITOR_PID)"
echo "Run 'python3 chart_generator.py' to generate updated charts"
echo "Run 'kill $MONITOR_PID' to stop the monitor"

# Save PID to file for easy management
echo $MONITOR_PID > monitor.pid