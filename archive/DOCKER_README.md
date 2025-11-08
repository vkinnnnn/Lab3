# Docker Deployment Quick Reference

Quick reference guide for Docker-based deployment of the Student Loan Document Extractor Platform.

## Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start all services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f

# 5. Access services
# Dashboard: http://localhost:8501
# API: http://localhost:8000
# MinIO Console: http://localhost:9001
```

## Common Commands

### Service Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart api

# View running services
docker-compose ps

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f dashboard
docker-compose logs -f worker

# View last 100 lines
docker-compose logs --tail=100 api

# Open shell in container
docker-compose exec api /bin/bash
docker-compose exec worker /bin/bash

# Run command in container
docker-compose exec api python -m storage.setup_storage
```

### Building and Updating

```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Build specific service
docker-compose build api

# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

## Development Mode

```bash
# Start with development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Build development images
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

# Stop development services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

Development mode includes:
- Hot reload for code changes
- PgAdmin at http://localhost:5050
- Debug logging enabled
- Volume mounts for live editing

## Service Details

### API Service
- **Port:** 8000
- **Health Check:** http://localhost:8000/health
- **Documentation:** http://localhost:8000/docs
- **Container:** loan-extractor-api

### Dashboard Service
- **Port:** 8501
- **URL:** http://localhost:8501
- **Container:** loan-extractor-dashboard

### Worker Service
- **Container:** loan-extractor-worker
- **Purpose:** Background document processing

### PostgreSQL Database
- **Port:** 5432
- **Database:** loanextractor
- **User:** loanuser (default)
- **Container:** loan-extractor-db

### MinIO Object Storage
- **API Port:** 9000
- **Console Port:** 9001
- **Console URL:** http://localhost:9001
- **Default Credentials:** minioadmin / minioadmin123
- **Container:** loan-extractor-minio

### Redis Cache
- **Port:** 6379
- **Container:** loan-extractor-redis

## Environment Configuration

Edit `.env` file to customize:

```bash
# Database
POSTGRES_DB=loanextractor
POSTGRES_USER=loanuser
POSTGRES_PASSWORD=loanpass123

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

# API
API_PORT=8000
API_WORKERS=4

# Dashboard
DASHBOARD_PORT=8501

# Worker
WORKER_CONCURRENCY=2
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs for errors
docker-compose logs

# Check if ports are already in use
netstat -an | grep 8000
netstat -an | grep 8501
netstat -an | grep 5432

# Remove old containers and volumes
docker-compose down -v
docker-compose up -d
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Connect to database
docker-compose exec db psql -U loanuser -d loanextractor

# Reinitialize database
docker-compose exec api python -m storage.setup_storage
```

### Out of Memory

```bash
# Check container resource usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Recommended: At least 8GB RAM

# Reduce worker concurrency in .env
WORKER_CONCURRENCY=1
```

### Permission Issues

```bash
# Fix volume permissions (Linux/Mac)
sudo chown -R $USER:$USER uploads/ temp/ processing/

# Windows: Run Docker Desktop as Administrator
```

### Clean Start

```bash
# Stop everything
docker-compose down -v

# Remove all data
rm -rf uploads/* temp/* processing/*

# Rebuild and start
docker-compose build --no-cache
docker-compose up -d

# Reinitialize
docker-compose exec api python -m storage.setup_storage
```

## Data Persistence

Data is stored in Docker volumes:

```bash
# List volumes
docker volume ls | grep loan

# Inspect volume
docker volume inspect lab3_postgres_data

# Backup volume
docker run --rm -v lab3_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz -C /data .

# Restore volume
docker run --rm -v lab3_postgres_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

## Performance Tuning

### API Service

```yaml
# In docker-compose.yml
api:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
      reservations:
        cpus: '1'
        memory: 2G
```

### Worker Service

```yaml
worker:
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 8G
  environment:
    WORKER_CONCURRENCY: 4
```

### Database

```yaml
db:
  command: postgres -c max_connections=200 -c shared_buffers=256MB
```

## Monitoring

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check all services
docker-compose ps

# Check resource usage
docker stats
```

### Logs

```bash
# Follow all logs
docker-compose logs -f

# Filter by level
docker-compose logs | grep ERROR

# Export logs
docker-compose logs > logs.txt
```

## Scaling

### Scale Worker Instances

```bash
# Scale to 3 workers
docker-compose up -d --scale worker=3

# Scale back to 1
docker-compose up -d --scale worker=1
```

### Scale API Instances (with load balancer)

```bash
# Scale to 3 API instances
docker-compose up -d --scale api=3

# Note: Requires load balancer configuration
```

## Security

### Change Default Passwords

Edit `.env`:
```bash
POSTGRES_PASSWORD=<strong-password>
MINIO_ROOT_PASSWORD=<strong-password>
SECRET_KEY=<random-secret-key>
ENCRYPTION_KEY=<random-encryption-key>
```

### Generate Secure Keys

```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate encryption key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Enable HTTPS (Production)

Use a reverse proxy like Nginx or Traefik:

```yaml
# docker-compose.prod.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
```

## Backup and Restore

### Database Backup

```bash
# Backup database
docker-compose exec -T db pg_dump -U loanuser loanextractor > backup.sql

# Restore database
docker-compose exec -T db psql -U loanuser loanextractor < backup.sql
```

### MinIO Backup

```bash
# Backup MinIO data
docker-compose exec minio mc mirror /data /backup

# Or use volume backup method shown above
```

## Useful Makefile Commands

If using `Makefile.docker`:

```bash
# Show available commands
make -f Makefile.docker help

# Complete setup
make -f Makefile.docker setup

# Start services
make -f Makefile.docker up

# Stop services
make -f Makefile.docker down

# View logs
make -f Makefile.docker logs

# Clean everything
make -f Makefile.docker clean

# Development mode
make -f Makefile.docker dev-up
```

## Production Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Generate secure secret keys
- [ ] Configure proper resource limits
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Enable HTTPS/TLS
- [ ] Set up monitoring and alerts
- [ ] Configure firewall rules
- [ ] Test disaster recovery procedures
- [ ] Document custom configuration
- [ ] Set up CI/CD pipeline
- [ ] Perform security audit
- [ ] Load test the system

## Getting Help

- Check logs: `docker-compose logs -f`
- Check service status: `docker-compose ps`
- Check resource usage: `docker stats`
- Review documentation: `DEPLOYMENT.md`
- Check API docs: http://localhost:8000/docs

## Additional Resources

- [Full Deployment Guide](./DEPLOYMENT.md)
- [AWS Deployment Guide](./DEPLOYMENT_AWS.md)
- [GCP Deployment Guide](./DEPLOYMENT_GCP.md)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Documentation](https://docs.docker.com/)
