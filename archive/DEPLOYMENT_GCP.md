# GCP Deployment Guide

This guide provides step-by-step instructions for deploying the Student Loan Document Extractor Platform on Google Cloud Platform (GCP).

## Architecture Overview

The GCP deployment uses the following services:
- **Cloud Run**: Serverless container platform for API and Dashboard services
- **GKE (Google Kubernetes Engine)**: Container orchestration for Worker services (alternative)
- **Cloud SQL for PostgreSQL**: Managed database service
- **Cloud Storage**: Object storage for loan documents
- **Memorystore for Redis**: Managed Redis for caching and job queues
- **Cloud Load Balancing**: Load balancing and SSL termination
- **Cloud Logging**: Centralized logging
- **Secret Manager**: Secure storage for credentials
- **VPC**: Network isolation and security

## Prerequisites

1. GCP Account with billing enabled
2. gcloud CLI installed and configured
3. Docker installed locally
4. kubectl installed (if using GKE)

## Step 1: Set Up Project and Enable APIs

```bash
# Set project ID
export PROJECT_ID=loan-extractor-prod
export REGION=us-central1
export ZONE=us-central1-a

# Create new project (or use existing)
gcloud projects create $PROJECT_ID --name="Loan Document Extractor"

# Set current project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  compute.googleapis.com \
  container.googleapis.com \
  sqladmin.googleapis.com \
  storage.googleapis.com \
  redis.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  cloudresourcemanager.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com
```

## Step 2: Set Up VPC Network

```bash
# Create VPC network
gcloud compute networks create loan-extractor-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create loan-extractor-subnet \
  --network=loan-extractor-vpc \
  --region=$REGION \
  --range=10.0.0.0/24

# Create firewall rules
gcloud compute firewall-rules create allow-internal \
  --network=loan-extractor-vpc \
  --allow=tcp,udp,icmp \
  --source-ranges=10.0.0.0/24

gcloud compute firewall-rules create allow-ssh \
  --network=loan-extractor-vpc \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0
```

## Step 3: Set Up Cloud SQL for PostgreSQL

```bash
# Create Cloud SQL instance
gcloud sql instances create loan-extractor-db \
  --database-version=POSTGRES_15 \
  --tier=db-custom-2-7680 \
  --region=$REGION \
  --network=projects/$PROJECT_ID/global/networks/loan-extractor-vpc \
  --no-assign-ip \
  --storage-type=SSD \
  --storage-size=100GB \
  --storage-auto-increase \
  --backup-start-time=03:00 \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=04

# Set root password
gcloud sql users set-password postgres \
  --instance=loan-extractor-db \
  --password=<secure-password>

# Create database
gcloud sql databases create loanextractor \
  --instance=loan-extractor-db

# Create application user
gcloud sql users create loanuser \
  --instance=loan-extractor-db \
  --password=<secure-password>

# Get connection name
gcloud sql instances describe loan-extractor-db --format="value(connectionName)"
```

## Step 4: Set Up Cloud Storage

```bash
# Create bucket for documents
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION gs://loan-extractor-documents-prod/

# Enable versioning
gsutil versioning set on gs://loan-extractor-documents-prod/

# Set lifecycle policy (optional)
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 365,
          "matchesPrefix": ["archived/"]
        }
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://loan-extractor-documents-prod/

# Set IAM permissions
gsutil iam ch serviceAccount:<service-account>@$PROJECT_ID.iam.gserviceaccount.com:objectAdmin \
  gs://loan-extractor-documents-prod/
```

## Step 5: Set Up Memorystore for Redis

```bash
# Create Redis instance
gcloud redis instances create loan-extractor-redis \
  --size=5 \
  --region=$REGION \
  --redis-version=redis_7_0 \
  --network=projects/$PROJECT_ID/global/networks/loan-extractor-vpc \
  --tier=standard

# Get Redis host and port
gcloud redis instances describe loan-extractor-redis \
  --region=$REGION \
  --format="value(host,port)"
```

## Step 6: Store Secrets in Secret Manager

```bash
# Create secrets
echo -n "postgresql://loanuser:<password>@<cloud-sql-connection>/loanextractor" | \
  gcloud secrets create database-url --data-file=-

echo -n "your-secret-key" | \
  gcloud secrets create app-secret-key --data-file=-

echo -n "your-encryption-key" | \
  gcloud secrets create app-encryption-key --data-file=-

# Grant access to service accounts
gcloud secrets add-iam-policy-binding database-url \
  --member="serviceAccount:<service-account>@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Step 7: Build and Push Docker Images to Container Registry

```bash
# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker

# Build images
docker build -t gcr.io/$PROJECT_ID/loan-extractor-api:latest --target api .
docker build -t gcr.io/$PROJECT_ID/loan-extractor-dashboard:latest --target dashboard .
docker build -t gcr.io/$PROJECT_ID/loan-extractor-worker:latest --target worker .

