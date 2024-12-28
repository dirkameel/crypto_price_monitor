#!/usr/bin/env python3
"""
Cryptocurrency Chart Generator
Reads data from crypto_prices.json and generates basic charts
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import time
from collections import defaultdict

class CryptoChartGenerator:
    def __init__(self, data_file='crypto_prices.json'):
        self.data_file = data_file
        self.historical_data = defaultdict(list)
        
    def load_data(self):
        """Load current price data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def update_historical_data(self, current_data):
        """Update historical data with current prices"""
        for crypto in current_data:
            symbol = crypto['symbol']
            price = crypto['price']
            timestamp = datetime.strptime(crypto['time'], '%Y-%m-%d %H:%M:%S')
            
            self.historical_data[symbol].append({
                'timestamp': timestamp,
                'price': price
            })
            
            # Keep only last 50 data points for each crypto
            if len(self.historical_data[symbol]) > 50:
                self.historical_data[symbol] = self.historical_data[symbol][-50:]
    
    def create_current_prices_chart(self, data):
        """Create a bar chart of current prices"""
        if not data:
            print("No data available for chart")
            return
            
        symbols = [crypto['symbol'] for crypto in data]
        prices = [crypto['price'] for crypto in data]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(symbols, prices, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        
        # Add value labels on bars
        for bar, price in zip(bars, prices):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(prices)*0.01,
                    f'${price:.2f}', ha='center', va='bottom')
        
        plt.title('Current Cryptocurrency Prices', fontsize=16, fontweight='bold')
        plt.ylabel('Price (USD)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('current_prices.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("Current prices chart saved as 'current_prices.png'")
    
    def create_price_trend_chart(self):
        """Create line charts showing price trends over time"""
        if not self.historical_data:
            print("No historical data available for trend chart")
            return
            
        plt.figure(figsize=(14, 8))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for i, (symbol, data) in enumerate(self.historical_data.items()):
            if len(data) < 2:
                continue
                
            timestamps = [point['timestamp'] for point in data]
            prices = [point['price'] for point in data]
            
            color = colors[i % len(colors)]
            plt.plot(timestamps, prices, marker='o', linewidth=2, markersize=4,
                    label=symbol, color=color)
            
            # Add latest price annotation
            latest_price = prices[-1]
            plt.annotate(f'${latest_price:.2f}', 
                        xy=(timestamps[-1], latest_price),
                        xytext=(10, 0), textcoords='offset points',
                        fontweight='bold')
        
        plt.title('Cryptocurrency Price Trends', fontsize=16, fontweight='bold')
        plt.ylabel('Price (USD)', fontsize=12)
        plt.xlabel('Time', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Format x-axis to show time nicely
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.gcf().autofmt_xdate()
        
        plt.tight_layout()
        plt.savefig('price_trends.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("Price trends chart saved as 'price_trends.png'")
    
    def generate_performance_summary(self, data):
        """Generate a text summary of performance"""
        if not data:
            return
            
        print("\n" + "="*50)
        print("CRYPTO PERFORMANCE SUMMARY")
        print("="*50)
        
        for crypto in data:
            symbol = crypto['symbol']
            current_price = crypto['price']
            
            if symbol in self.historical_data and len(self.historical_data[symbol]) > 1:
                first_price = self.historical_data[symbol][0]['price']
                change = ((current_price - first_price) / first_price) * 100
                change_symbol = "+" if change >= 0 else ""
                print(f"{symbol:12}: ${current_price:8.2f} ({change_symbol}{change:+.2f}%)")
            else:
                print(f"{symbol:12}: ${current_price:8.2f} (New)")
        
        print("="*50)

def main():
    chart_gen = CryptoChartGenerator()
    
    print("Cryptocurrency Chart Generator Started...")
    print("Monitoring price data and generating charts")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Load current data
            current_data = chart_gen.load_data()
            
            if current_data:
                # Update historical data
                chart_gen.update_historical_data(current_data)
                
                # Generate charts
                chart_gen.create_current_prices_chart(current_data)
                chart_gen.create_price_trend_chart()
                chart_gen.generate_performance_summary(current_data)
            
            # Wait before next update
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nChart generator stopped.")

if __name__ == "__main__":
    main()