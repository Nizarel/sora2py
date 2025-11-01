import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { videoService } from '../services/videoService';
import { projectService } from '../services/projectService';
import { VideoGenerateRequest } from '../types';
import { Sparkles, Clock } from 'lucide-react';

const VideoGenerate: React.FC = () => {
  const [formData, setFormData] = useState<VideoGenerateRequest>({
    prompt: '',
    duration: 12,
    resolution: '1280x720',
    project_id: undefined,
  });

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectService.listProjects(),
  });

  const generateMutation = useMutation({
    mutationFn: videoService.generateVideo,
    onSuccess: (data) => {
      alert(`Video generation started! Job ID: ${data.job_id}`);
      setFormData({
        prompt: '',
        duration: 12,
        resolution: '1280x720',
        project_id: undefined,
      });
    },
    onError: (error: any) => {
      alert(`Failed to generate video: ${error.response?.data?.detail || error.message}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    generateMutation.mutate(formData);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Generate Video</h2>
        <p className="text-gray-600">Create stunning videos with AI-powered Sora-2</p>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Prompt */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Video Prompt *
            </label>
            <textarea
              value={formData.prompt}
              onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
              placeholder="Describe the video you want to create... e.g., 'A refreshing Coca-Cola bottle with ice on a sunny beach'"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coca-cola-red"
              rows={4}
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              Be specific and descriptive for best results
            </p>
          </div>

          {/* Project Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Project (Optional)
            </label>
            <select
              value={formData.project_id || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  project_id: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coca-cola-red"
            >
              <option value="">No project</option>
              {projects?.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>

          {/* Duration */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Duration
            </label>
            <div className="flex space-x-4">
              {[4, 8, 12].map((duration) => (
                <button
                  key={duration}
                  type="button"
                  onClick={() => setFormData({ ...formData, duration })}
                  className={`flex-1 py-3 px-4 rounded-lg border-2 font-medium transition-colors ${
                    formData.duration === duration
                      ? 'border-coca-cola-red bg-coca-cola-red text-white'
                      : 'border-gray-300 text-gray-700 hover:border-gray-400'
                  }`}
                >
                  {duration}s
                </button>
              ))}
            </div>
          </div>

          {/* Resolution */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Resolution
            </label>
            <select
              value={formData.resolution}
              onChange={(e) => setFormData({ ...formData, resolution: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coca-cola-red"
            >
              <option value="1280x720">HD (1280x720)</option>
              <option value="1920x1080">Full HD (1920x1080)</option>
            </select>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start space-x-3">
            <Clock className="text-blue-600 flex-shrink-0 mt-0.5" size={20} />
            <div className="text-sm text-blue-900">
              <p className="font-medium mb-1">Generation Time</p>
              <p>
                Video generation typically takes 1-3 minutes per 12-second segment.
                You'll be able to view and download your video once it's completed.
              </p>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={generateMutation.isPending}
            className="w-full btn-primary flex items-center justify-center space-x-2 py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Sparkles size={24} />
            <span>
              {generateMutation.isPending ? 'Generating...' : 'Generate Video'}
            </span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default VideoGenerate;
