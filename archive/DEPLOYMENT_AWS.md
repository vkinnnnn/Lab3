# AWS Deployment Guide

This guide provides step-by-step instructions for deploying the Student Loan Document Extractor Platform on AWS.

## Architecture Overview

The AWS deployment uses the following services:
- **ECS (Elastic Container Service)**: Container orchestration for API, Dashboard, and Worker services
- **RDS PostgreSQL**: Managed database service
- **S3**: Object storage for loan documents
- **ElastiCache Redis**: Managed Redis for caching and job queues
- **Application Load Balancer (ALB)**: Load balancing for API and Dashboard
- **CloudWatch**: Logging and monitoring
- **Secrets Manager**: Secure storage for credentials
- **VPC**: Network isolation and security

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Docker installed locally
4. Terraform (optional, for infrastructure as code)

## Step 1: Set Up VPC and Networking

### Using AWS Console

1. Navigate to VPC Dashboard
2. Create a new VPC:
   - Name: `loan-extractor-vpc`
   - IPv4 CIDR: `10.0.0.0/16`
   - Enable DNS hostnames and DNS resolution

3. Create Subnets:
   - Public Subnet 1: `10.0.1.0/24` (us-east-1a)
   - Public Subnet 2: `10.0.2.0/24` (us-east-1b)
   - Private Subnet 1: `10.0.11.0/24` (us-east-1a)
   - Private Subnet 2: `10.0.12.0/24` (us-east-1b)

4. Create Internet Gateway and attach to VPC

5. Create NAT Gateways in public subnets (for private subnet internet access)

6. Configure Route Tables:
   - Public route table: Route `0.0.0.0/0` to Internet Gateway
   - Private route tables: Route `0.0.0.0/0` to NAT Gateway

### Using AWS CLI

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=loan-extractor-vpc}]'

# Note the VPC ID from output
export VPC_ID=<your-vpc-id>

# Create subnets (repeat for each subnet)
aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
```

## Step 2: Set Up RDS PostgreSQL

1. Navigate to RDS Dashboard
2. Click "Create database"
3. Configuration:
   - Engine: PostgreSQL 15
   - Template: Production (or Dev/Test for non-production)
   - DB instance identifier: `loan-extractor-db`
   - Master username: `loanuser`
   - Master password: (use strong password)
   - DB instance class: `db.t3.medium` (adjust based on load)
   - Storage: 100 GB SSD (with autoscaling enabled)
   - VPC: Select `loan-extractor-vpc`
   - Subnet group: Create new with private subnets
   - Public access: No
   - VPC security group: Create new `loan-extractor-db-sg`
   - Database name: `loanextractor`

4. Configure Security Group:
   - Allow inbound PostgreSQL (5432) from ECS security group

5. Note the endpoint URL for later use

## Step 3: Set Up S3 Bucket

```bash
# Create S3 bucket
aws s3 mb s3://loan-extractor-documents-prod --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket loan-extractor-documents-prod \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket loan-extractor-documents-prod \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Configure lifecycle policy (optional)
aws s3api put-bucket-lifecycle-configuration \
  --bucket loan-extractor-documents-prod \
  --lifecycle-configuration file://s3-lifecycle.json
```

## Step 4: Set Up ElastiCache Redis

1. Navigate to ElastiCache Dashboard
2. Click "Create" and select Redis
3. Configuration:
   - Cluster mode: Disabled
   - Name: `loan-extractor-redis`
   - Engine version: 7.0
   - Node type: `cache.t3.medium`
   - Number of replicas: 1 (for high availability)
   - Subnet group: Create new with private subnets
   - Security group: Create new `loan-extractor-redis-sg`

4. Configure Security Group:
   - Allow inbound Redis (6379) from ECS security group

## Step 5: Store Secrets in AWS Secrets Manager

```bash
# Create secret for database credentials
aws secretsmanager create-secret \
  --name loan-extractor/database \
  --secret-string '{
    "username": "loanuser",
    "password": "your-secure-password",
    "host": "your-rds-endpoint",
    "port": "5432",
    "database": "loanextractor"
  }'

# Create secret for S3 credentials (if using IAM roles, this may not be needed)
aws secretsmanager create-secret \
  --name loan-extractor/s3 \
  --secret-string '{
    "bucket": "loan-extractor-documents-prod",
    "region": "us-east-1"
  }'

# Create secret for application keys
aws secretsmanager create-secret \
  --name loan-extractor/app \
  --secret-string '{
    "secret_key": "your-secret-key",
    "encryption_key": "your-encryption-key"
  }'
```

## Step 6: Create ECR Repositories

```bash
# Create repositories for each service
aws ecr create-repository --repository-name loan-extractor/api
aws ecr create-repository --repository-name loan-extractor/dashboard
aws ecr create-repository --repository-name loan-extractor/worker

# Get login credentials
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

## Step 7: Build and Push Docker Images

