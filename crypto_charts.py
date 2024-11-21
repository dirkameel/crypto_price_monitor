#!/usr/bin/env python3
"""
Cryptocurrency Price Chart Display
Simple script to display basic charts from crypto price data
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
from collections import defaultdict
import argparse

def load_price_data(filename="crypto_prices.json"):
    """Load cryptocurrency price data from JSON file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File {filename} not found. Run the Go monitor first.")
        return None

def organize_data_by_crypto(price_data):
    """Organize price data by cryptocurrency symbol"""
    crypto_data = defaultdict(list)
    
    for entry in price_data:
        symbol = entry['symbol']
        price = entry['price']
        time_str = entry['time']
        
        # Convert time string to datetime object
        try:
            timestamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            crypto_data[symbol].append((timestamp, price))
        except ValueError:
            continue
    
    return crypto_data

def plot_individual_charts(crypto_data):
    """Create individual price charts for each cryptocurrency"""
    for symbol, data in crypto_data.items():
        if not data:
            continue
            
        times, prices = zip(*data)
        
        plt.figure(figsize=(12, 6))
        plt.plot(times, prices, marker='o', linewidth=2, markersize=4)
        plt.title(f'{symbol.upper()} Price Chart')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Format x-axis to show time nicely
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        
        plt.tight_layout()
        plt.show()

def plot_combined_chart(crypto_data):
    """Create a combined chart showing all cryptocurrencies"""
    plt.figure(figsize=(14, 8))
    
    for symbol, data in crypto_data.items():
        if not data:
            continue
            
        times, prices = zip(*data)
        plt.plot(times, prices, marker='o', linewidth=2, markersize=3, label=symbol.upper())
    
    plt.title('Cryptocurrency Price Comparison')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    
    plt.tight_layout()
    plt.show()

def display_price_table(crypto_data):
    """Display a simple price table"""
    print("\nLatest Prices:")
    print("-" * 40)
    print(f"{'Cryptocurrency':<15} {'Latest Price':<12} {'Change'}")
    print("-" * 40)
    
    for symbol, data in crypto_data.items():
        if len(data) >= 2:
            latest_price = data[-1][1]
            previous_price = data[-2][1]
            change = ((latest_price - previous_price) / previous_price) * 100
            change_str = f"{change:+.2f}%"
            print(f"{symbol.upper():<15} ${latest_price:<11.2f} {change_str}")
        elif data:
            latest_price = data[-1][1]
            print(f"{symbol.upper():<15} ${latest_price:<11.2f} N/A")

def main():
    parser = argparse.ArgumentParser(description='Cryptocurrency Price Charts')
    parser.add_argument('--combined', action='store_true', help='Show combined chart')
    parser.add_argument('--individual', action='store_true', help='Show individual charts')
    parser.add_argument('--table', action='store_true', help='Show price table')
    
    args = parser.parse_args()
    
    # Load data
    price_data = load_price_data()
    if not price_data:
        return
    
    # Organize data
    crypto_data = organize_data_by_crypto(price_data)
    
    # Display based on arguments
    if args.table or not (args.combined or args.individual):
        display_price_table(crypto_data)
    
    if args.combined:
        plot_combined_chart(crypto_data)
    
    if args.individual:
        plot_individual_charts(crypto_data)
    
    # Default: show combined chart if no specific chart type requested
    if not args.combined and not args.individual and not args.table:
        plot_combined_chart(crypto_data)

if __name__ == "__main__":
    main()