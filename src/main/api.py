import socket
import tempfile
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

import mimetypes
import pathlib

from storage import MinIO

"""
API for performing CRUD operations. 
Lets you upload data with defined mime-types
to an S3 bucket.
Also shows the hostname of the container/pod 
it is running on.
Lifespan event creates connection to bucket.
The data to upload is written in temp memory.
"""

#-Configurations---------------------------
from config import config_settings

#-Setup------------------------------------
# Setup lifespan for the API, binding to app makes it accessible to all routes.
@asynccontextmanager
async def lifespan(app: FastAPI):
    S3Object = MinIO(minio_host=config_settings.minio_host, 
                         bucket_name=config_settings.bucket_name, 
                         minio_port=config_settings.minio_port)
    app.S3Object = S3Object
    thumbs_minio_client = MinIO(minio_host=config_settings.minio_host, 
                                bucket_name=config_settings.thumb_bucket_name, 
                                minio_port=config_settings.minio_port)
    app.thumbs_minio_client = thumbs_minio_client
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#-API Area--------------------------------
# Root
@app.get('/', tags=["root"])
async def root():
    return {"message": "Hello from the API"}

# Get hostname and content
@app.get('/api/get', tags=["object_handler"])
async def api_get():
    S3Object = app.S3Object
    thumbs_minio_client = app.thumbs_minio_client
    data_list = S3Object.list_objects()
    hostname = socket.gethostname()
    res = {
        'hostname': hostname,
        'objects': []
    }

    for item in data_list:
        thumbnail_bucket, thumbnail_data = thumbs_minio_client.get_thumbnail_data(item['filename'])
        item['thumbnail_bucket'] = thumbnail_bucket
        item['thumbnail'] = thumbnail_data
        res['objects'].append(item)

    return res


# Download an data-object
@app.get('/api/download/{object_name}', tags=["object_handler"])
async def api_download_object(object_name:str):
    file_path = os.path.join(tempfile.gettempdir(), object_name)
    try:
        S3Object = app.S3Object
        S3Object.download_object(object_name, file_path)
        # return Response(content=open(file_path, 'rb').read(), media_type="application`/octet-stream")
        return FileResponse(file_path, media_type="application/octet-stream", filename=object_name)
    except:
        raise HTTPException(400, detail=f"Error downloading {object_name}")

# Post an data-object
@app.post('/api/upload', tags=["object_handler"])
async def api_upload_object(file: UploadFile):
    if file.content_type not in config_settings.allowed_mime_types:
        raise HTTPException(400, detail="Invalid document type")

    try:
        S3Object = app.S3Object
        thumbs_minio_client = app.thumbs_minio_client

        # Use tempfile.NamedTemporaryFile() to create a temporary file in memory
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Write file contents to the temporary file
            contents = await file.read()
            temp_file.write(contents)
            temp_file.flush()
            os.fsync(temp_file.fileno())

            # Remove whitespaces from the filename
            file.filename = file.filename.replace(" ", "")

            # Upload the file to the normal MinIO bucket
            object_name = file.filename  # Use the original filename as the object name
            object_url = S3Object.upload_object(temp_file.name, object_name)

            payload = {'file': (file.filename, contents, file.content_type)}

            # Make a POST request to the Go microservice
            response = requests.post(config_settings.thumbnail_service_host, files=payload)
            # print(response.content)

            thumbnail_object_url = None  # Initialize with a default value

            if response.status_code == 200:
                # Save the thumbnail image to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as thumbnail_file:
                    thumbnail_file.write(response.content)
                    thumbnail_file.flush()
                    os.fsync(thumbnail_file.fileno())
                    print(thumbnail_file.name)

                    # Determine the file extension based on the original file's MIME type
                    original_file_extension = mimetypes.guess_extension(file.content_type)

                    # Remove the original file's extension
                    original_filename_without_extension = pathlib.Path(file.filename).stem

                    # Check if the file is an image
                    if file.content_type.startswith('image/'):
                        # Use the original file's extension as the thumbnail file extension
                        thumbnail_file_extension = original_file_extension
                    else:
                        # Set the thumbnail file extension to PNG
                        thumbnail_file_extension = '.png'

                    # Append the thumbnail file extension to the original filename without extension
                    thumbnail_filename = f"thumb_{original_filename_without_extension}{thumbnail_file_extension}"

                    print("Original filename:", file.filename)
                    print("Original file extension:", original_file_extension)
                    print("Original filename without extension:", original_filename_without_extension)
                    print("Thumbnail filename:", thumbnail_filename)

                    # Upload the thumbnail image to the thumbs MinIO bucket with the appropriate filename
                    thumbnail_object_name = thumbnail_filename
                    thumbnail_object_url = thumbs_minio_client.upload_object(thumbnail_file.name, thumbnail_object_name)

                    print("Thumbnail object URL:", thumbnail_object_url)

            # Return the uploaded filename, status code, and the URL of the uploaded objects
            res = {
                "uploaded": file.filename,
                "status_code": 200,
                "object_url": object_url,
                "thumbnail_object_url": thumbnail_object_url
            }

    except Exception as e:
        raise HTTPException(400, detail=f"Error uploading {file.filename}: {str(e)}")

    return res
 

# Delete data by name
@app.delete('/api/delete/{object_name}', tags=["object_handler"])
async def api_delete_object(object_name:str):
    try:
        S3Object = app.S3Object
        for obj in S3Object.list_objects():
            if obj.get("filename") == object_name:
                S3Object.delete_object(object_name=object_name)
                res = {
                    "message": f"Successfully deleted object {object_name}",
                    "status_code": 200
                }
                return res

        raise HTTPException(404, detail=f"Object {object_name} not found.")
    except:
        raise HTTPException(400, detail=f"Error deleting object {object_name}")

if __name__ == "__main__":
    if "dev".lower() in sys.argv:
        print("Running in Dev-Mode")
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=config_settings.api_port, reload=True)
    else:
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=config_settings.api_port)