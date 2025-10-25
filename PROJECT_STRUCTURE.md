# 📁 Project Structure

## Overview

Clean, organized structure for the Student Loan Document Extractor Platform.

## Directory Structure

```
Lab3/
├── 📁 api/                          # FastAPI backend service
│   ├── __init__.py
│   ├── main.py                      # API entry point
│   ├── routes.py                    # API endpoints
│   ├── models.py                    # Data models
│   ├── document_ingestion.py       # Document upload handling
│   ├── document_preprocessor.py    # Document preprocessing
│   ├── metadata_extractor.py       # Metadata extraction
│   ├── error_handlers.py           # Error handling
│   ├── cache_manager.py            # Caching logic
│   └── README.md                    # API documentation
│
├── 📁 dashboard/                    # Streamlit web interface
│   ├── components/                  # UI components
│   │   ├── __init__.py
│   │   ├── upload.py               # Upload interface
│   │   ├── data_viewer.py          # Data viewer
│   │   └── search.py               # Search functionality
│   ├── .streamlit/                 # Streamlit config
│   ├── __init__.py
│   └── app.py                      # Dashboard entry point
│
├── 📁 extraction/                   # Data extraction modules
│   ├── __init__.py
│   ├── extraction_service.py       # Main extraction service
│   ├── field_extractor.py          # Field extraction
│   ├── fee_extractor.py            # Fee extraction
│   ├── schedule_extractor.py       # Payment schedule extraction
│   ├── terms_extractor.py          # Terms extraction
│   ├── entity_extractor.py         # Entity recognition
│   ├── confidence_scorer.py        # Confidence scoring
│   └── README.md                    # Extraction documentation
│
├── 📁 normalization/                # Data normalization
│   ├── __init__.py
│   ├── normalization_service.py    # Main normalization service
│   ├── data_models.py              # Pydantic models
│   ├── field_mapper.py             # Field mapping
│   ├── schema_validator.py         # Schema validation
│   ├── loan_type_classifier.py     # Loan type classification
│   ├── bank_identifier.py          # Bank identification
│   ├── comparison_calculator.py    # Comparison metrics
│   ├── output_generator.py         # Output generation
│   ├── output_service.py           # Output service
│   └── README.md                    # Normalization documentation
│
├── 📁 ocr/                          # OCR and layout analysis
│   ├── __init__.py
│   ├── ocr_service.py              # Main OCR service
│   ├── ocr_engine.py               # OCR engine wrapper
│   ├── layout_analyzer.py          # Layout analysis
│   ├── table_extractor.py          # Table extraction
│   ├── multipage_processor.py      # Multi-page handling
│   ├── mixed_content_handler.py    # Mixed content handling
│   └── README.md                    # OCR documentation
│
├── 📁 processing/                   # Document processing
│   ├── __init__.py
│   ├── document_processor.py       # Main document processor
│   └── gemini_agent.py             # AI-powered extraction agent
│
├── 📁 security/                     # Security and privacy
│   ├── __init__.py
│   └── data_masking.py             # Data masking/anonymization
│
├── 📁 storage/                      # Data storage
│   ├── __init__.py
│   ├── storage_service.py          # Main storage service
│   ├── database.py                 # Database operations
│   ├── object_storage.py           # S3/MinIO operations
│   ├── security.py                 # Storage security
│   ├── setup_storage.py            # Storage setup
│   ├── init_db.sql                 # Database schema
│   └── README.md                    # Storage documentation
│
├── 📁 worker/                       # Background worker
│   ├── __init__.py
│   └── processor.py                # Worker processor
│
├── 📁 scripts/                      # Utility scripts
│   ├── init_db.sql                 # Database initialization
│   └── verify_setup.py             # Setup verification
│
├── 📁 temp/                         # Temporary files (gitignored)
├── 📁 uploads/                      # Uploaded files (gitignored)
│
├── 📄 Dockerfile                    # Multi-stage Docker build
├── 📄 docker-compose.yml            # Production compose
├── 📄 docker-compose.dev.yml        # Development compose
├── 📄 .dockerignore                 # Docker ignore rules
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 pyproject.toml               # Python project config
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
│
├── 📄 Makefile                     # Build automation
├── 📄 Makefile.docker              # Docker commands
├── 📄 setup.sh                     # Linux/Mac setup
├── 📄 setup.bat                    # Windows setup
│
├── 📚 README.md                    # Main documentation
├── 📚 AI_EXTRACTION_GUIDE.md       # AI features guide
├── 📚 DEPLOYMENT.md                # General deployment
├── 📚 DEPLOYMENT_AWS.md            # AWS deployment
├── 📚 DEPLOYMENT_GCP.md            # GCP deployment
├── 📚 DOCKER_README.md             # Docker reference
├── 📚 DOCKER_QUICKSTART.md         # Quick start guide
├── 📚 PRIVACY_SECURITY.md          # Privacy guide
├── 📚 DUAL_OUTPUT_GUIDE.md         # Dual output guide
├── 📚 PROJECT_STRUCTURE.md         # This file
├── 📚 CONTRIBUTING.md              # Contribution guide
└── 📚 LICENSE                      # License file
```

