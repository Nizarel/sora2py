# Deployment Guide: Coca-Cola Sora-2 Video Studio

This guide covers deploying the Video Studio application to Azure Container Apps.

## Architecture

The application consists of:
- **Frontend**: React SPA served via Nginx
- **Backend**: Python FastAPI application
- **Database**: Azure PostgreSQL Flexible Server
- **Storage**: Azure Blob Storage for videos
- **Container Registry**: Azure Container Registry (ACR)
- **Hosting**: Azure Container Apps

## Prerequisites

1. Azure subscription
2. Azure CLI installed: `az --version`
3. Docker installed
4. Azure OpenAI access with Sora-2 deployment

## Setup Steps

### 1. Provision Azure Resources

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "<your-subscription-id>"

# Create resource group
az group create \
  --name rg-coca-cola-video-studio \
  --location eastus

# Create Azure Container Registry
az acr create \
  --resource-group rg-coca-cola-video-studio \
  --name cocacolavideostudio \
  --sku Basic

# Enable admin access
az acr update -n cocacolavideostudio --admin-enabled true

# Get ACR credentials
az acr credential show --name cocacolavideostudio
```

### 2. Deploy Infrastructure

```bash
# Navigate to infrastructure directory
cd infrastructure

# Deploy using Bicep
az deployment group create \
  --resource-group rg-coca-cola-video-studio \
  --template-file main.bicep \
  --parameters \
    containerRegistryName=cocacolavideostudio \
    postgresServerName=coca-cola-video-db \
    storageAccountName=cocacolavideostorage \
    azureOpenAIEndpoint='https://your-openai.openai.azure.com/' \
    azureOpenAIKey='your-api-key' \
    postgresAdminPassword='YourSecurePassword123!' \
    jwtSecretKey='your-jwt-secret-key-change-this'
```

### 3. Build and Push Container Images

```bash
# Login to ACR
az acr login --name cocacolavideostudio

# Build and push backend
cd backend
docker build -t cocacolavideostudio.azurecr.io/coca-cola-video-backend:latest .
docker push cocacolavideostudio.azurecr.io/coca-cola-video-backend:latest

# Build and push frontend
cd ../frontend
docker build -t cocacolavideostudio.azurecr.io/coca-cola-video-frontend:latest .
docker push cocacolavideostudio.azurecr.io/coca-cola-video-frontend:latest
```

### 4. Initialize Database

```bash
# Connect to the backend container
az containerapp exec \
  --name coca-cola-video-backend \
  --resource-group rg-coca-cola-video-studio \
  --command /bin/bash

# Inside the container, run migrations
# (This assumes you've set up Alembic migrations)
alembic upgrade head
```

### 5. Configure GitHub Actions (Optional)

For CI/CD automation:

1. Create a service principal:
```bash
az ad sp create-for-rbac \
  --name "coca-cola-video-studio-github" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/rg-coca-cola-video-studio \
  --sdk-auth
```

2. Add GitHub secrets:
   - `AZURE_CREDENTIALS`: Output from the above command
   - `ACR_NAME`: `cocacolavideostudio`
   - `ACR_USERNAME`: From `az acr credential show`
   - `ACR_PASSWORD`: From `az acr credential show`
   - `AZURE_RESOURCE_GROUP`: `rg-coca-cola-video-studio`

3. Push to `main` branch to trigger deployment

## Environment Variables

### Backend
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_DEPLOYMENT`: Sora-2 deployment name
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key

### Frontend
- `VITE_API_URL`: Backend API URL

## Scaling

Azure Container Apps automatically scales based on HTTP traffic:
- **Backend**: 1-5 replicas
- **Frontend**: 1-3 replicas

Modify scaling in `main.bicep`:
```bicep
scale: {
  minReplicas: 1
  maxReplicas: 10
  rules: [
    {
      name: 'http-rule'
      http: {
        metadata: {
          concurrentRequests: '10'
        }
      }
    }
  ]
}
```

## Monitoring

1. **Application Insights**: Automatically configured with Container Apps
2. **Container Logs**:
```bash
az containerapp logs show \
  --name coca-cola-video-backend \
  --resource-group rg-coca-cola-video-studio \
  --follow
```

3. **Metrics**: View in Azure Portal under Container Apps

## Costs Estimate

Monthly costs (approximate):
- Container Apps: $50-200 (based on usage)
- PostgreSQL Flexible Server (B1ms): $15
- Azure Storage: $5-50 (based on video storage)
- Azure OpenAI Sora-2: Pay-per-use (varies)
- Container Registry (Basic): $5

**Total**: ~$75-270/month + Azure OpenAI usage

## Security Considerations

1. **Secrets Management**: Use Azure Key Vault for production
2. **Network Security**: Configure VNET integration
3. **Authentication**: Implement Azure AD authentication
4. **HTTPS**: Enabled by default on Container Apps
5. **Database**: Enable SSL/TLS connections

## Troubleshooting

### Backend won't start
```bash
# Check logs
az containerapp logs show --name coca-cola-video-backend --resource-group rg-coca-cola-video-studio --tail 100

# Check environment variables
az containerapp show --name coca-cola-video-backend --resource-group rg-coca-cola-video-studio --query properties.template.containers[0].env
```

### Database connection issues
- Verify PostgreSQL firewall rules allow Azure services
- Check connection string format
- Ensure database and user exist

### Frontend can't connect to backend
- Verify CORS settings in backend
- Check `VITE_API_URL` points to backend URL
- Inspect browser console for errors

## Local Development

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Then run with Docker Compose
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Production Checklist

- [ ] Change all default passwords
- [ ] Configure custom domain
- [ ] Set up Azure Key Vault
- [ ] Enable Application Insights
- [ ] Configure backup for PostgreSQL
- [ ] Set up Azure CDN for static assets
- [ ] Implement rate limiting
- [ ] Configure auto-scaling rules
- [ ] Set up monitoring alerts
- [ ] Enable Azure AD authentication
