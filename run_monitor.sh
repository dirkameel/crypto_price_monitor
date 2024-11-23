#!/bin/bash
# Script to run the cryptocurrency monitor

echo "Starting Cryptocurrency Price Monitor..."
echo "Press Ctrl+C to stop the monitor"

# Build and run the Go monitor
go build -o crypto_monitor crypto_monitor.go
./crypto_monitor