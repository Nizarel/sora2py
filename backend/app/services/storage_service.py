"""
Azure Blob Storage service for storing videos
"""
import os
from typing import BinaryIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings
from ..core.config import settings


class StorageService:
    """Service for managing video storage in Azure Blob Storage"""
    
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )
        self.container_name = settings.AZURE_STORAGE_CONTAINER_NAME
        self._ensure_container_exists()
    
    def _ensure_container_exists(self):
        """Ensure the container exists, create if it doesn't"""
        try:
            self.blob_service_client.get_container_client(self.container_name)
        except:
            self.blob_service_client.create_container(
                self.container_name,
                public_access=None  # Private container
            )
    
    async def upload_video(
        self,
        file_path: str,
        blob_name: str
    ) -> str:
        """
        Upload a video file to Azure Blob Storage
        
        Args:
            file_path: Local path to the video file
            blob_name: Name to give the blob in storage
            
        Returns:
            URL of the uploaded blob
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            # Set content type for video
            content_settings = ContentSettings(content_type='video/mp4')
            
            with open(file_path, "rb") as data:
                blob_client.upload_blob(
                    data,
                    overwrite=True,
                    content_settings=content_settings
                )
            
            return blob_client.url
            
        except Exception as e:
            raise Exception(f"Failed to upload video to storage: {str(e)}")
    
    async def upload_image(
        self,
        file_data: BinaryIO,
        blob_name: str
    ) -> str:
        """
        Upload an image file to Azure Blob Storage
        
        Args:
            file_data: Binary file data
            blob_name: Name to give the blob in storage
            
        Returns:
            URL of the uploaded blob
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            # Set content type for image
            content_settings = ContentSettings(content_type='image/jpeg')
            
            blob_client.upload_blob(
                file_data,
                overwrite=True,
                content_settings=content_settings
            )
            
            return blob_client.url
            
        except Exception as e:
            raise Exception(f"Failed to upload image to storage: {str(e)}")
    
    async def delete_blob(self, blob_name: str) -> bool:
        """
        Delete a blob from storage
        
        Args:
            blob_name: Name of the blob to delete
            
        Returns:
            True if successful
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.delete_blob()
            return True
            
        except Exception as e:
            raise Exception(f"Failed to delete blob: {str(e)}")
    
    async def get_blob_url(self, blob_name: str) -> str:
        """
        Get the URL for a blob
        
        Args:
            blob_name: Name of the blob
            
        Returns:
            URL of the blob
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name
        )
        return blob_client.url
