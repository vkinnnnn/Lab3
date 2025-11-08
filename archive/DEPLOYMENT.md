# Deployment Guide

This document provides an overview of deployment options for the Student Loan Document Extractor Platform.

## Deployment Options

The platform can be deployed in several ways:

1. **Local Development** - Docker Compose on local machine
2. **Cloud Deployment** - AWS or GCP managed services
3. **Kubernetes** - Self-managed or managed Kubernetes clusters
4. **Hybrid** - Mix of cloud and on-premises infrastructure

## Quick Start - Local Deployment

### Prerequisites

- Docker and Docker Compose installed
- At least 8GB RAM available
- 20GB free disk space

### Steps

1. Clone the repository and navigate to the project directory:
```bash
cd Lab3
```

2. Copy the environment template:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration (optional for local development)

4. Start all services:
```bash
docker-compose up -d
```

5. Wait for services to be ready (about 30 seconds):
```bash
docker-compose ps
```

6. Access the application:
   - Dashboard: http://localhost:8501
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001

7. Initialize the database (first time only):
```bash
docker-compose exec api python -m storage.setup_storage
```

### Development Mode

For development with hot-reload:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This enables:
- Code hot-reloading for API and Dashboard
- PgAdmin for database management (http://localhost:5050)
- Volume mounts for live code editing

## Cloud Deployment

### AWS Deployment

For detailed AWS deployment instructions, see [DEPLOYMENT_AWS.md](./DEPLOYMENT_AWS.md).

**Key Services:**
- ECS Fargate for container orchestration
- RDS PostgreSQL for database
- S3 for object storage
- ElastiCache Redis for caching
- Application Load Balancer for routing

**Estimated Monthly Cost (Production):**
- Small: $200-400 (2 API instances, small RDS)
- Medium: $500-800 (4 API instances, medium RDS)
- Large: $1000-2000 (10+ API instances, large RDS with replicas)

### GCP Deployment

For detailed GCP deployment instructions, see [DEPLOYMENT_GCP.md](./DEPLOYMENT_GCP.md).

**Key Services:**
- Cloud Run for serverless containers
- Cloud SQL for PostgreSQL
- Cloud Storage for objects
- Memorystore for Redis
- Cloud Load Balancing

**Estimated Monthly Cost (Production):**
- Small: $150-350 (Cloud Run with minimal traffic)
- Medium: $400-700 (Higher traffic, larger Cloud SQL)
- Large: $900-1800 (High traffic, GKE for workers)

## Architecture Components

### Services

1. **API Service**
   - FastAPI application
   - Handles document uploads and processing requests
   - Exposes REST API endpoints
   - Port: 8000

2. **Dashboard Service**
   - Streamlit web application
   - User interface for document upload and analysis
   - Port: 8501

3. **Worker Service**
   - Background processing for document extraction
   - OCR and data extraction tasks
   - Batch processing

4. **PostgreSQL Database**
   - Stores document metadata and extracted data
   - Port: 5432

5. **MinIO/S3**
   - Object storage for uploaded documents
   - Port: 9000 (API), 9001 (Console)

6. **Redis**
   - Caching and job queue
   - Port: 6379

### Network Architecture

```
┌─────────────┐
│   Internet  │
└──────┬──────┘
       │
┌──────▼──────────────────────────────┐
│     Load Balancer / Ingress         │
└──────┬──────────────────────────────┘
       │
       ├─────────────┬─────────────────┐
       │             │                 │
┌──────▼──────┐ ┌───▼────────┐ ┌──────▼──────┐
│     API     │ │ Dashboard  │ │   Worker    │
│  (Port 8000)│ │(Port 8501) │ │             │
└──────┬──────┘ └─────┬──────┘ └──────┬──────┘
       │              │               │
       └──────────────┴───────────────┘
                      │
       ┌──────────────┼──────────────┐
       │              │              │
┌──────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
│  PostgreSQL │ │  MinIO/S3│ │    Redis    │
│ (Port 5432) │ │(Port 9000│ │ (Port 6379) │
└─────────────┘ └──────────┘ └─────────────┘
```

## Environment Variables

### Required Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Object Storage
S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123
S3_BUCKET_NAME=loan-documents

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key
ENCRYPTION_KEY=your-encryption-key
```

### Optional Variables

```bash
# API Configuration
API_WORKERS=4
MAX_FILE_SIZE_MB=50
MAX_PAGES=50

# Worker Configuration
WORKER_CONCURRENCY=2

# Logging
LOG_LEVEL=INFO
DEBUG=false
```

## Scaling Considerations

### Horizontal Scaling

**API Service:**
- Scale based on request rate
- Target: 70% CPU utilization
- Min instances: 2
- Max instances: 10+

**Worker Service:**
- Scale based on queue depth
- Target: 80% CPU utilization
- Min instances: 1
- Max instances: 5+

**Dashboard:**
- Scale based on concurrent users
- Min instances: 1
- Max instances: 3

### Vertical Scaling

**API Service:**
- CPU: 1-2 cores per instance
- Memory: 2-4 GB per instance

**Worker Service:**
- CPU: 2-4 cores per instance
- Memory: 4-8 GB per instance (OCR is memory-intensive)

**Database:**
- Start: 2 cores, 8 GB RAM
- Production: 4+ cores, 16+ GB RAM

## Performance Optimization

### Database

1. Enable connection pooling
2. Create indexes on frequently queried fields
3. Use read replicas for reporting queries
4. Regular VACUUM and ANALYZE operations

### Caching

1. Cache OCR results for duplicate documents
2. Cache API responses for common queries
3. Use Redis for session management
4. Implement CDN for static assets

### Storage

1. Use lifecycle policies to archive old documents
2. Enable compression for stored documents
3. Use appropriate storage classes (Standard, Infrequent Access)
4. Implement multipart uploads for large files

### Application

1. Enable async processing for long-running tasks
2. Implement request queuing for batch operations
3. Use connection pooling for database and Redis
4. Optimize OCR preprocessing pipeline

## Monitoring and Observability

### Key Metrics

**Application Metrics:**
- Request rate and latency
- Error rate by endpoint
- Document processing time
- Queue depth and processing rate

**Infrastructure Metrics:**
- CPU and memory utilization
- Disk I/O and network throughput
- Database connections and query performance
- Cache hit rate

**Business Metrics:**
- Documents processed per day
- Average extraction accuracy
- User engagement metrics
- Cost per document processed

### Logging

Structured logging format:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "api",
  "message": "Document processed",
  "document_id": "abc123",
  "processing_time": 12.5,
  "confidence": 0.95
}
```

### Alerting

Set up alerts for:
- High error rates (>5%)
- Slow response times (>5s p95)
- High queue depth (>100 items)
- Low disk space (<20%)
- Database connection failures
- Service health check failures

## Security

### Network Security

1. Use private subnets for databases and workers
2. Implement security groups/firewall rules
3. Enable VPC flow logs
4. Use VPN or private connectivity for sensitive data

### Application Security

1. Enable HTTPS/TLS for all external endpoints
2. Implement rate limiting and request throttling
3. Use API keys or OAuth for authentication
4. Validate and sanitize all inputs
5. Implement CORS policies

### Data Security

1. Encrypt data at rest (database and storage)
2. Encrypt data in transit (TLS 1.3)
3. Implement role-based access control (RBAC)
4. Regular security audits and penetration testing
5. Secure secret management (AWS Secrets Manager, GCP Secret Manager)

### Compliance

1. GDPR compliance for EU users
2. COPPA compliance for student data
3. Regular data retention and deletion policies
4. Audit logging for all data access
5. Data processing agreements with cloud providers

## Backup and Disaster Recovery

### Backup Strategy

**Database:**
- Automated daily backups
- Point-in-time recovery enabled
- Retention: 30 days
- Test restores monthly

**Object Storage:**
- Versioning enabled
- Cross-region replication (production)
- Lifecycle policies for old versions

**Configuration:**
- Infrastructure as Code (Terraform/CloudFormation)
- Version control for all configurations
- Documented deployment procedures

### Disaster Recovery

**RTO (Recovery Time Objective):** 4 hours
**RPO (Recovery Point Objective):** 1 hour

**Recovery Procedures:**
1. Restore database from latest backup
2. Restore object storage from replica
3. Deploy services from container registry
4. Update DNS to point to new infrastructure
5. Verify functionality with smoke tests

## Troubleshooting

### Common Issues

**Service Won't Start:**
- Check logs: `docker-compose logs <service>`
- Verify environment variables
- Ensure dependencies are healthy
- Check resource availability

**Database Connection Errors:**
- Verify database is running
- Check connection string
- Verify network connectivity
- Check firewall rules

**OCR Processing Failures:**
- Verify Tesseract installation
- Check file format compatibility
- Ensure sufficient memory
- Review preprocessing steps

**High Memory Usage:**
- Check for memory leaks in logs
- Review worker concurrency settings
- Optimize image preprocessing
- Consider vertical scaling

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error logs
- Check service health
- Review performance metrics

**Weekly:**
- Review and rotate logs
- Check backup success
- Update security patches

**Monthly:**
- Review and optimize costs
- Test disaster recovery procedures
- Update dependencies
- Performance tuning

### Updates and Upgrades

1. Test updates in staging environment
2. Create backup before deployment
3. Use blue-green or canary deployments
4. Monitor closely after deployment
5. Have rollback plan ready

## Support and Resources

### Documentation

- API Documentation: `/docs` endpoint (Swagger UI)
- Architecture diagrams: `docs/architecture/`
- Runbooks: `docs/runbooks/`

### Getting Help

- GitHub Issues: Report bugs and feature requests
- Documentation: Check README and deployment guides
- Logs: Review application and infrastructure logs
- Monitoring: Check dashboards for anomalies

## Next Steps

1. Choose your deployment platform (Local, AWS, or GCP)
2. Follow the detailed deployment guide for your platform
3. Configure monitoring and alerting
4. Set up CI/CD pipeline
5. Perform load testing
6. Document your specific configuration
7. Train your team on operations and troubleshooting
