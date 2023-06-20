package main

type AppConfig struct {
	CustomMessage string
	ApiPort string
	DataDir string
}

// StatusCode of type int: This field represents the HTTP status code of the response.
// Files of type []string: This field is a slice of strings that holds the list of file names.
// The struct tags json:"statusCode" and json:"files" are used to specify the corresponding JSON property names 
// when the struct is serialized to JSON. 
// They ensure that the field names are properly mapped to their JSON counterparts.
type FileListResponse struct {
    StatusCode int      `json:"statusCode"`
    Files      []string `json:"files"`
}