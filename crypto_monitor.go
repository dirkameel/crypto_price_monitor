package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

// CryptoData represents the structure for cryptocurrency price data
type CryptoData struct {
	Symbol string  `json:"symbol"`
	Price  float64 `json:"price,string"`
	Time   string  `json:"time"`
}

// CoinGeckoResponse represents the API response structure
type CoinGeckoResponse map[string]map[string]float64

func main() {
	// Cryptocurrencies to monitor
	cryptos := []string{"bitcoin", "ethereum", "cardano", "solana", "polkadot"}
	
	fmt.Println("Cryptocurrency Price Monitor Started...")
	fmt.Println("Monitoring:", cryptos)
	fmt.Println("Press Ctrl+C to stop")
	
	for {
		// Fetch prices for all cryptocurrencies
		prices, err := fetchCryptoPrices(cryptos)
		if err != nil {
			log.Printf("Error fetching prices: %v", err)
			time.Sleep(30 * time.Second)
			continue
		}
		
		// Save data to JSON file for Python to read
		err = saveToJSON(prices)
		if err != nil {
			log.Printf("Error saving data: %v", err)
		}
		
		// Display current prices
		displayPrices(prices)
		
		// Wait before next update
		time.Sleep(60 * time.Second)
	}
}

// fetchCryptoPrices fetches current prices from CoinGecko API
func fetchCryptoPrices(cryptos []string) ([]CryptoData, error) {
	// Build API URL with multiple cryptocurrencies
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
		return nil, fmt.Errorf("failed to fetch data: %v", err)
	}
	defer resp.Body.Close()
	
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %v", err)
	}
	
	var data CoinGeckoResponse
	err = json.Unmarshal(body, &data)
	if err != nil {
		return nil, fmt.Errorf("failed to parse JSON: %v", err)
	}
	
	var prices []CryptoData
	currentTime := time.Now().Format("2006-01-02 15:04:05")
	
	for _, crypto := range cryptos {
		if cryptoData, exists := data[crypto]; exists {
			if usdPrice, exists := cryptoData["usd"]; exists {
				prices = append(prices, CryptoData{
					Symbol: crypto,
					Price:  usdPrice,
					Time:   currentTime,
				})
			}
		}
	}
	
	return prices, nil
}

// saveToJSON saves the price data to a JSON file
func saveToJSON(prices []CryptoData) error {
	file, err := os.Create("crypto_prices.json")
	if err != nil {
		return fmt.Errorf("failed to create file: %v", err)
	}
	defer file.Close()
	
	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	err = encoder.Encode(prices)
	if err != nil {
		return fmt.Errorf("failed to encode JSON: %v", err)
	}
	
	return nil
}

// displayPrices prints current prices to console
func displayPrices(prices []CryptoData) {
	fmt.Printf("\n=== Current Prices (%s) ===\n", time.Now().Format("15:04:05"))
	for _, crypto := range prices {
		fmt.Printf("%-12s: $%.2f\n", crypto.Symbol, crypto.Price)
	}
	fmt.Println("=============================")
}