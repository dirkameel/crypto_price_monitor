package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

// CryptoData represents the structure for cryptocurrency data
type CryptoData struct {
	Symbol string  `json:"symbol"`
	Price  float64 `json:"price,string"`
	Time   int64   `json:"time"`
}

// APIResponse represents the response from the CoinCap API
type APIResponse struct {
	Data struct {
		Symbol string `json:"symbol"`
		Price  string `json:"priceUsd"`
		Time   int64  `json:"timestamp"`
	} `json:"data"`
}

// Config holds configuration for the monitor
type Config struct {
	Symbols    []string `json:"symbols"`
	Interval   int      `json:"interval"`
	OutputFile string   `json:"output_file"`
}

func main() {
	// Load configuration
	config, err := loadConfig("config.json")
	if err != nil {
		fmt.Printf("Error loading config: %v\n", err)
		return
	}

	fmt.Printf("Starting crypto monitor for symbols: %v\n", config.Symbols)
	fmt.Printf("Monitoring interval: %d seconds\n", config.Interval)
	fmt.Printf("Output file: %s\n", config.OutputFile)

	// Create or clear the output file
	err = initializeOutputFile(config.OutputFile)
	if err != nil {
		fmt.Printf("Error initializing output file: %v\n", err)
		return
	}

	// Start monitoring
	ticker := time.NewTicker(time.Duration(config.Interval) * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			for _, symbol := range config.Symbols {
				data, err := fetchCryptoPrice(symbol)
				if err != nil {
					fmt.Printf("Error fetching %s: %v\n", symbol, err)
					continue
				}
				err = saveDataToFile(data, config.OutputFile)
				if err != nil {
					fmt.Printf("Error saving data: %v\n", err)
				} else {
					fmt.Printf("Saved %s: $%.2f at %s\n", 
						data.Symbol, data.Price, time.Unix(data.Time/1000, 0).Format("15:04:05"))
				}
			}
			fmt.Println("---")
		}
	}
}

// loadConfig reads the configuration from JSON file
func loadConfig(filename string) (*Config, error) {
	file, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var config Config
	err = json.Unmarshal(file, &config)
	if err != nil {
		return nil, err
	}

	return &config, nil
}

// fetchCryptoPrice fetches current price for a cryptocurrency symbol
func fetchCryptoPrice(symbol string) (*CryptoData, error) {
	url := fmt.Sprintf("https://api.coincap.io/v2/assets/%s", symbol)
	
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var apiResp APIResponse
	err = json.Unmarshal(body, &apiResp)
	if err != nil {
		return nil, err
	}

	price, err := parseFloat(apiResp.Data.Price)
	if err != nil {
		return nil, err
	}

	return &CryptoData{
		Symbol: symbol,
		Price:  price,
		Time:   apiResp.Data.Time,
	}, nil
}

// parseFloat safely parses string to float64
func parseFloat(s string) (float64, error) {
	var f float64
	_, err := fmt.Sscanf(s, "%f", &f)
	return f, err
}

// initializeOutputFile creates or clears the output file
func initializeOutputFile(filename string) error {
	return ioutil.WriteFile(filename, []byte(""), 0644)
}

// saveDataToFile appends crypto data to the output file
func saveDataToFile(data *CryptoData, filename string) error {
	file, err := os.OpenFile(filename, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
	if err != nil {
		return err
	}
	defer file.Close()

	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}

	_, err = file.WriteString(string(jsonData) + "\n")
	return err
}