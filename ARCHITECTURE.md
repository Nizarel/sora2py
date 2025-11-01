# System Architecture: Coca-Cola Sora-2 Video Studio

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           End Users                                      │
│                      (Coca-Cola Marketing Team)                          │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Azure Container Apps (Frontend)                       │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  React SPA (TypeScript)                                           │  │
│  │  - Dashboard                                                      │  │
│  │  - Project Management                                             │  │
│  │  - Video Generation UI                                            │  │
│  │  Served by: Nginx                                                 │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ REST API (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Azure Container Apps (Backend)                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application (Python 3.11)                                │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │  API Layer                                                    │ │  │
│  │  │  - /api/v1/projects (CRUD)                                    │ │  │
│  │  │  - /api/v1/videos (Generate, List, Get, Delete)              │ │  │
│  │  │  - /health (Health Check)                                     │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │  Business Logic Layer                                         │ │  │
│  │  │  - VideoGenerationService → Azure OpenAI Sora-2              │ │  │
│  │  │  - StorageService → Azure Blob Storage                       │ │  │
│  │  │  - Authentication/Authorization (JWT)                        │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │  Data Access Layer                                            │ │  │
│  │  │  - SQLAlchemy ORM                                             │ │  │
│  │  │  - Models: User, Project, Video                              │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└──────┬──────────────┬──────────────┬──────────────┬─────────────────────┘
       │              │              │              │
       │              │              │              │
       ▼              ▼              ▼              ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────────┐
│  PostgreSQL │ │  Redis   │ │  Azure   │ │  Azure OpenAI   │
│  Flexible   │ │  Cache   │ │   Blob   │ │    (Sora-2)     │
│   Server    │ │          │ │ Storage  │ │                 │
│             │ │          │ │          │ │                 │
│ - Users     │ │ - Celery │ │ - Videos │ │ - Video Gen     │
│ - Projects  │ │ - Tasks  │ │ - Images │ │ - Status Poll   │
│ - Videos    │ │ - Queue  │ │          │ │ - Download      │
└─────────────┘ └──────────┘ └──────────┘ └─────────────────┘
```

## Component Details

### 1. Frontend (React SPA)

**Technology:**
- React 18 with TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- React Router (routing)
- TanStack Query (data fetching)

**Components:**
```
frontend/
├── Pages
│   ├── Dashboard - Statistics and recent videos
│   ├── Projects - Project management (CRUD)
│   └── VideoGenerate - Video creation form
├── Components
│   └── Layout - Navigation and header
├── Services
│   ├── api.ts - Axios configuration
│   ├── videoService.ts - Video API calls
│   └── projectService.ts - Project API calls
└── Types
    └── index.ts - TypeScript definitions
```

**Deployment:**
- Built as static files
- Served by Nginx
- Containerized with Docker
- Deployed to Azure Container Apps

### 2. Backend (FastAPI)

**Technology:**
- Python 3.11
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Pydantic (validation)
- Uvicorn (ASGI server)

**Architecture Layers:**

```
┌──────────────────────────────────────┐
│         API Layer                    │
│  - Request validation (Pydantic)     │
│  - Response serialization            │
│  - Error handling                    │
│  - Authentication middleware         │
└──────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│      Business Logic Layer            │
│  - VideoGenerationService            │
│  - StorageService                    │
│  - AuthService                       │
│  - Background tasks                  │
└──────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│       Data Access Layer              │
│  - SQLAlchemy models                 │
│  - Database operations               │
│  - Transaction management            │
└──────────────────────────────────────┘
```

### 3. Database (PostgreSQL)

**Schema:**

```sql
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │       │    projects     │       │     videos      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id              │◄──┐   │ id              │◄──┐   │ id              │
│ email           │   │   │ name            │   │   │ project_id (FK) │──┐
│ username        │   └───│ owner_id (FK)   │   │   │ prompt          │  │
│ hashed_password │       │ description     │   └───│ video_type      │  │
│ full_name       │       │ brand           │       │ duration        │  │
│ is_active       │       │ created_at      │       │ resolution      │  │
│ created_at      │       │ updated_at      │       │ status          │  │
└─────────────────┘       └─────────────────┘       │ job_id          │  │
                                                     │ blob_url        │  │
                                                     │ file_size       │  │
                                                     │ created_at      │  │
                                                     │ completed_at    │  │
                                                     └─────────────────┘  │
                                                             │            │
                                                             └────────────┘
```

### 4. External Services

#### Azure OpenAI (Sora-2)
```
┌────────────────────────────────────────┐
│       Azure OpenAI Service             │
│                                        │
│  POST /deployments/sora-2/videos       │
│  → Initiate video generation           │
│                                        │
│  GET /videos/{job_id}                  │
│  → Check generation status             │
│                                        │
│  GET /videos/{job_id}/content          │
│  → Download completed video            │
└────────────────────────────────────────┘
```

#### Azure Blob Storage
```
┌────────────────────────────────────────┐
│       Azure Blob Storage               │
│                                        │
│  Container: videos/                    │
│  ├── videos/{id}/video.mp4             │
│  ├── videos/{id}/thumbnail.jpg         │
│  └── images/{id}/input.jpg             │
│                                        │
│  Features:                             │
│  - Secure access with SAS tokens       │
│  - CDN integration ready               │
│  - Lifecycle management                │
└────────────────────────────────────────┘
```

## Data Flow

### Video Generation Flow

```
User Request → Frontend → Backend API → Database (Create Record)
                                      ↓
                             Azure OpenAI Sora-2
                                      ↓
                             Background Task (Poll Status)
                                      ↓
                             Download Video
                                      ↓
                             Upload to Blob Storage
                                      ↓
                             Update Database Record
                                      ↓
                             Notify User (via polling)
```

**Detailed Steps:**

1. **Initiation**
   - User fills video generation form
   - Frontend validates input
   - POST request to `/api/v1/videos/generate`

2. **Backend Processing**
   - Create video record in database (status: pending)
   - Call Azure OpenAI Sora-2 API
   - Receive job_id
   - Return job_id to frontend
   - Start background task

3. **Background Task**
   - Update status to "processing"
   - Poll Azure OpenAI every 10 seconds
   - Check if status is "completed"

4. **Completion**
   - Download video from Azure OpenAI
   - Upload to Azure Blob Storage
   - Update database (status: completed, blob_url, file_size)
   - Clean up temporary files

5. **User Notification**
   - Frontend polls `/api/v1/videos/{id}` every 10 seconds
   - Displays updated status
   - Shows download link when completed

## Security Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├────────────────────────────────────────────────────────────┤
│ 1. Network Security                                         │
│    - HTTPS only (Container Apps)                            │
│    - CORS configuration                                     │
│    - Azure Private Link (optional)                          │
├────────────────────────────────────────────────────────────┤
│ 2. Authentication                                           │
│    - JWT tokens                                             │
│    - Password hashing (bcrypt)                              │
│    - Azure AD integration ready                             │
├────────────────────────────────────────────────────────────┤
│ 3. Authorization                                            │
│    - Role-based access control                              │
│    - Resource ownership validation                          │
├────────────────────────────────────────────────────────────┤
│ 4. Data Security                                            │
│    - Encrypted database connections                         │
│    - Secrets in environment variables                       │
│    - Azure Key Vault integration ready                      │
├────────────────────────────────────────────────────────────┤
│ 5. Input Validation                                         │
│    - Pydantic schema validation                             │
│    - SQL injection protection (ORM)                         │
│    - XSS protection (React)                                 │
└────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

### Local Development (Docker Compose)

```
┌─────────────────────────────────────────────────────────┐
│                Docker Compose Network                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Frontend │  │ Backend  │  │PostgreSQL│  │ Redis  │ │
│  │  :3000   │  │  :8000   │  │  :5432   │  │ :6379  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Azure Production Deployment

```
┌──────────────────────────────────────────────────────────────┐
│                   Azure Subscription                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │            Resource Group                              │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  Container Apps Environment                       │ │  │
│  │  │  ┌────────────────┐  ┌────────────────┐          │ │  │
│  │  │  │ Frontend App   │  │ Backend App    │          │ │  │
│  │  │  │ (React/Nginx)  │  │ (FastAPI)      │          │ │  │
│  │  │  │ Auto-scale:1-3 │  │ Auto-scale:1-5 │          │ │  │
│  │  │  └────────────────┘  └────────────────┘          │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │                                                        │  │
│  │  ┌────────────────┐  ┌────────────────┐              │  │
│  │  │  PostgreSQL    │  │  Blob Storage  │              │  │
│  │  │  Flexible      │  │  (videos)      │              │  │
│  │  │  Server        │  │                │              │  │
│  │  └────────────────┘  └────────────────┘              │  │
│  │                                                        │  │
│  │  ┌────────────────┐  ┌────────────────┐              │  │
│  │  │  Container     │  │  Application   │              │  │
│  │  │  Registry      │  │  Insights      │              │  │
│  │  └────────────────┘  └────────────────┘              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  External Services:                                           │
│  ┌────────────────┐                                          │
│  │  Azure OpenAI  │                                          │
│  │  (Sora-2)      │                                          │
│  └────────────────┘                                          │
└──────────────────────────────────────────────────────────────┘
```

## Scaling Strategy

### Horizontal Scaling

```
Load Balancer
      │
      ├─────┬─────┬─────┬─────┐
      ▼     ▼     ▼     ▼     ▼
    App1  App2  App3  App4  App5
      │     │     │     │     │
      └─────┴─────┴─────┴─────┘
              │
              ▼
        Shared Database
```

**Configuration:**
- Frontend: 1-3 replicas (CPU-based)
- Backend: 1-5 replicas (HTTP concurrency)
- Database: Vertical scaling (CPU/Memory)
- Redis: Single instance (no persistence)

### Vertical Scaling

- **Backend**: Increase CPU/Memory per container
- **Database**: Upgrade to higher tier (B1ms → B2s → GP)
- **Storage**: Automatic (pay-per-use)

## Monitoring & Observability

```
┌──────────────────────────────────────────┐
│     Azure Application Insights           │
├──────────────────────────────────────────┤
│  Metrics:                                │
│  - Request rate                          │
│  - Response time                         │
│  - Error rate                            │
│  - Dependency calls                      │
│                                          │
│  Logs:                                   │
│  - Application logs                      │
│  - Container logs                        │
│  - Query logs                            │
│                                          │
│  Alerts:                                 │
│  - High error rate                       │
│  - Slow response time                    │
│  - Resource exhaustion                   │
└──────────────────────────────────────────┘
```

## CI/CD Pipeline

```
GitHub Repository
      │
      │ git push to main
      ▼
┌──────────────────────┐
│  GitHub Actions      │
├──────────────────────┤
│ 1. Checkout code     │
│ 2. Build backend     │
│ 3. Build frontend    │
│ 4. Run tests         │
│ 5. Build images      │
│ 6. Push to ACR       │
│ 7. Deploy to Apps    │
└──────────────────────┘
      │
      ▼
Azure Container Registry
      │
      ▼
Azure Container Apps
```

## Cost Optimization

### Resource Tiers

```
Development:
- Container Apps: Basic (1 vCPU, 2GB RAM)
- PostgreSQL: Burstable B1ms
- Storage: LRS
Cost: ~$50/month

Production:
- Container Apps: Standard (2 vCPU, 4GB RAM) with auto-scale
- PostgreSQL: General Purpose GP_Gen5_2
- Storage: GRS with lifecycle management
Cost: ~$200-300/month

Enterprise:
- Container Apps: Premium with VNET
- PostgreSQL: Business Critical
- Storage: Premium with CDN
Cost: ~$500-1000/month
```

## Disaster Recovery

```
Primary Region (East US)
      │
      │ Geo-replication
      ▼
Secondary Region (West US)
      │
      │ Automated failover
      ▼
Database Backup (7 days retention)
```

---

This architecture provides:
- ✅ Scalability (horizontal and vertical)
- ✅ High availability (99.9% SLA)
- ✅ Security (multiple layers)
- ✅ Cost optimization
- ✅ Easy maintenance
- ✅ Disaster recovery
