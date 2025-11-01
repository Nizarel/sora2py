# API Documentation

## Overview

The Coca-Cola Video Studio API provides RESTful endpoints for video generation, project management, and user authentication.

**Base URL**: `/api/v1`

## Authentication

All API requests require JWT authentication (except health check endpoints).

Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Rate Limits

- Standard users: 100 requests/minute
- Premium users: 1000 requests/minute

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message here"
}
```

### Common Error Codes

- `400` - Bad Request: Invalid input
- `401` - Unauthorized: Missing or invalid token
- `403` - Forbidden: Insufficient permissions
- `404` - Not Found: Resource doesn't exist
- `422` - Validation Error: Invalid request body
- `500` - Internal Server Error

## Projects API

### Create Project

**POST** `/api/v1/projects`

Create a new video project.

**Request Body:**
```json
{
  "name": "Summer Campaign 2024",
  "description": "Coca-Cola summer promotional videos",
  "brand": "Coca-Cola"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Summer Campaign 2024",
  "description": "Coca-Cola summer promotional videos",
  "brand": "Coca-Cola",
  "owner_id": 1,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### List Projects

**GET** `/api/v1/projects`

Retrieve all projects.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Summer Campaign 2024",
    "description": "Coca-Cola summer promotional videos",
    "brand": "Coca-Cola",
    "owner_id": 1,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
]
```

### Get Project

**GET** `/api/v1/projects/{project_id}`

Retrieve a specific project.

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Summer Campaign 2024",
  "description": "Coca-Cola summer promotional videos",
  "brand": "Coca-Cola",
  "owner_id": 1,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Update Project

**PUT** `/api/v1/projects/{project_id}`

Update project details.

**Request Body:**
```json
{
  "name": "Updated Campaign Name",
  "description": "Updated description"
}
```

**Response:** `200 OK`

### Delete Project

**DELETE** `/api/v1/projects/{project_id}`

Delete a project and all associated videos.

**Response:** `204 No Content`

## Videos API

### Generate Video

**POST** `/api/v1/videos/generate`

Start a new video generation job.

**Request Body:**
```json
{
  "prompt": "A refreshing Coca-Cola bottle with ice on a sunny beach",
  "duration": 12,
  "resolution": "1280x720",
  "project_id": 1,
  "input_image_url": null
}
```

**Parameters:**
- `prompt` (string, required): Description of the video
- `duration` (int): 4, 8, or 12 seconds (default: 12)
- `resolution` (string): "1280x720" or "1920x1080" (default: "1280x720")
- `project_id` (int, optional): Project to associate with
- `input_image_url` (string, optional): URL for image-to-video

**Response:** `201 Created`
```json
{
  "id": 1,
  "project_id": 1,
  "prompt": "A refreshing Coca-Cola bottle with ice on a sunny beach",
  "video_type": "text_to_video",
  "duration": 12,
  "resolution": "1280x720",
  "status": "pending",
  "job_id": "abc123",
  "error_message": null,
  "blob_url": null,
  "thumbnail_url": null,
  "file_size": null,
  "input_image_url": null,
  "created_at": "2024-01-15T10:00:00Z",
  "completed_at": null
}
```

### Get Video

**GET** `/api/v1/videos/{video_id}`

Retrieve video details and status.

**Response:** `200 OK`
```json
{
  "id": 1,
  "project_id": 1,
  "prompt": "A refreshing Coca-Cola bottle with ice on a sunny beach",
  "video_type": "text_to_video",
  "duration": 12,
  "resolution": "1280x720",
  "status": "completed",
  "job_id": "abc123",
  "error_message": null,
  "blob_url": "https://storage.blob.core.windows.net/videos/video1.mp4",
  "thumbnail_url": "https://storage.blob.core.windows.net/videos/thumb1.jpg",
  "file_size": 5.2,
  "input_image_url": null,
  "created_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:03:00Z"
}
```

### List Videos

**GET** `/api/v1/videos`

List all videos with optional filtering.

**Query Parameters:**
- `project_id` (int): Filter by project
- `status` (string): Filter by status (pending, processing, completed, failed)
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20)

**Response:** `200 OK`
```json
{
  "videos": [
    {
      "id": 1,
      "project_id": 1,
      "prompt": "A refreshing Coca-Cola bottle...",
      "video_type": "text_to_video",
      "duration": 12,
      "resolution": "1280x720",
      "status": "completed",
      "job_id": "abc123",
      "blob_url": "https://storage.blob.core.windows.net/videos/video1.mp4",
      "created_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T10:03:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

### Delete Video

**DELETE** `/api/v1/videos/{video_id}`

Delete a video and its associated files.

**Response:** `204 No Content`

## Video Status Values

- `pending`: Job created, waiting to start
- `processing`: Video generation in progress
- `completed`: Video ready and available
- `failed`: Generation failed (check error_message)
- `cancelled`: Job was cancelled

## Video Types

- `text_to_video`: Generated from text prompt
- `image_to_video`: Animated from still image
- `chained_video`: Multiple segments combined

## Best Practices

1. **Poll for Status**: After creating a video, poll GET `/videos/{id}` every 10 seconds to check status
2. **Error Handling**: Always check `status` and `error_message` fields
3. **Prompt Quality**: Be specific and descriptive in prompts for best results
4. **Resource Limits**: Maximum 12 seconds per video generation
5. **Resolution**: Higher resolutions take longer to generate

## Code Examples

### Python

```python
import requests

# Generate video
response = requests.post(
    'https://api.example.com/api/v1/videos/generate',
    headers={'Authorization': 'Bearer YOUR_TOKEN'},
    json={
        'prompt': 'A Coca-Cola bottle on ice',
        'duration': 12,
        'resolution': '1920x1080'
    }
)
video = response.json()

# Poll for completion
import time
while video['status'] not in ['completed', 'failed']:
    time.sleep(10)
    response = requests.get(
        f'https://api.example.com/api/v1/videos/{video["id"]}',
        headers={'Authorization': 'Bearer YOUR_TOKEN'}
    )
    video = response.json()

# Download video
if video['status'] == 'completed':
    video_url = video['blob_url']
    print(f'Video ready: {video_url}')
```

### JavaScript/TypeScript

```typescript
// Generate video
const response = await fetch('/api/v1/videos/generate', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'A Coca-Cola bottle on ice',
    duration: 12,
    resolution: '1920x1080',
  }),
});
let video = await response.json();

// Poll for completion
while (!['completed', 'failed'].includes(video.status)) {
  await new Promise(resolve => setTimeout(resolve, 10000));
  const statusRes = await fetch(`/api/v1/videos/${video.id}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  video = await statusRes.json();
}

// Use video
if (video.status === 'completed') {
  console.log('Video ready:', video.blob_url);
}
```

## Support

For API issues or questions:
- Check the [Swagger docs](/api/docs) for interactive testing
- Review error messages in responses
- Contact support team
