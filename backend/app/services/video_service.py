"""
Video generation service - refactored from original video_generator.py
"""
import os
import time
from typing import Optional
from openai import OpenAI
from ..core.config import settings


class VideoGenerationService:
    """Service for generating videos using Azure OpenAI Sora-2"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            base_url=f"{settings.AZURE_OPENAI_ENDPOINT}openai/v1/",
            default_headers={"api-key": settings.AZURE_OPENAI_API_KEY}
        )
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT
    
    async def generate_video(
        self,
        prompt: str,
        duration: int = 12,
        resolution: str = "1280x720",
        input_image_path: Optional[str] = None
    ) -> dict:
        """
        Generate a video using Sora-2
        
        Args:
            prompt: Text description of the video
            duration: Video duration in seconds (4, 8, or 12)
            resolution: Video resolution (WIDTHxHEIGHT)
            input_image_path: Optional path to input image for image-to-video
            
        Returns:
            dict with job_id and initial status
        """
        try:
            if input_image_path:
                # Image-to-video mode
                with open(input_image_path, "rb") as image_file:
                    video = self.client.videos.create(
                        model=self.deployment,
                        prompt=prompt,
                        size=resolution,
                        seconds=str(duration),
                        input_reference=image_file
                    )
            else:
                # Text-to-video mode
                video = self.client.videos.create(
                    model=self.deployment,
                    prompt=prompt,
                    size=resolution,
                    seconds=str(duration)
                )
            
            return {
                "job_id": video.id,
                "status": video.status
            }
            
        except Exception as e:
            raise Exception(f"Failed to initiate video generation: {str(e)}")
    
    async def check_video_status(self, job_id: str) -> dict:
        """
        Check the status of a video generation job
        
        Args:
            job_id: The job ID returned from generate_video
            
        Returns:
            dict with status and other details
        """
        try:
            video = self.client.videos.retrieve(job_id)
            
            result = {
                "job_id": job_id,
                "status": video.status
            }
            
            if hasattr(video, 'error'):
                result["error"] = video.error
                
            return result
            
        except Exception as e:
            raise Exception(f"Failed to check video status: {str(e)}")
    
    async def download_video(self, job_id: str, output_path: str) -> dict:
        """
        Download a completed video
        
        Args:
            job_id: The job ID of the completed video
            output_path: Path where to save the video
            
        Returns:
            dict with file_path and file_size
        """
        try:
            # Download the video content
            content = self.client.videos.download_content(job_id, variant="video")
            content.write_to_file(output_path)
            
            # Get file size
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            
            return {
                "file_path": output_path,
                "file_size_mb": round(file_size, 2)
            }
            
        except Exception as e:
            raise Exception(f"Failed to download video: {str(e)}")
