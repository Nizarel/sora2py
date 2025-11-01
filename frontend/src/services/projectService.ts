import { api } from './api';
import { Project, ProjectCreate } from '../types';

export const projectService = {
  async createProject(project: ProjectCreate): Promise<Project> {
    const response = await api.post<Project>('/projects', project);
    return response.data;
  },

  async getProject(id: number): Promise<Project> {
    const response = await api.get<Project>(`/projects/${id}`);
    return response.data;
  },

  async listProjects(skip = 0, limit = 100): Promise<Project[]> {
    const response = await api.get<Project[]>('/projects', {
      params: { skip, limit },
    });
    return response.data;
  },

  async updateProject(id: number, updates: Partial<ProjectCreate>): Promise<Project> {
    const response = await api.put<Project>(`/projects/${id}`, updates);
    return response.data;
  },

  async deleteProject(id: number): Promise<void> {
    await api.delete(`/projects/${id}`);
  },
};
