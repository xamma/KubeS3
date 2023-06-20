package main

import (
	"os"
)

func LoadConfig() (*AppConfig, error) {
	defaultEnvVars := map[string]string{
		"CUSTOM_MESSAGE": "Here could be your message",
		"API_PORT": "8080",
		"DATA_DIR": "./data",
	}

	customMessage := getEnv("CUSTOM_MESSAGE", defaultEnvVars)
	apiPort := getEnv("API_PORT", defaultEnvVars)
	dataDir := getEnv("DATA_DIR", defaultEnvVars)

	config := &AppConfig{
		CustomMessage: customMessage,
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