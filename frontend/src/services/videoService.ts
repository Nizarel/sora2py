import { api } from './api';
import { Video, VideoGenerateRequest, ChainedVideoRequest } from '../types';

export const videoService = {
  async generateVideo(request: VideoGenerateRequest): Promise<Video> {
    const response = await api.post<Video>('/videos/generate', request);
    return response.data;
  },

  async getVideo(id: number): Promise<Video> {
    const response = await api.get<Video>(`/videos/${id}`);
    return response.data;
  },

  async listVideos(params?: {
    project_id?: number;
    status?: string;
    page?: number;
    page_size?: number;
  }) {
    const response = await api.get('/videos', { params });
    return response.data;
  },

  async deleteVideo(id: number): Promise<void> {
    await api.delete(`/videos/${id}`);
  },
};
