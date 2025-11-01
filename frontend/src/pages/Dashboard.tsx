import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { videoService } from '../services/videoService';
import { projectService } from '../services/projectService';
import { Video as VideoIcon, FolderOpen, Clock, CheckCircle } from 'lucide-react';

const Dashboard: React.FC = () => {
  const { data: videos } = useQuery({
    queryKey: ['videos'],
    queryFn: () => videoService.listVideos({ page_size: 10 }),
  });

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectService.listProjects(0, 10),
  });

  const stats = [
    {
      label: 'Total Videos',
      value: videos?.total || 0,
      icon: VideoIcon,
      color: 'bg-blue-500',
    },
    {
      label: 'Projects',
      value: projects?.length || 0,
      icon: FolderOpen,
      color: 'bg-green-500',
    },
    {
      label: 'Processing',
      value: videos?.videos?.filter((v) => v.status === 'processing').length || 0,
      icon: Clock,
      color: 'bg-yellow-500',
    },
    {
      label: 'Completed',
      value: videos?.videos?.filter((v) => v.status === 'completed').length || 0,
      icon: CheckCircle,
      color: 'bg-coca-cola-red',
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h2>
        <p className="text-gray-600">Welcome to the Coca-Cola Video Studio</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {stat.value}
                  </p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="text-white" size={24} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Videos */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Recent Videos</h3>
        {videos && videos.videos && videos.videos.length > 0 ? (
          <div className="space-y-3">
            {videos.videos.slice(0, 5).map((video) => (
              <div
                key={video.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{video.prompt}</p>
                  <p className="text-sm text-gray-600">
                    {new Date(video.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    video.status === 'completed'
                      ? 'bg-green-100 text-green-800'
                      : video.status === 'processing'
                      ? 'bg-yellow-100 text-yellow-800'
                      : video.status === 'failed'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {video.status}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600">No videos yet. Create your first video!</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
