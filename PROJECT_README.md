# Coca-Cola Sora-2 Video Studio

A full-stack web application for generating marketing videos using Azure OpenAI's Sora-2 model. Built specifically for Coca-Cola's marketing team to create high-quality video content.

## Features

- 🎬 **AI-Powered Video Generation**: Create videos from text prompts using Sora-2
- 🖼️ **Image-to-Video**: Animate still images into dynamic videos
- 📁 **Project Management**: Organize videos into branded projects
- ⚡ **Real-time Status**: Track video generation progress
- 🎨 **Coca-Cola Branding**: Custom UI with brand colors and styling
- ☁️ **Azure Integration**: Fully integrated with Azure services
- 🐳 **Containerized**: Deploy anywhere with Docker
- 🔒 **Secure**: JWT authentication and Azure AD support

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Azure Container Apps                     │
├──────────────────────┬──────────────────────────────────────┤
│   Frontend (React)   │      Backend (FastAPI)               │
│   - TypeScript       │      - Python 3.11                   │
│   - TailwindCSS      │      - SQLAlchemy                    │
│   - Vite             │      - Celery                        │
└──────────────────────┴──────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │  Azure Blob  │    │ Azure OpenAI │
│   Database   │    │   Storage    │    │   (Sora-2)   │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Azure OpenAI access with Sora-2 deployment
- Azure Storage Account
- PostgreSQL database (or use Docker Compose)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Nizarel/sora2py.git
cd sora2py
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

3. **Start with Docker Compose**
```bash
docker-compose up
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

## Project Structure

```
sora2py/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & utilities
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── infrastructure/         # Azure Bicep templates
│   └── main.bicep
├── docs/                  # Documentation
│   └── deployment.md
├── .github/
│   └── workflows/         # CI/CD pipelines
│       └── deploy.yml
└── docker-compose.yml     # Local development
```

## Technology Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL
- **Storage**: Azure Blob Storage
- **AI**: Azure OpenAI (Sora-2)

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: TanStack Query
- **HTTP Client**: Axios
- **Routing**: React Router

### Infrastructure
- **Hosting**: Azure Container Apps
- **CI/CD**: GitHub Actions
- **IaC**: Azure Bicep
- **Monitoring**: Azure Application Insights

## API Endpoints

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Videos
- `POST /api/v1/videos/generate` - Generate video
- `GET /api/v1/videos` - List videos
- `GET /api/v1/videos/{id}` - Get video details
- `DELETE /api/v1/videos/{id}` - Delete video

## Deployment

### Azure Container Apps

See [Deployment Guide](docs/deployment.md) for detailed instructions.

**Quick deploy:**
```bash
cd infrastructure
az deployment group create \
  --resource-group rg-coca-cola-video-studio \
  --template-file main.bicep \
  --parameters @parameters.json
```

### CI/CD

GitHub Actions automatically deploys on push to `main`:
1. Builds Docker images
2. Pushes to Azure Container Registry
3. Deploys to Azure Container Apps

## Configuration

### Environment Variables

**Backend** (`.env`):
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=sora-2
AZURE_STORAGE_CONNECTION_STRING=your-storage-connection-string
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-jwt-secret
```

**Frontend** (`.env`):
```env
VITE_API_URL=/api/v1
```

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Features in Detail

### Video Generation
- Text-to-video with customizable prompts
- Duration: 4, 8, or 12 seconds per segment
- Resolution: Up to 1920x1080 (Full HD)
- Automatic audio generation
- Background processing with status tracking

### Project Management
- Organize videos by campaign/project
- Brand-specific settings (Coca-Cola default)
- Project descriptions and metadata
- Easy video filtering by project

### Storage & Delivery
- Videos stored in Azure Blob Storage
- Automatic thumbnail generation
- Secure access URLs
- Efficient CDN delivery

## Monitoring

- **Application Insights**: Performance and error tracking
- **Container Logs**: Real-time debugging
- **Metrics Dashboard**: Usage statistics
- **Health Checks**: Automated health monitoring

## Security

- JWT-based authentication
- Azure AD integration ready
- HTTPS encryption (Container Apps)
- Secure secrets management
- CORS configuration
- Input validation

## Cost Optimization

- Auto-scaling based on demand
- Serverless containers (pay-per-use)
- Efficient storage lifecycle policies
- Query result caching
- Optimized container images

## Contributing

This is a private Coca-Cola project. For internal contributions:
1. Create a feature branch
2. Make changes with tests
3. Submit PR for review
4. CI/CD will deploy after merge

## License

Proprietary - Coca-Cola Company

## Support

For issues or questions:
- Create an issue in this repository
- Contact the development team
- Check the [Deployment Guide](docs/deployment.md)

## Roadmap

- [ ] Video editing capabilities
- [ ] Batch video generation
- [ ] Template library
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Mobile app

---

**Built with ❤️ for Coca-Cola Marketing Team**
