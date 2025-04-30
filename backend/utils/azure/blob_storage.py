# utils/blob_storage.py
from azure.storage.blob import BlobServiceClient
import os

class AzureBlobStorage:
    def __init__(self, connection_string: str, container_name: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        
    def upload_file(self, file_path: str, blob_name: str):
        with open(file_path, "rb") as data:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data, overwrite=True)
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_client.container_name}/{blob_name}"