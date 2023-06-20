from minio import Minio
from minio.error import S3Error
import datetime

class MinIO:
    """
    This is the operator for the MiniO S3 Storage
    To build the object you have to pass the host,
    bucket name and port.
    The client and bucket are created on initialization.
    The methods allow CRUD operations on the bucket
    objects.
    """
    def __init__(self, minio_host:str, bucket_name:str, minio_port:int) -> None:
        self.minio_client = None
        self.bucket_name = bucket_name
        self.minio_host = minio_host
        self.minio_port = minio_port
        self.minio_tls = False
        self.minio_user = "minio"
        self.minio_password = "miniosecret"

        self.create_minio_client()
        self.create_bucket()

    def create_minio_client(self):
        self.minio_client = Minio(
            f"{self.minio_host}:{self.minio_port}",
            access_key = self.minio_user,
            secret_key = self.minio_password,
            secure = self.minio_tls
        )

    def create_bucket(self):
        found = self.minio_client.bucket_exists(self.bucket_name)
        if not found:
            self.minio_client.make_bucket(self.bucket_name)

    def upload_object(self, file_path:str, object_name:str):
        try:
            self.minio_client.fput_object(
                self.bucket_name, object_name, file_path
            )
            print(f"Object {object_name} successfully uploaded to bucket {self.bucket_name}")

            # Get the URL of the uploaded object
            object_url = self.minio_client.presigned_get_object(self.bucket_name, object_name)
            return object_url
        except S3Error as e:
            print("Error", e)

    def list_objects(self):
        try:
            res = self.minio_client.list_objects(
                self.bucket_name
            )
            data = []
            for item in res:
                item_dict = {
                    "filename": item.__dict__["_object_name"],
                    "uploaded": int(datetime.datetime.timestamp(item.__dict__["_last_modified"])),
                    "size": item.__dict__["_size"]
                }
                data.append(item_dict)

            return data
        
        except S3Error as e:
            print("Error", e)

    def delete_object(self, object_name:str):
        try:
            self.minio_client.remove_object(
                object_name=object_name,
                bucket_name=self.bucket_name
            )
        except S3Error as e:
            print("Error", e)

    def download_object(self, object_name:str, file_path:str):
        try:
            self.minio_client.fget_object(
                self.bucket_name, object_name, file_path
            )
            print(f"Object {object_name} successfully downloaded to {file_path}")
        except S3Error as e:
            print ("Error", e)