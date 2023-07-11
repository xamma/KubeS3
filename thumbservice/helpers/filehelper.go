package helpers

import (
	"strings"
	"os"
)

// Get the path of the placeholder image based on the file extension
func GetPlaceholderImagePath(ext string) string {
	switch strings.ToLower(ext) {
	case ".pdf":
		return "./assets/pdf_placeholder.png"
	case ".csv":
		return "./assets/csv_placeholder.png"
	case ".json":
		return "./assets/json_placeholder.png"
	// Add cases for other unsupported file types if needed
	default:
		return "./assets/notsupported_placeholder.png" // Default placeholder image for unsupported file types
	}
}

func DeleteDirContents(dir string) error {

	err := os.RemoveAll(dir)
	if err != nil {
		return err
	}
	return nil
}