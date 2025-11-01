# Coca-Cola Sora-2 Video Studio - Quick Start Guide

This guide will help you get the Video Studio application running in minutes.

## Prerequisites

- **Docker Desktop** installed and running
- **Azure OpenAI** access with Sora-2 deployment
- **Azure Storage Account** (or create one)
- Git installed

## Option 1: Quick Start with Docker Compose (Recommended)

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/Nizarel/sora2py.git
cd sora2py

# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
# Required: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_STORAGE_CONNECTION_STRING
nano .env  # or use your favorite editor
```

### 2. Start the Application

```bash
# Start all services (database, redis, backend, frontend)
docker-compose up

# Or run in background
docker-compose up -d
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

### 4. Create Your First Video

1. Open http://localhost:3000 in your browser
2. Navigate to "Generate Video"
3. Enter a prompt like: "A refreshing Coca-Cola bottle with ice on a sunny beach"
4. Select duration (12 seconds recommended)
5. Click "Generate Video"
6. Watch the status on the Dashboard

### 5. Stop the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean reset)
docker-compose down -v
```

## Option 2: Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp ../.env.example .env
# Edit .env with your credentials

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access backend at: http://localhost:8000

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=/api/v1" > .env

# Run development server
npm run dev
```

Access frontend at: http://localhost:3000

## Option 3: Deploy to Azure

See [Deployment Guide](docs/deployment.md) for detailed Azure deployment instructions.

**Quick Deploy:**

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-coca-cola-video-studio --location eastus

# Deploy infrastructure
cd infrastructure
az deployment group create \
  --resource-group rg-coca-cola-video-studio \
  --template-file main.bicep \
  --parameters @parameters.json
```

## Environment Variables Explained

### Essential Variables

```env
# Azure OpenAI (Required)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=sora-2

# Azure Storage (Required for production)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER_NAME=videos

# Database (Auto-configured in Docker Compose)
DATABASE_URL=postgresql://admin:changeme@db:5432/videostudio

# Security (Change in production!)
SECRET_KEY=your-secret-key-here
```

### Optional Variables

```env
# Development mode
DEBUG=True

# Video settings
MAX_VIDEO_DURATION=120
DEFAULT_VIDEO_RESOLUTION=1280x720

# Redis (for background tasks)
REDIS_URL=redis://redis:6379/0
```

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reset Database

```bash
# Stop and remove volumes
docker-compose down -v

# Start fresh
docker-compose up
```

### Build Images

```bash
# Build all
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

### Backend won't start

**Issue**: "Missing required environment variables"
```bash
# Solution: Check .env file exists and has all required variables
cat .env
```

**Issue**: "Cannot connect to database"
```bash
# Solution: Ensure database is running
docker-compose up db
```

### Frontend can't reach backend

**Issue**: "Network error" in browser console
```bash
# Solution: Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/app/core/config.py
```

### Video generation fails

**Issue**: "Failed to generate video"
```bash
# Solution: Check Azure OpenAI credentials
# Verify Sora-2 deployment exists
# Check Azure OpenAI logs in Azure Portal
```

### Docker issues

**Issue**: "Port already in use"
```bash
# Solution: Change ports in docker-compose.yml
# Or stop conflicting services
```

**Issue**: "Out of disk space"
```bash
# Solution: Clean up Docker
docker system prune -a
```

## Next Steps

1. **Customize branding**: Edit frontend colors in `frontend/tailwind.config.js`
2. **Add authentication**: Implement Azure AD in backend
3. **Create projects**: Organize your videos into campaigns
4. **Batch generate**: Create multiple videos with different prompts
5. **Deploy to Azure**: Follow deployment guide for production

## Support & Documentation

- **Full README**: [PROJECT_README.md](PROJECT_README.md)
- **API Documentation**: [docs/api-documentation.md](docs/api-documentation.md)
- **Deployment Guide**: [docs/deployment.md](docs/deployment.md)
- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose                           │
├──────────────────────┬──────────────────────────────────────┤
│   Frontend (React)   │      Backend (FastAPI)               │
│   Port: 3000         │      Port: 8000                      │
├──────────────────────┴──────────────────────────────────────┤
│   PostgreSQL (5432)  │  Redis (6379)                        │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │  Azure Blob  │    │ Azure OpenAI │
│   Database   │    │   Storage    │    │   (Sora-2)   │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Quick Commands Cheat Sheet

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Reset and clean
docker-compose down -v

# Rebuild images
docker-compose build

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec db psql -U admin -d videostudio

# Check status
docker-compose ps

# Restart a service
docker-compose restart backend
```

## Success Checklist

- [ ] Docker Desktop is running
- [ ] Azure OpenAI credentials configured
- [ ] Azure Storage connection string set
- [ ] `.env` file created and populated
- [ ] `docker-compose up` runs without errors
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend API docs at http://localhost:8000/api/docs
- [ ] Database connected successfully
- [ ] First video generated successfully

---

**Need Help?** Check the documentation or create an issue in the repository.
