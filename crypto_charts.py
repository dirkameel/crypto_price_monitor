#!/usr/bin/env python3
"""
Cryptocurrency Price Chart Generator
Displays charts from data collected by the Go monitor
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import numpy as np

class CryptoChartGenerator:
    def __init__(self):
        self.data_dir = "data"
        plt.style.use('seaborn-v0_8')
        
    def load_price_data(self, filename):
        """Load price data from JSON file"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Data file {filename} not found. Run the Go monitor first.")
            return None
    
    def create_price_comparison_chart(self):
        """Create a bar chart comparing current prices"""
        data = self.load_price_data("latest_prices.json")
        if not data:
            return
            
        symbols = [item['symbol'] for item in data]
        prices = [item['price'] for item in data]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(symbols, prices, color=['#FF9900', '#3C3C3D', '#0033AD', '#00FFBD', '#E6007A'])
        
        # Add value labels on bars
        for bar, price in zip(bars, prices):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'${price:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Current Cryptocurrency Prices', fontsize=16, fontweight='bold')
        plt.ylabel('Price (USD)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def create_price_history_chart(self):
        """Create a line chart showing price history"""
        # Find the latest data file
        data_files = [f for f in os.listdir(self.data_dir) if f.startswith('crypto_prices_')]
        if not data_files:
            print("No historical data found. Run the Go monitor for some time first.")
            return
            
        latest_file = sorted(data_files)[-1]
        data = self.load_price_data(latest_file)
        if not data:
            return
        
        # Organize data by cryptocurrency
        crypto_data = {}
        for entry in data:
            symbol = entry['symbol']
            if symbol not in crypto_data:
                crypto_data[symbol] = {'times': [], 'prices': []}
            
            # Parse timestamp
            try:
                time_obj = datetime.strptime(entry['time'], '%Y-%m-%d %H:%M:%S')
                crypto_data[symbol]['times'].append(time_obj)
                crypto_data[symbol]['prices'].append(entry['price'])
            except ValueError:
                continue
        
        plt.figure(figsize=(14, 8))
        
        colors = ['#FF9900', '#3C3C3D', '#0033AD', '#00FFBD', '#E6007A']
        color_idx = 0
        
        for symbol, data in crypto_data.items():
            if data['times'] and data['prices']:
                # Sort by time
                sorted_data = sorted(zip(data['times'], data['prices']))
                times, prices = zip(*sorted_data)
                
                plt.plot(times, prices, 
                        label=symbol.capitalize(), 
                        linewidth=2,
                        color=colors[color_idx % len(colors)],
                        marker='o',
                        markersize=3)
                color_idx += 1
        
        plt.title('Cryptocurrency Price History', fontsize=16, fontweight='bold')
        plt.ylabel('Price (USD)', fontsize=12)
        plt.xlabel('Time', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Format x-axis to show time properly
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.gcf().autofmt_xdate()
        
        plt.tight_layout()
        plt.show()
    
    def create_performance_chart(self):
        """Create a chart showing percentage change"""
        data_files = [f for f in os.listdir(self.data_dir) if f.startswith('crypto_prices_')]
        if not data_files or len(data_files) < 2:
            print("Need at least 2 data points to calculate performance.")
            return
        
        # Get oldest and newest files
        oldest_file = sorted(data_files)[0]
        newest_file = sorted(data_files)[-1]
        
        old_data = self.load_price_data(oldest_file)
        new_data = self.load_price_data(newest_file)
        
        if not old_data or not new_data:
            return
        
        # Calculate percentage changes
        changes = {}
        for new_entry in new_data:
            symbol = new_entry['symbol']
            new_price = new_entry['price']
            
            # Find corresponding old price
            old_price = None
            for old_entry in old_data:
                if old_entry['symbol'] == symbol:
                    old_price = old_entry['price']
                    break
            
            if old_price and old_price > 0:
                change = ((new_price - old_price) / old_price) * 100
                changes[symbol] = change
        
        if changes:
            symbols = list(changes.keys())
            percentages = list(changes.values())
            colors = ['green' if x >= 0 else 'red' for x in percentages]
            
            plt.figure(figsize=(12, 6))
            bars = plt.bar(symbols, percentages, color=colors, alpha=0.7)
            
            # Add value labels
            for bar, percentage in zip(bars, percentages):
                plt.text(bar.get_x() + bar.get_width()/2, 
                        bar.get_height() + (1 if percentage >= 0 else -3),
                        f'{percentage:+.1f}%', 
                        ha='center', 
                        va='bottom' if percentage >= 0 else 'top',
                        fontweight='bold')
            
            plt.title('Cryptocurrency Performance (%)', fontsize=16, fontweight='bold')
            plt.ylabel('Percentage Change (%)', fontsize=12)
            plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()

def main():
    chart_gen = CryptoChartGenerator()
    
    print("📈 Cryptocurrency Chart Generator")
    print("1. Current Price Comparison")
    print("2. Price History")
    print("3. Performance Chart")
    
    try:
        choice = input("Select chart type (1-3): ").strip()
        
        if choice == '1':
            chart_gen.create_price_comparison_chart()
        elif choice == '2':
            chart_gen.create_price_history_chart()
        elif choice == '3':
            chart_gen.create_performance_chart()
        else:
            print("Invalid choice. Please run again and select 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()