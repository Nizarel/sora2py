"""
API endpoints for video operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
import tempfile
import os

from ..db.database import get_db
from ..schemas.schemas import (
    VideoGenerateRequest,
    ChainedVideoRequest,
    VideoResponse,
    VideoListResponse,
    VideoStatus as VideoStatusEnum
)
from ..models.models import Video, VideoType, VideoStatus
from ..services.video_service import VideoGenerationService
from ..services.storage_service import StorageService

router = APIRouter(prefix="/videos", tags=["videos"])

video_service = VideoGenerationService()
storage_service = StorageService()


async def process_video_generation(
    video_id: int,
    db: Session
):
    """Background task to process video generation"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    try:
        # Update status to processing
        video.status = VideoStatus.PROCESSING
        db.commit()
        
        # Poll for completion
        while True:
            status_result = await video_service.check_video_status(video.job_id)
            
            if status_result["status"] == "completed":
                # Download video to temp file
                temp_path = f"/tmp/{uuid.uuid4()}.mp4"
                download_result = await video_service.download_video(
                    video.job_id,
                    temp_path
                )
                
                # Upload to blob storage
                blob_name = f"videos/{video.id}/{uuid.uuid4()}.mp4"
                blob_url = await storage_service.upload_video(temp_path, blob_name)
                
                # Update video record
                video.status = VideoStatus.COMPLETED
                video.blob_url = blob_url
                video.file_size = download_result["file_size_mb"]
                video.completed_at = datetime.utcnow()
                
                # Clean up temp file
                os.remove(temp_path)
                
                db.commit()
                break
                
            elif status_result["status"] in ["failed", "cancelled"]:
                video.status = VideoStatus.FAILED
                video.error_message = status_result.get("error", "Unknown error")
                db.commit()
                break
            
            # Wait before next check
            import asyncio
            await asyncio.sleep(10)
            
    except Exception as e:
        video.status = VideoStatus.FAILED
        video.error_message = str(e)
        db.commit()


@router.post("/generate", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def generate_video(
    request: VideoGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate a new video using Sora-2
    
    - **prompt**: Text description of the video to generate
    - **duration**: Video duration in seconds (4, 8, or 12)
    - **resolution**: Video resolution (default: 1280x720)
    - **project_id**: Optional project to associate the video with
    - **input_image_url**: Optional image URL for image-to-video generation
    """
    try:
        # Determine video type
        video_type = VideoType.IMAGE_TO_VIDEO if request.input_image_url else VideoType.TEXT_TO_VIDEO
        
        # Initiate video generation
        input_image_path = None
        if request.input_image_url:
            # Download image from URL to temp file
            # TODO: Implement image download from blob storage
            pass
        
        result = await video_service.generate_video(
            prompt=request.prompt,
            duration=request.duration,
            resolution=request.resolution,
            input_image_path=input_image_path
        )
        
        # Create video record
        video = Video(
            project_id=request.project_id,
            prompt=request.prompt,
            video_type=video_type,
            duration=request.duration,
            resolution=request.resolution,
            status=VideoStatus.PENDING,
            job_id=result["job_id"],
            input_image_url=request.input_image_url
        )
        
        db.add(video)
        db.commit()
        db.refresh(video)
        
        # Start background processing
        background_tasks.add_task(process_video_generation, video.id, db)
        
        return video
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate video: {str(e)}"
        )


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Get details of a specific video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    return video


@router.get("/", response_model=VideoListResponse)
async def list_videos(
    project_id: Optional[int] = None,
    status: Optional[VideoStatusEnum] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """List videos with optional filtering"""
    query = db.query(Video)
    
    if project_id:
        query = query.filter(Video.project_id == project_id)
    
    if status:
        query = query.filter(Video.status == VideoStatus[status.value.upper()])
    
    # Get total count
    total = query.count()
    
    # Paginate
    offset = (page - 1) * page_size
    videos = query.offset(offset).limit(page_size).all()
    
    return VideoListResponse(
        videos=videos,
        total=total,
        page=page,
        page_size=page_size
    )


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Delete a video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    # Delete from blob storage if exists
    if video.blob_url:
        # Extract blob name from URL and delete
        # TODO: Implement blob deletion
        pass
    
    db.delete(video)
    db.commit()
    
    return None
