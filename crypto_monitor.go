package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
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
	
	fmt.Println("Cryptocurrency Price Monitor")
	fmt.Println("============================")
	
	for {
		prices, err := fetchCryptoPrices(cryptos)
		if err != nil {
			log.Printf("Error fetching prices: %v", err)
			time.Sleep(30 * time.Second)
			continue
		}
		
		// Display current prices
		displayPrices(prices)
		
		// Save to JSON file for Python charting
		saveToJSON(prices)
		
		// Wait before next update
		time.Sleep(60 * time.Second)
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
			price := CryptoPrice{
				Symbol: crypto,
				Price:  cryptoData["usd"],
				Time:   currentTime,
			}
			prices = append(prices, price)
		}
	}
	
	return prices, nil
}

// displayPrices prints current prices to console
func displayPrices(prices []CryptoPrice) {
	fmt.Printf("\n%s - Current Prices:\n", time.Now().Format("15:04:05"))
	fmt.Println("-------------------")
	for _, price := range prices {
		fmt.Printf("%-12s: $%.2f\n", price.Symbol, price.Price)
	}
	fmt.Println("-------------------")
}

// saveToJSON saves price data to a JSON file for Python processing
func saveToJSON(prices []CryptoPrice) {
	// Read existing data
	var allData []CryptoPrice
	existingData, err := ioutil.ReadFile("crypto_prices.json")
	if err == nil {
		json.Unmarshal(existingData, &allData)
	}
	
	// Append new data (keep last 100 records)
	allData = append(allData, prices...)
	if len(allData) > 100 {
		allData = allData[len(allData)-100:]
	}
	
	// Write to file
	data, err := json.MarshalIndent(allData, "", "  ")
	if err != nil {
		log.Printf("Error marshaling JSON: %v", err)
		return
	}
	
	err = ioutil.WriteFile("crypto_prices.json", data, 0644)
	if err != nil {
		log.Printf("Error writing to file: %v", err)
	}
}