# Push images
docker push gcr.io/$PROJECT_ID/loan-extractor-api:latest
docker push gcr.io/$PROJECT_ID/loan-extractor-dashboard:latest
docker push gcr.io/$PROJECT_ID/loan-extractor-worker:latest
```

## Step 8: Deploy API Service to Cloud Run

```bash
# Create service account for Cloud Run
gcloud iam service-accounts create loan-extractor-api \
  --display-name="Loan Extractor API Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:loan-extractor-api@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:loan-extractor-api@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

# Deploy API to Cloud Run
gcloud run deploy loan-extractor-api \
  --image=gcr.io/$PROJECT_ID/loan-extractor-api:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --service-account=loan-extractor-api@$PROJECT_ID.iam.gserviceaccount.com \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:loan-extractor-db \
  --vpc-connector=loan-extractor-connector \
  --set-env-vars="API_HOST=0.0.0.0,API_PORT=8000" \
  --set-secrets="DATABASE_URL=database-url:latest,SECRET_KEY=app-secret-key:latest" \
  --memory=2Gi \
  --cpu=2 \
  --max-instances=10 \
  --min-instances=1 \
  --timeout=300

# Get service URL
gcloud run services describe loan-extractor-api \
  --region=$REGION \
  --format="value(status.url)"
```

## Step 9: Deploy Dashboard to Cloud Run

```bash
# Create service account for Dashboard
gcloud iam service-accounts create loan-extractor-dashboard \
  --display-name="Loan Extractor Dashboard Service Account"

# Deploy Dashboard
gcloud run deploy loan-extractor-dashboard \
  --image=gcr.io/$PROJECT_ID/loan-extractor-dashboard:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --service-account=loan-extractor-dashboard@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars="API_URL=<api-service-url>" \
  --memory=1Gi \
  --cpu=1 \
  --max-instances=5 \
  --port=8501
```

## Step 10: Deploy Worker Service (Option A: Cloud Run Jobs)

```bash
# Deploy worker as Cloud Run Job
gcloud run jobs create loan-extractor-worker \
  --image=gcr.io/$PROJECT_ID/loan-extractor-worker:latest \
  --region=$REGION \
  --service-account=loan-extractor-api@$PROJECT_ID.iam.gserviceaccount.com \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:loan-extractor-db \
  --vpc-connector=loan-extractor-connector \
  --set-secrets="DATABASE_URL=database-url:latest" \
  --memory=4Gi \
  --cpu=2 \
  --max-retries=3 \
  --task-timeout=3600

# Execute job
gcloud run jobs execute loan-extractor-worker --region=$REGION
```

## Step 11: Deploy Worker Service (Option B: GKE)

### Create GKE Cluster

```bash
# Create GKE cluster
gcloud container clusters create loan-extractor-cluster \
  --region=$REGION \
  --num-nodes=2 \
  --machine-type=n1-standard-2 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=5 \
  --enable-autorepair \
  --enable-autoupgrade \
  --network=loan-extractor-vpc \
  --subnetwork=loan-extractor-subnet \
  --enable-ip-alias \
  --enable-stackdriver-kubernetes

# Get cluster credentials
gcloud container clusters get-credentials loan-extractor-cluster --region=$REGION
```

### Deploy Worker to GKE

Create `worker-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-extractor-worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: loan-extractor-worker
  template:
    metadata:
      labels:
        app: loan-extractor-worker
    spec:
      serviceAccountName: loan-extractor-worker-sa
      containers:
      - name: worker
        image: gcr.io/PROJECT_ID/loan-extractor-worker:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        - name: REDIS_URL
          value: "redis://REDIS_HOST:6379/0"
        - name: WORKER_CONCURRENCY
          value: "2"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: loan-extractor-worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: loan-extractor-worker
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Deploy:
```bash
kubectl apply -f worker-deployment.yaml
```

## Step 12: Set Up VPC Connector (for Cloud Run)

```bash
# Create VPC connector for Cloud Run to access VPC resources
gcloud compute networks vpc-access connectors create loan-extractor-connector \
  --region=$REGION \
  --network=loan-extractor-vpc \
  --range=10.8.0.0/28 \
  --min-instances=2 \
  --max-instances=10
```

## Step 13: Configure Load Balancer (Optional)

For custom domain and SSL:

```bash
# Reserve static IP
gcloud compute addresses create loan-extractor-ip \
  --global

# Create SSL certificate
gcloud compute ssl-certificates create loan-extractor-cert \
  --domains=api.yourdomain.com,dashboard.yourdomain.com \
  --global

# Create backend services and URL maps
# (Detailed configuration depends on your routing needs)
```

## Step 14: Set Up Cloud Monitoring and Logging

