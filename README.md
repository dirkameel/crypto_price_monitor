.md

# Cryptocurrency Price Monitor & Chart Generator

A dual-language application that uses Go for real-time cryptocurrency price monitoring and Python for data visualization.

## Features

- **Real-time Monitoring**: Fetches current prices for major cryptocurrencies every 60 seconds
- **Data Persistence**: Saves price data to JSON file for historical tracking
- **Visual Charts**: Generates bar charts and trend line charts
- **Performance Summary**: Shows percentage changes over monitoring period
- **Multi-crypto Support**: Monitors Bitcoin, Ethereum, Cardano, Solana, and Polkadot

## Prerequisites

- Go 1.16 or higher
- Python 3.8 or higher
- Internet connection (for API calls)

## Installation & Setup

1. **Clone or download the files** to your desired directory

2. **Make the shell script executable** (Linux/Mac):
   ```bash
   chmod +x run_monitor.sh
   ```

3. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

### Method 1: Using the Shell Script (Recommended)
```bash
./run_monitor.sh
```

### Method 2: Manual Execution

**Terminal 1 - Start Go Monitor:**
```bash
go run crypto_monitor.go
```

**Terminal 2 - Start Python Chart Generator:**
```bash
python3 chart_generator.py
```

## How It Works

1. **Go Application** (`crypto_monitor.go`):
   - Fetches real-time prices from CoinGecko API
   - Updates every 60 seconds
   - Saves data to `crypto_prices.json`
   - Displays current prices in terminal

2. **Python Application** (`chart_generator.py`):
   - Reads data from JSON file
   - Generates two types of charts:
     - `current_prices.png`: Bar chart of current prices
     - `price_trends.png`: Line chart showing price trends over time
   - Updates charts every 60 seconds

## Output Files

- `crypto_prices.json`: Current and historical price data
- `current_prices.png`: Bar chart of latest prices
- `price_trends.png`: Trend analysis chart

## Customization

### Add More Cryptocurrencies
Edit the `cryptos` slice in `crypto_monitor.go`:
```go
cryptos := []string{"bitcoin", "ethereum", "cardano", "solana", "polkadot", "dogecoin"}
```

### Change Update Interval
Modify the sleep duration in both files (currently 60 seconds):
```go
time.Sleep(60 * time.Second)  // In Go file
time.sleep(60)                // In Python file
```

## Stopping the Application

- Press `Ctrl+C` in each terminal
- If using the shell script, `Ctrl+C` will stop both processes

## Troubleshooting

- **API Rate Limits**: The app uses free CoinGecko API which has rate limits
- **Missing Dependencies**: Ensure all Python packages are installed
- **Network Issues**: Verify internet connectivity for API calls

## License

This project is for educational purposes. Feel free to modify and extend as needed.