## Key Components

### 🔧 Core Services

**API Service** (`api/`)
- FastAPI-based REST API
- Document upload and processing
- Data retrieval endpoints
- Error handling and validation

**Dashboard** (`dashboard/`)
- Streamlit web interface
- Document upload UI
- Data visualization
- Comparison tools

**Worker** (`worker/`)
- Background processing
- Async document handling
- Job queue management

### 🤖 Processing Pipeline

**OCR** (`ocr/`)
- Tesseract integration
- Layout analysis
- Table extraction
- Multi-page support

**Extraction** (`extraction/`)
- Field extraction
- Entity recognition
- Confidence scoring
- Data validation

**Normalization** (`normalization/`)
- Data standardization
- Schema validation
- Type classification
- Comparison metrics

**AI Processing** (`processing/`)
- Gemini AI integration
- Intelligent extraction
- Web search enhancement
- Context analysis

### 🔒 Security & Privacy

**Security** (`security/`)
- Data masking
- Anonymization
- Privacy protection
- Compliance features

**Storage** (`storage/`)
- PostgreSQL integration
- S3/MinIO storage
- Encryption at rest
- Access control

## File Types

### Python Modules
- `*.py` - Python source files
- `__init__.py` - Package initialization
- `*_service.py` - Service modules
- `*_extractor.py` - Extraction modules

### Configuration
- `.env` - Environment variables (gitignored)
- `.env.example` - Environment template
- `config.py` - Application configuration
- `pyproject.toml` - Python project metadata

### Docker
- `Dockerfile` - Container build instructions
- `docker-compose.yml` - Service orchestration
- `.dockerignore` - Docker ignore rules

### Documentation
- `README.md` - Module documentation
- `*_GUIDE.md` - User guides
- `DEPLOYMENT*.md` - Deployment guides

### Scripts
- `setup.sh` - Linux/Mac setup
- `setup.bat` - Windows setup
- `Makefile*` - Build automation

## Important Directories

### Development
```
api/          - Backend API code
dashboard/    - Frontend UI code
processing/   - Document processing
```

### Data
```
storage/      - Database and storage
security/     - Privacy and security
```

### Infrastructure
```
scripts/      - Setup and utility scripts
temp/         - Temporary files (runtime)
uploads/      - Uploaded files (runtime)
```

## Excluded from Git

The following are gitignored:
- `temp/` - Temporary processing files
- `uploads/` - Uploaded documents
- `.env` - Environment variables
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python
- `*.log` - Log files

## Documentation Files

### User Guides
- `README.md` - Main project documentation
- `DOCKER_QUICKSTART.md` - Quick start guide
- `AI_EXTRACTION_GUIDE.md` - AI features
- `PRIVACY_SECURITY.md` - Privacy guide
- `DUAL_OUTPUT_GUIDE.md` - Output system

### Deployment
- `DEPLOYMENT.md` - General deployment
- `DEPLOYMENT_AWS.md` - AWS specific
- `DEPLOYMENT_GCP.md` - GCP specific
- `DOCKER_README.md` - Docker reference

### Development
- `CONTRIBUTING.md` - Contribution guidelines
- `PROJECT_STRUCTURE.md` - This file
- Module `README.md` files - Component docs

## Clean Structure

✅ **No test files in production**
✅ **No example files**
✅ **No redundant documentation**
✅ **No empty files**
✅ **Clear organization**
✅ **Logical grouping**

## Adding New Components

### New Extraction Module
```
extraction/
└── new_extractor.py
```

### New Dashboard Component
```
dashboard/components/
└── new_component.py
```

### New Documentation
```
Lab3/
└── NEW_FEATURE_GUIDE.md
```

## Maintenance

### Regular Cleanup
- Remove unused imports
- Delete obsolete files
- Update documentation
- Clean temp directories

### Code Organization
- Keep modules focused
- Use clear naming
- Document public APIs
- Follow Python conventions

---

**Clean, organized, production-ready structure!** 📁✨
