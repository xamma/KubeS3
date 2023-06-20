package main

import (
	"fmt"
	"net/http"
	"os"
	"log"
	"path/filepath"
	"strings"

	"github.com/disintegration/imaging"
	"github.com/gin-gonic/gin"
)

func renderRoot(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"statusCode": http.StatusOK,
		"message":    "This is a microservice for creating Thumbnails.",
	})
}

// uploadFile            godoc
// @Summary      Post files
// @Description  Upload files to data dir.
// @Tags         files
// @Produce      json
// @Success      200 {string} binary
// @Accept       multipart/form-data
// @Param        file formData file true "File to upload"
// @Router       /upload [post]
func createThumbnail(c *gin.Context) {
	config, err := LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check the file extension
	ext := filepath.Ext(file.Filename)
	supportedExtensions := []string{".jpg", ".jpeg", ".png", ".bmp"}

	// Check if the file extension is supported
	isSupported := false
	for _, supportedExt := range supportedExtensions {
		if strings.EqualFold(ext, supportedExt) {
			isSupported = true
			break
		}
	}

	if !isSupported {
		// Return a placeholder image for unsupported file types
		placeholderPath := getPlaceholderImagePath(ext)
		c.File(placeholderPath)
		return
	}

	// Save the uploaded file to the data directory
	dst := filepath.Join(config.DataDir, file.Filename)
	if err := c.SaveUploadedFile(file, dst); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Open the uploaded file
	srcImage, err := imaging.Open(dst)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Generate the thumbnail
	dstImage80 := imaging.Resize(srcImage, 80, 80, imaging.Lanczos)

	// Save the thumbnail
	thumbnailFilename := "thumb_" + file.Filename
	thumbnailFilePath := filepath.Join(".", config.DataDir, thumbnailFilename)
	if err := imaging.Save(dstImage80, thumbnailFilePath); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Return the thumbnail as the response
	c.File(thumbnailFilePath)
}

// Get the path of the placeholder image based on the file extension
func getPlaceholderImagePath(ext string) string {
	switch strings.ToLower(ext) {
	case ".pdf":
		return "./assets/placeholder.png"
	case ".csv":
		return "./placeholder_image2.jpg"
	// Add cases for other unsupported file types if needed
	default:
		return "./placeholder_image.jpg" // Default placeholder image for unsupported file types
	}
}


// @title           Gin Web Service
// @version         1.0
// @description     Testing API in Go using Gin framework.
// @termsOfService  placeholder

// @contact.name   Max
// @contact.url    xamma.github.io
// @contact.email  xam93@live.de

// @license.name  Apache 2.0
// @license.url   http://www.apache.org/licenses/LICENSE-2.0.html

// @host      localhost:8080
// @BasePath  /api/v1
func main() {
	config, err := LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	newpath := filepath.Join(".", config.DataDir)
	if err := os.MkdirAll(newpath, os.ModePerm); err != nil {
		log.Fatal(err)
	}

	router := gin.Default()
	v1 := router.Group("/api/v1")

	v1.GET("/", renderRoot)
	v1.POST("/thumbnail", createThumbnail)

	port := fmt.Sprintf(":%s", config.ApiPort)
	router.Run(port)
}
