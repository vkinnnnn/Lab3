# Docker Quick Start Guide

Get the Student Loan Document Extractor Platform running in 5 minutes!

## Prerequisites

- Docker Desktop installed (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- At least 8GB RAM available for Docker
- 20GB free disk space

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd Lab3
```

### 2. Set Up Environment

```bash
# Copy the example environment file
cp .env.example .env

# (Optional) Edit .env to customize settings
# For local development, the defaults work fine
```

### 3. Start All Services

```bash
# Start all services in detached mode
docker-compose up -d

# This will:
# - Download required Docker images
# - Build custom images for API, Dashboard, and Worker
# - Start PostgreSQL, MinIO, Redis, API, Dashboard, and Worker
# - Set up networking between services
```

### 4. Wait for Services to Initialize

```bash
# Check service status
docker-compose ps

# All services should show "Up" status
# Wait about 30-60 seconds for everything to be ready
```

### 5. Access the Application

Open your browser and navigate to:

- **Dashboard (Main UI):** http://localhost:8501
- **API Documentation:** http://localhost:8000/docs
- **MinIO Console:** http://localhost:9001
  - Username: `minioadmin`
  - Password: `minioadmin123`

## First Time Setup

### Initialize the Database

```bash
# Run database initialization
docker-compose exec api python -m storage.setup_storage
```

### Create MinIO Bucket

The bucket should be created automatically, but if needed:

1. Go to http://localhost:9001
2. Login with credentials above
3. Create bucket named `loan-documents`

## Using the Application

### Upload a Document

1. Open http://localhost:8501
2. Click "Upload Documents" in the sidebar
3. Drag and drop a loan document (PDF, JPEG, PNG, or TIFF)
4. Wait for processing to complete
5. View extracted data

### View Extracted Data

1. Navigate to "View Extracted Data"
2. Select a processed document
3. Review extracted loan information

### Compare Loans

1. Upload multiple loan documents
2. Navigate to "Compare Loans"
3. Select documents to compare
4. View side-by-side comparison

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove all data (clean slate)
docker-compose down -v
```

## Viewing Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f dashboard
docker-compose logs -f worker
```

## Troubleshooting

### Port Already in Use

If you get port conflict errors:

```bash
# Check what's using the port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Change ports in .env file
API_PORT=8001
DASHBOARD_PORT=8502
```

### Services Won't Start

```bash
# Check logs for errors
docker-compose logs

# Try clean restart
docker-compose down -v
docker-compose up -d
```

### Out of Memory

Increase Docker memory limit:
- Docker Desktop: Settings → Resources → Memory (set to 8GB+)
- Linux: Adjust Docker daemon settings

### Database Connection Errors

```bash
# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db

# Reinitialize database
docker-compose exec api python -m storage.setup_storage
```

## Development Mode

For development with hot-reload:

```bash
# Start in development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# This enables:
# - Code hot-reloading
# - PgAdmin at http://localhost:5050
# - Debug logging
# - Volume mounts for live editing
```

## Next Steps

- Read [DOCKER_README.md](./DOCKER_README.md) for detailed Docker commands
- Read [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- Check [DEPLOYMENT_AWS.md](./DEPLOYMENT_AWS.md) for AWS deployment
- Check [DEPLOYMENT_GCP.md](./DEPLOYMENT_GCP.md) for GCP deployment

## Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Rebuild images
docker-compose build

# Clean everything
docker-compose down -v
```

## Getting Help

- Check service logs: `docker-compose logs -f`
- Check service status: `docker-compose ps`
- Review [DOCKER_README.md](./DOCKER_README.md)
- Check API documentation: http://localhost:8000/docs

## Success!

You should now have the Student Loan Document Extractor Platform running locally. Try uploading a sample loan document to test the system!
