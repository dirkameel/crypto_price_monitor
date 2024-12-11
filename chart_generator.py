#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import argparse
import sys

def load_crypto_data(filename):
    """Load cryptocurrency data from JSON file"""
    data = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line.strip()))
        return data
    except FileNotFoundError:
        print(f"Error: File {filename} not found. Make sure the Go monitor is running.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        sys.exit(1)

def generate_charts(data, output_file='crypto_charts.png'):
    """Generate price charts for different cryptocurrencies"""
    if not data:
        print("No data available to generate charts.")
        return
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')
    
    # Group by symbol
    symbols = df['symbol'].unique()
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Cryptocurrency Price Monitoring', fontsize=16, fontweight='bold')
    
    axes = axes.flatten()
    
    for i, symbol in enumerate(symbols):
        if i >= len(axes):
            break
            
        symbol_data = df[df['symbol'] == symbol]
        
        if len(symbol_data) > 0:
            axes[i].plot(symbol_data['datetime'], symbol_data['price'], 
                        marker='o', linewidth=2, markersize=4)
            axes[i].set_title(f'{symbol.upper()} Price', fontweight='bold')
            axes[i].set_ylabel('Price (USD)')
            axes[i].grid(True, alpha=0.3)
            
            # Format x-axis
            axes[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            axes[i].xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.setp(axes[i].xaxis.get_majorticklabels(), rotation=45)
            
            # Add current price annotation
            current_price = symbol_data['price'].iloc[-1]
            axes[i].annotate(f'Current: ${current_price:.2f}', 
                           xy=(1, 0), xycoords='axes fraction',
                           xytext=(-5, 5), textcoords='offset points',
                           ha='right', va='bottom',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
    
    # Hide empty subplots
    for i in range(len(symbols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Charts saved to {output_file}")
    plt.show()

def print_summary(data):
    """Print a summary of the collected data"""
    if not data:
        print("No data available.")
        return
    
    df = pd.DataFrame(data)
    latest_data = df.sort_values('time').groupby('symbol').tail(1)
    
    print("\n" + "="*50)
    print("CRYPTO PRICE SUMMARY")
    print("="*50)
    
    for _, row in latest_data.iterrows():
        symbol_data = df[df['symbol'] == row['symbol']]
        price_change = symbol_data['price'].iloc[-1] - symbol_data['price'].iloc[0] if len(symbol_data) > 1 else 0
        change_percent = (price_change / symbol_data['price'].iloc[0]) * 100 if len(symbol_data) > 1 else 0
        
        print(f"{row['symbol'].upper():<12} ${row['price']:>8.2f} "
              f"({change_percent:+.2f}%)")
    
    print(f"\nTotal data points: {len(data)}")
    print(f"Time range: {df['datetime'].min().strftime('%H:%M')} - {df['datetime'].max().strftime('%H:%M')}")

def main():
    parser = argparse.ArgumentParser(description='Generate cryptocurrency price charts')
    parser.add_argument('--input', '-i', default='crypto_data.json', 
                       help='Input JSON file with crypto data')
    parser.add_argument('--output', '-o', default='crypto_charts.png',
                       help='Output chart image file')
    parser.add_argument('--summary', '-s', action='store_true',
                       help='Show data summary')
    
    args = parser.parse_args()
    
    # Load data
    data = load_crypto_data(args.input)
    
    if args.summary:
        print_summary(data)
    
    # Generate charts
    generate_charts(data, args.output)

if __name__ == "__main__":
    main()