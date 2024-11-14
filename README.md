# Cryptocurrency Price Monitor & Chart Generator

A two-part system for monitoring cryptocurrency prices and generating charts:
- **Go script**: Continuously monitors prices and saves data
- **Python script**: Generates various charts from collected data

## Prerequisites

- Go 1.19 or later
- Python 3.8 or later
- Internet connection (for API calls)

## Installation

1. **Clone or download the files** to a directory

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Run the Go Monitor

Start monitoring cryptocurrency prices:

```bash
go run crypto_monitor.go
```

The monitor will:
- Fetch prices every minute for Bitcoin, Ethereum, Cardano, Solana, and Polkadot
- Display current prices in the console
- Save data to JSON files in the `data/` directory
- Run continuously until stopped with `Ctrl+C`

### Step 2: Generate Charts

After collecting some data, run the Python chart generator:

```bash
python crypto_charts.py
```

You'll be prompted to choose from three chart types:

1. **Current Price Comparison**: Bar chart showing current prices
2. **Price History**: Line chart showing price trends over time
3. **Performance Chart**: Bar chart showing percentage changes

## File Structure

```
.
├── crypto_monitor.go    # Go script for price monitoring
├── crypto_charts.py     # Python script for chart generation
├── go.mod              # Go module file
├── requirements.txt    # Python dependencies
└── data/              # Directory for price data (created automatically)
    ├── crypto_prices_YYYYMMDD.json
    └── latest_prices.json
```

## Customization

### Adding More Cryptocurrencies

Edit the `cryptos` slice in `crypto_monitor.go`:

```go
cryptos := []string{"bitcoin", "ethereum", "cardano", "solana", "polkadot", "dogecoin"}
```

### Changing Update Interval

Modify the sleep duration in `crypto_monitor.go`:

```go
// For 30-second updates:
time.Sleep(30 * time.Second)
```

### Modifying Chart Styles

Edit the color schemes and styling in `crypto_charts.py` in the `create_*_chart` methods.

## Notes

- The Go monitor uses the free CoinGecko API
- Data is saved locally in JSON format
- Historical charts require at least a few minutes of monitoring data
- The system keeps only the last 100 data points to prevent large files

## Troubleshooting

- **No data files**: Ensure the Go monitor has been running for at least one minute
- **API errors**: Check your internet connection and CoinGecko API status
- **Chart display issues**: Verify matplotlib is properly installed in your Python environment

Enjoy monitoring your cryptocurrency investments! 📈