```bash
# Set variables
export AWS_ACCOUNT_ID=<your-account-id>
export AWS_REGION=us-east-1
export ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build images
docker build -t loan-extractor/api:latest --target api .
docker build -t loan-extractor/dashboard:latest --target dashboard .
docker build -t loan-extractor/worker:latest --target worker .

# Tag images
docker tag loan-extractor/api:latest $ECR_REGISTRY/loan-extractor/api:latest
docker tag loan-extractor/dashboard:latest $ECR_REGISTRY/loan-extractor/dashboard:latest
docker tag loan-extractor/worker:latest $ECR_REGISTRY/loan-extractor/worker:latest

# Push images
docker push $ECR_REGISTRY/loan-extractor/api:latest
docker push $ECR_REGISTRY/loan-extractor/dashboard:latest
docker push $ECR_REGISTRY/loan-extractor/worker:latest
```

## Step 8: Create ECS Cluster

1. Navigate to ECS Dashboard
2. Click "Create Cluster"
3. Configuration:
   - Cluster name: `loan-extractor-cluster`
   - Infrastructure: AWS Fargate
   - Monitoring: Enable Container Insights

## Step 9: Create Task Definitions

### API Task Definition

Create file `task-definition-api.json`:

```json
{
  "family": "loan-extractor-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/loan-extractor/api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "API_HOST",
          "value": "0.0.0.0"
        },
        {
          "name": "API_PORT",
          "value": "8000"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:loan-extractor/database"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/loan-extractor-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register task definition:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition-api.json
```

Repeat similar process for Dashboard and Worker services.

## Step 10: Create Application Load Balancer

1. Navigate to EC2 > Load Balancers
2. Create Application Load Balancer:
   - Name: `loan-extractor-alb`
   - Scheme: Internet-facing
   - IP address type: IPv4
   - VPC: Select `loan-extractor-vpc`
   - Subnets: Select public subnets
   - Security group: Create new allowing HTTP (80) and HTTPS (443)

3. Create Target Groups:
   - API Target Group: Port 8000, Health check path `/health`
   - Dashboard Target Group: Port 8501, Health check path `/`

4. Configure Listeners:
   - HTTP:80 → Forward to API target group
   - HTTP:8501 → Forward to Dashboard target group

## Step 11: Create ECS Services

### API Service

```bash
aws ecs create-service \
  --cluster loan-extractor-cluster \
  --service-name api \
  --task-definition loan-extractor-api \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:<account-id>:targetgroup/loan-extractor-api-tg,containerName=api,containerPort=8000"
```

Repeat for Dashboard and Worker services.

## Step 12: Configure Auto Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/loan-extractor-cluster/api \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/loan-extractor-cluster/api \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

## Step 13: Configure CloudWatch Alarms

```bash
# Create alarm for high CPU usage
aws cloudwatch put-metric-alarm \
  --alarm-name loan-extractor-api-high-cpu \
  --alarm-description "Alert when API CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

## Step 14: Set Up CloudFront (Optional)

For improved performance and caching:

1. Create CloudFront distribution
2. Origin: ALB DNS name
3. Configure caching behaviors
4. Enable HTTPS with ACM certificate

## Step 15: Configure Route 53 (Optional)

1. Create hosted zone for your domain
2. Create A record pointing to ALB or CloudFront distribution
3. Configure health checks

## Monitoring and Maintenance

### View Logs

```bash
# View API logs
aws logs tail /ecs/loan-extractor-api --follow

# View specific task logs
aws ecs describe-tasks --cluster loan-extractor-cluster --tasks <task-id>
```

### Update Services

```bash
# Build and push new image
docker build -t loan-extractor/api:v2 --target api .
docker tag loan-extractor/api:v2 $ECR_REGISTRY/loan-extractor/api:v2
docker push $ECR_REGISTRY/loan-extractor/api:v2

# Update task definition with new image
# Register new task definition revision

# Update service
aws ecs update-service \
  --cluster loan-extractor-cluster \
  --service api \
  --task-definition loan-extractor-api:2 \
  --force-new-deployment
```

## Cost Optimization

1. Use Fargate Spot for worker tasks
2. Enable S3 Intelligent-Tiering
3. Use RDS Reserved Instances for production
4. Configure CloudWatch log retention policies
5. Use ElastiCache reserved nodes

## Security Best Practices

1. Enable VPC Flow Logs
2. Use AWS WAF with ALB
3. Enable GuardDuty for threat detection
4. Implement least privilege IAM policies
5. Enable encryption at rest for all services
6. Use AWS Systems Manager Session Manager instead of SSH
7. Regularly rotate secrets in Secrets Manager
8. Enable MFA for AWS console access

## Troubleshooting

### Service Won't Start

1. Check CloudWatch logs for errors
2. Verify security group rules
3. Ensure secrets are accessible
4. Check task definition configuration

### Database Connection Issues

1. Verify RDS security group allows ECS security group
2. Check database credentials in Secrets Manager
3. Ensure RDS is in same VPC as ECS tasks

### High Costs

1. Review CloudWatch metrics for over-provisioning
2. Check S3 storage usage and lifecycle policies
3. Review ECS task sizes and scaling policies
4. Enable Cost Explorer and set up budgets

## Backup and Disaster Recovery

1. Enable automated RDS backups (7-30 day retention)
2. Configure S3 versioning and cross-region replication
3. Export task definitions and infrastructure as code
4. Document recovery procedures
5. Test disaster recovery plan regularly
