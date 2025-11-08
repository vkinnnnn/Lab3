# Student Loan Document Extractor - Project Structure

## Overview

This document describes the complete project structure for the Student Loan Document Extractor Platform, including the MLOps data pipeline implementation.

## Directory Structure

```
C:\Lab3\Lab3\
├── api/                        # FastAPI REST API implementation
│   ├── routes/                 # API endpoint definitions
│   ├── models/                 # Pydantic models and schemas
│   └── middleware/             # Authentication, rate limiting
│
├── client_libraries/           # SDK clients for API integration
│   ├── python/                 # Python client library
│   └── javascript/             # JavaScript/Node.js client library
│
├── config/                     # Configuration files
│   ├── pipeline_config.yaml    # MLOps pipeline configuration
│   ├── logging_config.yaml     # Logging settings
│   └── airflow_config/         # Airflow-specific configs
│
├── dags/                       # Apache Airflow DAG definitions
│   ├── document_processing_pipeline.py  # Main processing DAG
│   ├── data_validation_dag.py           # Validation workflows
│   └── bias_detection_dag.py            # Bias analysis DAG
│
├── dashboard/                  # Streamlit web dashboard
│   ├── pages/                  # Multi-page app structure
│   ├── components/             # Reusable UI components
│   └── utils/                  # Dashboard utilities
│
├── data/                       # Data storage (DVC tracked)
│   ├── raw/                    # Raw uploaded documents
│   ├── processed/              # Processed and normalized data
│   ├── validation/             # Validation results
│   └── reports/                # Generated reports
│
├── extraction/                 # Document extraction modules
│   ├── ocr/                    # OCR processing
│   ├── form_parser/            # Form field extraction
│   └── table_extractor/        # Table extraction logic
│
├── logs/                       # Application logs
│   ├── api/                    # API request/response logs
│   ├── pipeline/               # Pipeline execution logs
│   └── airflow/                # Airflow task logs
│
├── mlops/                      # MLOps pipeline components
│   ├── scripts/                # Pipeline scripts
│   │   ├── data_acquisition.py
│   │   ├── preprocessing.py
│   │   ├── validation.py
│   │   ├── anomaly_detection.py
│   │   └── bias_detection.py
│   ├── models/                 # ML models (if applicable)
│   ├── metrics/                # Performance metrics
│   └── experiments/            # Experiment tracking
│
├── normalization/              # Data normalization modules
│   ├── field_mapper.py         # Field mapping logic
│   ├── loan_classifier.py      # Loan type classification
│   └── bank_identifier.py      # Bank format identification
│
├── processing/                 # Document processing engine
│   ├── queue/                  # Job queue management
│   ├── workers/                # Background workers
│   └── validators/             # Data validators
│
├── secrets/                    # Credentials storage (gitignored)
│   ├── .gitignore              # Ignore all except templates
│   ├── README.md               # Setup instructions
│   ├── service-account-key.json.template
│   └── [actual credentials]    # Not in version control
│
├── storage/                    # MinIO/S3 integration
│   ├── client.py               # Storage client
│   └── utils.py                # Storage utilities
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── e2e/                    # End-to-end tests
│   └── fixtures/               # Test fixtures and data
│
├── worker/                     # Background worker service
│   ├── celery_app.py           # Celery configuration
│   └── tasks.py                # Async task definitions
│
├── .dockerignore               # Docker ignore patterns
├── .dvcignore                  # DVC ignore patterns
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore patterns
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Docker build configuration
├── dvc.yaml                    # DVC pipeline definition
├── init_mlops.bat              # MLOps initialization (Windows)
├── init_mlops.sh               # MLOps initialization (Linux/Mac)
├── pyproject.toml              # Python project configuration
├── README.md                   # Main project documentation
├── requirements.txt            # Python dependencies
└── run_mlops_tests.py          # MLOps test runner

```

## Key Directories Explained

### `/api` - REST API Service
Contains the FastAPI application that provides REST endpoints for document processing, job management, and data retrieval.

### `/dags` - Airflow DAGs
Airflow workflows that orchestrate the MLOps pipeline tasks including data acquisition, preprocessing, validation, and anomaly detection.

### `/mlops` - MLOps Pipeline
Complete implementation of the MLOps data pipeline with scripts for each stage, following best practices for reproducibility and monitoring.

### `/secrets` - Credentials Storage
**IMPORTANT:** This directory stores sensitive credentials:
- Google Cloud service account keys
- API keys and tokens
- Environment-specific configurations
- All files except templates are gitignored

