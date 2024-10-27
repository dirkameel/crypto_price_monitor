package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

// CryptoPrice represents the price data for a cryptocurrency
type CryptoPrice struct {
	Symbol string  `json:"symbol"`
	Price  float64 `json:"price,string"`
	Time   string  `json:"time"`
}

// CoinGeckoResponse represents the response from CoinGecko API
type CoinGeckoResponse map[string]map[string]float64

func main() {
	// Cryptocurrencies to monitor
	cryptos := []string{"bitcoin", "ethereum", "cardano", "solana", "polkadot"}
	
	fmt.Println("🚀 Cryptocurrency Price Monitor Started...")
	fmt.Println("Monitoring:", cryptos)
	fmt.Println("Press Ctrl+C to stop")
	
	// Create data directory if it doesn't exist
	os.MkdirAll("data", 0755)
	
	for {
		prices, err := fetchCryptoPrices(cryptos)
		if err != nil {
			fmt.Printf("Error fetching prices: %v\n", err)
		} else {
			savePricesToFile(prices)
			displayCurrentPrices(prices)
		}
		
		// Wait for 1 minute before next update
		time.Sleep(1 * time.Minute)
	}
}

// fetchCryptoPrices fetches current prices from CoinGecko API
func fetchCryptoPrices(cryptos []string) ([]CryptoPrice, error) {
	// Build URL with multiple cryptocurrencies
	url := "https://api.coingecko.com/api/v3/simple/price?ids="
	for i, crypto := range cryptos {
		if i > 0 {
			url += ","
		}
		url += crypto
	}
	url += "&vs_currencies=usd"
	
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	
	var data CoinGeckoResponse
	err = json.Unmarshal(body, &data)
	if err != nil {
		return nil, err
	}
	
	var prices []CryptoPrice
	currentTime := time.Now().Format("2006-01-02 15:04:05")
	
	for _, crypto := range cryptos {
		if cryptoData, exists := data[crypto]; exists {
			if price, exists := cryptoData["usd"]; exists {
				prices = append(prices, CryptoPrice{
					Symbol: crypto,
					Price:  price,
					Time:   currentTime,
				})
			}
		}
	}
	
	return prices, nil
}

// savePricesToFile saves price data to JSON file for charting
func savePricesToFile(prices []CryptoPrice) {
	filename := fmt.Sprintf("data/crypto_prices_%s.json", 
		time.Now().Format("20060102"))
	
	// Read existing data
	var allData []CryptoPrice
	if existingData, err := ioutil.ReadFile(filename); err == nil {
		json.Unmarshal(existingData, &allData)
	}
	
	// Append new data
	allData = append(allData, prices...)
	
	// Keep only last 100 records to prevent file from growing too large
	if len(allData) > 100 {
		allData = allData[len(allData)-100:]
	}
	
	// Write to file
	dataJSON, _ := json.MarshalIndent(allData, "", "  ")
	ioutil.WriteFile(filename, dataJSON, 0644)
	
	// Also create a latest snapshot for the chart script
	latestData, _ := json.MarshalIndent(prices, "", "  ")
	ioutil.WriteFile("data/latest_prices.json", latestData, 0644)
}

// displayCurrentPrices displays current prices in console
func displayCurrentPrices(prices []CryptoPrice) {
	fmt.Printf("\n📊 Price Update - %s\n", time.Now().Format("15:04:05"))
	fmt.Println("┌─────────────────┬──────────────┐")
	fmt.Println("│ Cryptocurrency  │    Price     │")
	fmt.Println("├─────────────────┼──────────────┤")
	
	for _, price := range prices {
		fmt.Printf("│ %-15s │ $%9.2f  │\n", price.Symbol, price.Price)
	}
	
	fmt.Println("└─────────────────┴──────────────┘")
}