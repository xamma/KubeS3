from pydantic import BaseModel
from typing import List

class AppConfig(BaseModel):
    """
    This is the configuration Class for the App.
    It uses pydantics BaseModel to declare the Types
    and what happens, when the entry is not defined.
    """
    api_port : int | None = None
    allowed_mime_types : List | None = None
    minio_port : str | None = None
    minio_host : str | None = None
    bucket_name : str | None = None
    thumb_bucket_name : str | None = None
    thumbnail_service_host : str | None = None