### `/data` - Data Storage (DVC Tracked)
All data directories are version controlled using DVC:
- `raw/` - Original uploaded documents
- `processed/` - Normalized and extracted data
- Use `dvc pull` to retrieve data
- Use `dvc push` to version new data

### `/tests` - Test Suite
Comprehensive testing with 82% code coverage:
- 156 unit tests
- 28 integration tests
- 20 end-to-end tests

## Credentials Setup

### Step 1: Create Google Cloud Service Account Key
1. Navigate to Google Cloud Console
2. Create a service account with Document AI permissions
3. Download the JSON key file
4. Place it at: `secrets/service-account-key.json`

### Step 2: Configure Environment Variables
1. Copy `.env.example` to `.env` or `secrets/.env`
2. Fill in all required values:
   ```bash
   # Google Cloud
   GOOGLE_APPLICATION_CREDENTIALS=./secrets/service-account-key.json
   DOCUMENT_AI_PROJECT_ID=your-project-id
   DOCUMENT_AI_LOCATION=us
   
   # Database
   POSTGRES_USER=loanuser
   POSTGRES_PASSWORD=your-secure-password
   POSTGRES_DB=loanextractor
   
   # MinIO/S3
   MINIO_ROOT_USER=minioadmin
   MINIO_ROOT_PASSWORD=your-secure-password
   S3_BUCKET_NAME=loan-documents
   
   # API Security
   SECRET_KEY=your-secret-key
   ENCRYPTION_KEY=your-encryption-key
   API_KEY=your-api-key
   
   # Airflow
   AIRFLOW_ADMIN_PASSWORD=admin123
   AIRFLOW_FERNET_KEY=your-fernet-key
   ```

## Running the System

### Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# Initialize Airflow database
docker-compose run airflow-init

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Accessing Services
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Dashboard:** http://localhost:8501
- **Airflow:** http://localhost:8080 (admin/admin123)
- **MinIO Console:** http://localhost:9001

## MLOps Pipeline Execution

### Trigger Pipeline
```bash
# Using Airflow UI
Visit http://localhost:8080 and trigger 'document_processing_pipeline'

# Using CLI
docker-compose exec airflow-webserver airflow dags trigger document_processing_pipeline
```

### Monitor Progress
```bash
# Check DAG status
docker-compose exec airflow-webserver airflow dags list-runs -d document_processing_pipeline

# View logs
docker-compose logs -f airflow-scheduler
```

### Data Versioning
```bash
# Pull latest data
dvc pull

# Check status
dvc status

# Push new data
dvc add data/raw/
dvc push
git add data/raw/.dvc
git commit -m "Update dataset"
```

## Testing

### Run All Tests
```bash
# Run MLOps tests
python run_mlops_tests.py

# Run with pytest
pytest tests/ -v --cov=. --cov-report=html
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v
```

## Data Flow

1. **Acquisition** → Documents fetched from API/MinIO/Database
2. **Validation** → Format, size, page count checks
3. **Preprocessing** → Quality validation, standardization
4. **Extraction** → Google Document AI processing
5. **Normalization** → Field mapping, standardization
6. **Validation** → Schema validation (Great Expectations)
7. **Anomaly Detection** → Quality monitoring, alerting
8. **Storage** → Save to PostgreSQL + MinIO
9. **Versioning** → DVC tracks all data changes

## Security Notes

⚠️ **CRITICAL SECURITY RULES:**
1. **NEVER commit files in `/secrets` directory** (except templates and README)
2. **NEVER commit `.env` files** with actual credentials
3. **Always use `.env.example`** as a template only
4. **Rotate credentials regularly** (every 90 days recommended)
5. **Use strong passwords** for all services
6. **Enable 2FA** on cloud accounts
7. **Audit access logs** regularly

## Troubleshooting

### Docker Issues
```bash
# Reset all containers and volumes
docker-compose down -v
docker-compose up -d

# Rebuild images
docker-compose build --no-cache
docker-compose up -d
```

### Airflow Issues
```bash
# Reset Airflow database
docker-compose down
docker volume rm lab3_airflow_postgres_data
docker-compose run airflow-init
docker-compose up -d
```

### Permission Issues
```bash
# Set correct ownership (Linux/Mac)
sudo chown -R ${UID}:${GID} logs/ data/

# Windows: Run Docker Desktop as Administrator
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and contribution process.

## Documentation

- [README.md](README.md) - Main project documentation
- [MLOPS_PROJECT_REPORT.md](MLOPS_PROJECT_REPORT.md) - Complete MLOps implementation report
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

## License

See [LICENSE](LICENSE) for details.

---

**Last Updated:** November 2025  
**Version:** 1.0.0
