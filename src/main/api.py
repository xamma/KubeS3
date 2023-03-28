import socket
import tempfile
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
    data_list = S3Object.list_objects()
    hostname = socket.gethostname()
    res = {
        'hostname': hostname,
        'objects': data_list
    }
    
    return res

# Post an data-object
@app.post('/api/upload', tags=["object_handler"])
async def api_upload_object(file: UploadFile):
    if file.content_type not in config_settings.allowed_mime_types:
        raise HTTPException(400, detail="Invalid document type")
    
    try:
        S3Object = app.S3Object

        # Use tempfile.NamedTemporaryFile() to create a temporary file in memory
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Write file contents to the temporary file
            contents = await file.read()
            temp_file.write(contents)

            # Remove whitespaces from the filename
            file.filename = file.filename.replace(" ", "")

            S3Object.upload_object(file_path=temp_file.name, object_name=file.filename)

        res = {
            "uploaded": file.filename,
            "status_code": 200
        }
    except:
        raise HTTPException(400, detail=f"Error uploading {file.filename}")

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