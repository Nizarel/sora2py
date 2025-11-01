export interface Video {
  id: number;
  project_id?: number;
  prompt: string;
  video_type: 'text_to_video' | 'image_to_video' | 'chained_video';
  duration?: number;
  resolution?: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';
  job_id?: string;
  error_message?: string;
  blob_url?: string;
  thumbnail_url?: string;
  file_size?: number;
  input_image_url?: string;
  created_at: string;
  completed_at?: string;
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  brand: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface VideoGenerateRequest {
  prompt: string;
  duration: number;
  resolution: string;
  project_id?: number;
  input_image_url?: string;
}

export interface ChainedVideoRequest {
  prompt: string;
  total_duration: number;
  segment_duration: number;
  crossfade_duration: number;
  resolution: string;
  project_id?: number;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  brand?: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
}
