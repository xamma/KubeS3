package main

import (
	"os"
)

func LoadConfig() (*AppConfig, error) {
	defaultEnvVars := map[string]string{
		"API_PORT": "8080",
		"DATA_DIR": "./data",
	}

	apiPort := getEnv("API_PORT", defaultEnvVars)
	dataDir := getEnv("DATA_DIR", defaultEnvVars)

	config := &AppConfig{
		ApiPort: apiPort,
		DataDir: dataDir,
	}

	return config, nil
}

func getEnv(key string, defaultValues map[string]string) string {
	value, exists := os.LookupEnv(key)
	if !exists {
		value = defaultValues[key]
	}
	return value
}