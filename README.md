# Cryptocurrency Price Monitor & Chart Generator

A dual-language solution using Go for real-time cryptocurrency price monitoring and Python for data visualization.

## Prerequisites

- Go 1.16+
- Python 3.8+
- Internet connection

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Go is installed and configured**

## Quick Start

### Method 1: Automated Script (Recommended)
```bash
# Make the script executable
chmod +x run_monitor.sh

# Run the complete system
./run_monitor.sh
```

### Method 2: Manual Steps

1. **Start the Go monitor:**
   ```bash
   go run crypto_monitor.go
   ```
   Or build and run:
   ```bash
   go build -o crypto_monitor crypto_monitor.go
   ./crypto_monitor
   ```

2. **Generate charts with Python:**
   ```bash
   python3 chart_generator.py
   ```

## Configuration

Edit `config.json` to customize:

- `symbols`: Cryptocurrencies to monitor (use CoinCap API symbols)
- `interval`: Data collection interval in seconds
- `output_file`: Where to store collected data

Example configuration:
```json
{
  "symbols": ["bitcoin", "ethereum", "cardano", "solana"],
  "interval": 60,
  "output_file": "crypto_data.json"
}
```

## Usage Examples

### Basic Chart Generation
```bash
python3 chart_generator.py
```

### Generate Charts with Summary
```bash
python3 chart_generator.py --summary
```

### Custom Input/Output Files
```bash
python3 chart_generator.py --input my_data.json --output my_chart.png
```

### View Only Summary
```bash
python3 chart_generator.py --summary --output /dev/null
```

## Features

- **Real-time Monitoring**: Go service fetches prices at configurable intervals
- **Data Persistence**: All price data saved to JSON file
- **Interactive Charts**: Python generates matplotlib charts with current prices
- **Multi-currency Support**: Monitor multiple cryptocurrencies simultaneously
- **Price Change Tracking**: Shows percentage changes from start of monitoring

## File Structure

- `crypto_monitor.go` - Go service for price monitoring
- `config.json` - Configuration file
- `chart_generator.py` - Python script for chart generation
- `run_monitor.sh` - Automation script
- `requirements.txt` - Python dependencies
- `crypto_data.json` - Generated data file (created by Go monitor)
- `crypto_charts.png` - Generated chart file (created by Python script)

## Stopping the Monitor

If using the automated script:
```bash
kill $(cat monitor.pid)
```

If running manually, use Ctrl+C in the terminal where the Go monitor is running.

## Supported Cryptocurrencies

Use any cryptocurrency symbol supported by the CoinCap API v2. Common examples:
- `bitcoin`, `ethereum`, `cardano`, `solana`, `polkadot`, `dogecoin`

## Troubleshooting

1. **No data in charts**: Ensure the Go monitor has been running for at least one interval
2. **API errors**: Check internet connection and verify cryptocurrency symbols
3. **Chart generation fails**: Ensure all Python dependencies are installed
4. **Permission denied**: Make `run_monitor.sh` executable with `chmod +x run_monitor.sh`

## API Notes

This solution uses the free CoinCap API v2. Be mindful of rate limits for extended monitoring.