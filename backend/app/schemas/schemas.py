"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class VideoStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoType(str, Enum):
    TEXT_TO_VIDEO = "text_to_video"
    IMAGE_TO_VIDEO = "image_to_video"
    CHAINED_VIDEO = "chained_video"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    brand: str = "Coca-Cola"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Video Schemas
class VideoGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    duration: int = Field(12, ge=4, le=12, description="Duration in seconds (4, 8, or 12)")
    resolution: str = Field("1280x720", description="Video resolution (WIDTHxHEIGHT)")
    project_id: Optional[int] = None
    input_image_url: Optional[str] = None  # For image-to-video


class ChainedVideoRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    total_duration: int = Field(..., ge=12, le=120, description="Total duration in seconds")
    segment_duration: int = Field(12, ge=4, le=12, description="Duration per segment")
    crossfade_duration: float = Field(1.0, ge=0.5, le=2.0, description="Crossfade duration")
    resolution: str = Field("1280x720", description="Video resolution")
    project_id: Optional[int] = None


class VideoResponse(BaseModel):
    id: int
    project_id: Optional[int]
    prompt: str
    video_type: VideoType
    duration: Optional[int]
    resolution: Optional[str]
    status: VideoStatus
    job_id: Optional[str]
    error_message: Optional[str]
    blob_url: Optional[str]
    thumbnail_url: Optional[str]
    file_size: Optional[float]
    input_image_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class VideoListResponse(BaseModel):
    videos: list[VideoResponse]
    total: int
    page: int
    page_size: int


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
