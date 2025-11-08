# Project Cleanup and Restructure Plan

**Date**: November 6, 2025  
**Purpose**: Restructure Student Loan Document Extractor Platform for clarity and maintainability

---

## Current Issues

1. **Duplicate Documentation** - 40+ markdown files with overlapping content
2. **Redundant Directories** - Multiple unused folders (Lab3/, frontend/, LoanQA-Integration/)
3. **Unclear Structure** - Core modules mixed with examples and documentation
4. **Inconsistent Naming** - Multiple README files, duplicate guides

---

## Restructuring Strategy

### Phase 1: Identify Core vs Non-Core

**Core Components (KEEP)**:
- `api/` - FastAPI backend
- `dashboard/` - Streamlit UI
- `processing/` - Document extraction
- `normalization/` - Data normalization
- `storage/` - Storage services
- `tests/` - Test suite
- `mlops/` - MLOps pipeline
- `dags/` - Airflow DAGs
- `config/` - Configuration files

**Non-Core (REMOVE/ARCHIVE)**:
- `Lab3/` - Duplicate of root project
- `frontend/` - Unused Next.js frontend
- `LoanQA-Integration/` - External project integration
- `Lib/`, `Scripts/` - Python virtual env artifacts
- `extraction/`, `ocr/` - Redundant with processing/
- `temp/`, `uploads/`, `output/` - Runtime directories

### Phase 2: Documentation Consolidation

**Keep Only**:
- `README.md` - Main project documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `DEPLOYMENT.md` - Deployment guide
- `LICENSE` - License file
- `CHANGELOG.md` - Version history (NEW)
- `docs/` directory with organized documentation

**Archive/Remove**:
- All `*_COMPLETE.md`, `*_SUMMARY.md`, `*_STATUS.md` files
- Duplicate guides and implementation notes
- Old research documents

### Phase 3: Code Organization

**New Structure**:
```
student-loan-extractor/
├── src/                          # Source code
│   ├── api/                      # FastAPI application
│   ├── dashboard/                # Streamlit UI
│   ├── processing/               # Document processing
│   ├── normalization/            # Data normalization
│   ├── storage/                  # Storage layer
│   ├── mlops/                    # MLOps components
│   └── utils/                    # Shared utilities
├── tests/                        # Test suite
├── dags/                         # Airflow DAGs
├── config/                       # Configuration
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   ├── deployment/               # Deployment guides
│   ├── architecture/             # Architecture docs
│   └── user-guide/               # User guides
├── data/                         # Data directories
│   ├── raw/                      # Raw documents
│   └── processed/                # Processed data
├── docker/                       # Docker files
│   ├── api/
│   ├── dashboard/
│   └── worker/
├── .kiro/                        # Kiro specs
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
├── DEPLOYMENT.md
├── LICENSE
└── CHANGELOG.md
```

---

## Execution Plan

1. ✅ Create new directory structure
2. ✅ Move core modules to `src/`
3. ✅ Consolidate documentation to `docs/`
4. ✅ Remove redundant files and directories
5. ✅ Update all import paths
6. ✅ Update Docker configurations
7. ✅ Run tests to verify functionality
8. ✅ Create comprehensive project report
9. ✅ Update README with new structure

---

## Files to Keep

### Core Application
- `api/` → `src/api/`
- `dashboard/` → `src/dashboard/`
- `processing/` → `src/processing/`
- `normalization/` → `src/normalization/`
- `storage/` → `src/storage/`
- `mlops/` → `src/mlops/`

### Configuration
- `config/` → Keep
- `dags/` → Keep
- `.env.example` → Keep
- `docker-compose.yml` → Keep
- `requirements.txt` → Keep
- `pyproject.toml` → Keep

### Documentation
- `README.md` → Update
- `CONTRIBUTING.md` → Keep
- `DEPLOYMENT.md` → Move to `docs/deployment/`
- `LICENSE` → Keep

### Testing
- `tests/` → Keep all test files
- `test_end_to_end_integration.py` → Move to `tests/`

---

## Files to Remove/Archive

### Duplicate Directories
- `Lab3/` - Complete duplicate
- `frontend/` - Unused Next.js app
- `LoanQA-Integration/` - External project
- `Lib/`, `Scripts/` - Virtual env artifacts
- `extraction/`, `ocr/` - Redundant modules

### Documentation to Archive
- All `*_COMPLETE.md` files
- All `*_SUMMARY.md` files
- All `*_STATUS.md` files
- All `*_IMPLEMENTATION.md` files
- Duplicate guides (QUICKSTART vs QUICK_START)

### Temporary/Generated
- `__pycache__/` directories
- `.pytest_cache/`
- `temp/`
- `uploads/` (keep .gitkeep)
- `output/` (keep .gitkeep)
- `test_files/` (move to tests/fixtures/)

---

## Next Steps

1. Execute cleanup script
2. Update all import paths
3. Run full test suite
4. Create comprehensive project report
5. Update README with new structure
6. Commit changes

