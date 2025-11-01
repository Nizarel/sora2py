# Coca-Cola Sora-2 Video Studio - Backend API

Python FastAPI backend for the Coca-Cola Video Studio application.

## Architecture

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configurations and utilities
│   ├── db/            # Database connection and session management
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic schemas for validation
│   └── services/      # Business logic services
├── requirements.txt   # Python dependencies
└── Dockerfile        # Container configuration
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
# Application
DEBUG=True
SECRET_KEY=your-secret-key-here

# Azure OpenAI (Sora-2)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=sora-2

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_STORAGE_CONTAINER_NAME=videos

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/videostudio

# Redis
REDIS_URL=redis://localhost:6379/0
```

### 3. Run Database Migrations

```bash
# Install Alembic (if not already installed)
pip install alembic

# Initialize database
alembic upgrade head
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## API Endpoints

### Projects

- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Videos

- `POST /api/v1/videos/generate` - Generate a new video
- `GET /api/v1/videos` - List videos (with filtering)
- `GET /api/v1/videos/{id}` - Get video details
- `DELETE /api/v1/videos/{id}` - Delete video

## Services

### VideoGenerationService

Handles video generation using Azure OpenAI Sora-2 API:
- Text-to-video generation
- Image-to-video generation
- Status polling
- Video download

### StorageService

Manages video storage in Azure Blob Storage:
- Upload videos and images
- Generate access URLs
- Delete files

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Docker

### Build

```bash
docker build -t coca-cola-video-studio-backend .
```

### Run

```bash
docker run -p 8000:8000 --env-file .env coca-cola-video-studio-backend
```

## Deployment

See `../docs/deployment.md` for Azure Container Apps deployment instructions.