```bash
# Create log sink for errors
gcloud logging sinks create loan-extractor-errors \
  bigquery.googleapis.com/projects/$PROJECT_ID/datasets/loan_extractor_logs \
  --log-filter='severity>=ERROR'

# Create uptime check
gcloud monitoring uptime create loan-extractor-api-uptime \
  --resource-type=uptime-url \
  --host=<api-url> \
  --path=/health

# Create alert policy
gcloud alpha monitoring policies create \
  --notification-channels=<channel-id> \
  --display-name="High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

## Step 15: Configure Cloud Scheduler (for periodic tasks)

```bash
# Create job to trigger worker processing
gcloud scheduler jobs create http process-documents \
  --schedule="0 */6 * * *" \
  --uri="<api-url>/api/v1/process-batch" \
  --http-method=POST \
  --oidc-service-account-email=loan-extractor-api@$PROJECT_ID.iam.gserviceaccount.com
```

## Monitoring and Maintenance

### View Logs

```bash
# View API logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=loan-extractor-api" \
  --limit=50 \
  --format=json

# Stream logs
gcloud logging tail "resource.type=cloud_run_revision" --format=json
```

### Update Services

```bash
# Build and push new image
docker build -t gcr.io/$PROJECT_ID/loan-extractor-api:v2 --target api .
docker push gcr.io/$PROJECT_ID/loan-extractor-api:v2

# Update Cloud Run service
gcloud run services update loan-extractor-api \
  --image=gcr.io/$PROJECT_ID/loan-extractor-api:v2 \
  --region=$REGION
```

### Scale Services

```bash
# Update Cloud Run scaling
gcloud run services update loan-extractor-api \
  --min-instances=2 \
  --max-instances=20 \
  --region=$REGION

# For GKE
kubectl scale deployment loan-extractor-worker --replicas=5
```

## Cost Optimization

1. Use Cloud Run for variable workloads (pay per request)
2. Enable Cloud Storage lifecycle management
3. Use committed use discounts for Cloud SQL
4. Configure appropriate autoscaling thresholds
5. Use preemptible VMs for GKE worker nodes
6. Set up budget alerts in Cloud Billing

## Security Best Practices

1. Enable VPC Service Controls
2. Use Cloud Armor for DDoS protection
3. Enable Binary Authorization for GKE
4. Implement least privilege IAM policies
5. Enable audit logging
6. Use Workload Identity for GKE
7. Regularly rotate secrets
8. Enable Security Command Center
9. Use Private Google Access for VPC
10. Implement Cloud KMS for encryption keys

## Backup and Disaster Recovery

```bash
# Enable automated Cloud SQL backups
gcloud sql instances patch loan-extractor-db \
  --backup-start-time=03:00 \
  --retained-backups-count=30

# Create on-demand backup
gcloud sql backups create \
  --instance=loan-extractor-db \
  --description="Pre-deployment backup"

# Enable Cloud Storage versioning (already done in Step 4)

# Export database for additional backup
gcloud sql export sql loan-extractor-db \
  gs://loan-extractor-backups/backup-$(date +%Y%m%d).sql \
  --database=loanextractor
```

## Troubleshooting

### Cloud Run Service Won't Start

1. Check Cloud Logging for container errors
2. Verify service account permissions
3. Ensure secrets are accessible
4. Check VPC connector configuration
5. Verify Cloud SQL connection

### Database Connection Issues

1. Verify Cloud SQL instance is running
2. Check service account has `cloudsql.client` role
3. Ensure VPC connector is properly configured
4. Verify connection string in secrets

### High Costs

1. Review Cloud Billing reports
2. Check Cloud Run request counts and execution times
3. Review Cloud SQL instance size
4. Check Cloud Storage usage
5. Enable cost optimization recommendations

## Multi-Region Deployment

For high availability across regions:

1. Deploy Cloud Run services in multiple regions
2. Use Cloud Load Balancing for global distribution
3. Set up Cloud SQL read replicas in other regions
4. Configure multi-regional Cloud Storage buckets
5. Use Cloud CDN for static content

## CI/CD Integration

### Using Cloud Build

Create `cloudbuild.yaml`:

```yaml
steps:
  # Build images
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/loan-extractor-api:$COMMIT_SHA', '--target', 'api', '.']
  
  # Push images
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/loan-extractor-api:$COMMIT_SHA']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'loan-extractor-api'
      - '--image=gcr.io/$PROJECT_ID/loan-extractor-api:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'

images:
  - 'gcr.io/$PROJECT_ID/loan-extractor-api:$COMMIT_SHA'
```

Set up trigger:
```bash
gcloud builds triggers create github \
  --repo-name=loan-extractor \
  --repo-owner=your-org \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

## Compliance and Governance

1. Enable Data Loss Prevention (DLP) API for sensitive data scanning
2. Configure Organization Policy constraints
3. Use Cloud Asset Inventory for resource tracking
4. Implement VPC Service Controls for data perimeter
5. Enable Access Transparency logs
6. Configure compliance reports in Security Command Center
