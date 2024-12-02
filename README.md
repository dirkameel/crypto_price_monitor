## Cryptocurrency Price Monitor & Chart Display

This project consists of a Go-based cryptocurrency price monitor and a Python-based chart display system.

### Prerequisites

1. **Go** (1.16 or higher)
2. **Python** (3.7 or higher)
3. **Python packages**: matplotlib, pandas

### Installation

1. **Install Go dependencies** (none required - uses standard library)
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Step 1: Run the Price Monitor

**Option A - Using the shell script:**
```bash
chmod +x run_monitor.sh
./run_monitor.sh
```

**Option B - Manual execution:**
```bash
go run crypto_monitor.go
```

The monitor will:
- Fetch prices for Bitcoin, Ethereum, Cardano, Solana, and Polkadot every 60 seconds
- Display current prices in the console
- Save price history to `crypto_prices.json`

#### Step 2: Display Charts

After the monitor has collected some data, run the Python charting script:

**Basic usage (shows combined chart):**
```bash
python crypto_charts.py
```

**Show only price table:**
```bash
python crypto_charts.py --table
```

**Show combined chart of all cryptocurrencies:**
```bash
python crypto_charts.py --combined
```

**Show individual charts for each cryptocurrency:**
```bash
python crypto_charts.py --individual
```

**Show table and combined chart:**
```bash
python crypto_charts.py --table --combined
```

### Features

**Go Monitor:**
- Real-time price monitoring from CoinGecko API
- Automatic data persistence to JSON file
- Configurable update interval (currently 60 seconds)
- Keeps last 100 price points for each cryptocurrency

**Python Charts:**
- Individual price charts for each cryptocurrency
- Combined comparison chart
- Price table with percentage changes
- Interactive matplotlib charts
- Command-line options for different display modes

### File Structure

- `crypto_monitor.go` - Main Go application for price monitoring
- `crypto_charts.py` - Python script for chart visualization
- `run_monitor.sh` - Convenience script to run the monitor
- `requirements.txt` - Python dependencies
- `crypto_prices.json` - Generated data file (created by monitor)

### Customization

**To monitor different cryptocurrencies:**
Edit the `cryptos` slice in `crypto_monitor.go`:

```go
cryptos := []string{"bitcoin", "ethereum", "litecoin", "ripple"}
```

**To change update frequency:**
Modify the sleep duration in `crypto_monitor.go`:
```go
time.Sleep(30 * time.Second) // Update every 30 seconds
```

### Notes

- The application uses the free CoinGecko API (no API key required)
- Internet connection is required for price monitoring
- Charts will only show data after the monitor has been running for some time
- Press `Ctrl+C` to stop the Go monitor

### Troubleshooting

- If you get rate limit errors, increase the sleep interval in the Go code
- Ensure you have an active internet connection
- Make sure all dependencies are installed correctly
- Check that the `crypto_prices.json` file is being created and updated