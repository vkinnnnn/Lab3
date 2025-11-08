# Design Document

## Overview

The Student Loan Document Extractor Platform is a document processing system that extracts structured financial and legal information from diverse loan documents using OCR, layout analysis, and table extraction technologies. The platform normalizes data from various bank formats and loan types into a standardized JSON schema, enabling comparison and analysis.

### Key Design Principles

1. **Modular Architecture**: Separate concerns for document ingestion, OCR processing, data extraction, normalization, and storage
2. **Format Agnostic**: Handle multiple input formats (PDF, JPEG, PNG, TIFF) and diverse bank-specific layouts
3. **Accuracy First**: Prioritize extraction accuracy through multi-stage validation and confidence scoring
4. **Scalability**: Support batch processing and concurrent document handling
5. **Extensibility**: Easy addition of new loan types and bank-specific extractors

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Web Dashboard │
│   (Streamlit)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                    REST API Layer                        │
│              (FastAPI / Flask)                           │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              Document Processing Pipeline                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │ Ingestion│→ │   OCR    │→ │Extraction│→ │  Output │││
│  │          │  │          │  │          │  │         │││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                          │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │   PostgreSQL     │      │   S3/MinIO       │        │
│  │   (Metadata)     │      │   (Documents)    │        │
│  └──────────────────┘      └──────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Component Architecture

```
Document Processing Pipeline:

1. Document Ingestion
   ├── Format Validator
   ├── File Type Detector
   └── Document Preprocessor

2. OCR & Layout Analysis
   ├── Image Preprocessor
   ├── OCR Engine (Tesseract/Donut/LayoutLMv3)
   ├── Layout Analyzer (LayoutParser)
   └── Table Detector (Camelot/Tabula)

3. Data Extraction
   ├── Field Extractor
   ├── Table Extractor
   ├── Entity Recognizer (NER)
   └── Confidence Scorer

4. Data Normalization
   ├── Loan Type Classifier
   ├── Bank Format Identifier
   ├── Field Mapper
   └── Schema Validator (Pydantic)

5. Output Generation
   ├── JSON Generator
   ├── Comparison Calculator
   └── Storage Manager
```

## Components and Interfaces

### 1. Document Ingestion Module

**Purpose**: Accept, validate, and prepare documents for processing

**Components**:
- `DocumentUploader`: Handles file uploads via API or web interface
- `FormatValidator`: Validates file format (PDF, JPEG, PNG, TIFF)
- `DocumentPreprocessor`: Converts images to optimal format for OCR

**Interfaces**:
```python
class DocumentIngestionService:
    def upload_document(self, file: UploadFile) -> DocumentMetadata
    def validate_format(self, file_path: str) -> bool
    def preprocess_document(self, file_path: str) -> ProcessedDocument
```

### 2. OCR and Layout Analysis Module

**Purpose**: Extract text and identify document structure

**Components**:
- `OCREngine`: Wrapper for Tesseract, Donut, or LayoutLMv3
- `LayoutAnalyzer`: Identifies document regions (text blocks, tables, headers)
- `TableDetector`: Detects and extracts table structures
- `HandwritingRecognizer`: Specialized handler for handwritten content

**Interfaces**:
```python
class OCRService:
    def extract_text(self, document: ProcessedDocument) -> ExtractedText
    def analyze_layout(self, document: ProcessedDocument) -> LayoutStructure
    def detect_tables(self, document: ProcessedDocument) -> List[TableRegion]
    def extract_table_data(self, table_region: TableRegion) -> TableData
```

### 3. Data Extraction Module

**Purpose**: Extract specific loan fields from OCR output

**Components**:
- `FieldExtractor`: Extracts key-value pairs (principal, interest rate, tenure)
- `TableExtractor`: Processes payment schedules and fee structures
- `EntityRecognizer`: NER for identifying entities (bank names, borrower names)
- `ConfidenceScorer`: Assigns confidence scores to extracted data

**Interfaces**:
```python
class DataExtractionService:
    def extract_loan_fields(self, text: ExtractedText, layout: LayoutStructure) -> LoanFields
    def extract_payment_schedule(self, table: TableData) -> PaymentSchedule
    def extract_fee_structure(self, table: TableData) -> FeeStructure
    def calculate_confidence(self, field: ExtractedField) -> float
```

### 4. Data Normalization Module

**Purpose**: Normalize extracted data to standard schema

**Components**:
- `LoanTypeClassifier`: Identifies loan type (education, home, personal, etc.)
- `BankFormatIdentifier`: Identifies lending institution
- `FieldMapper`: Maps bank-specific field names to standard schema
- `SchemaValidator`: Validates against Pydantic models

**Interfaces**:
```python
class DataNormalizationService:
    def classify_loan_type(self, fields: LoanFields) -> LoanType
    def identify_bank(self, text: ExtractedText) -> BankInfo
    def normalize_fields(self, fields: LoanFields, bank: BankInfo) -> NormalizedLoanData
    def validate_schema(self, data: NormalizedLoanData) -> ValidationResult
```

### 5. Comparison and Analysis Module

**Purpose**: Calculate metrics and enable loan comparison

**Components**:
- `MetricsCalculator`: Calculates total cost, effective rate, flexibility score
- `ComparisonEngine`: Generates side-by-side comparisons
- `RankingService`: Ranks loans by various criteria

**Interfaces**:
```python
class ComparisonService:
    def calculate_metrics(self, loan_data: NormalizedLoanData) -> ComparisonMetrics
    def compare_loans(self, loans: List[NormalizedLoanData]) -> ComparisonResult
    def rank_by_cost(self, loans: List[NormalizedLoanData]) -> List[RankedLoan]
    def rank_by_flexibility(self, loans: List[NormalizedLoanData]) -> List[RankedLoan]
```

### 6. Storage Module

**Purpose**: Persist documents and extracted data

**Components**:
- `DocumentStore`: S3/MinIO for raw documents
- `MetadataStore`: PostgreSQL for structured data
- `CacheManager`: Redis for temporary processing state

**Interfaces**:
```python
class StorageService:
    def store_document(self, file: bytes, metadata: DocumentMetadata) -> str
    def store_extracted_data(self, data: NormalizedLoanData) -> UUID
    def retrieve_document(self, document_id: str) -> bytes
    def query_loans(self, filters: QueryFilters) -> List[NormalizedLoanData]
```

### 7. API Layer

**Purpose**: Expose platform functionality via REST API

**Endpoints**:
- `POST /api/v1/documents/upload` - Upload single document
- `POST /api/v1/documents/batch-upload` - Upload multiple documents
- `GET /api/v1/documents/{id}` - Retrieve document metadata
- `GET /api/v1/documents/{id}/extracted-data` - Get extracted loan data
- `POST /api/v1/compare` - Compare multiple loans
- `GET /api/v1/loans` - Query loans with filters
- `GET /api/v1/processing-status/{job_id}` - Check processing status

### 8. Web Dashboard

**Purpose**: User interface for document upload and visualization

**Features**:
- Document upload interface (drag-and-drop)
- Processing status display
- Extracted data viewer
- Loan comparison table
- Search and filter functionality
- Mobile-responsive design

## Data Models

### Core Data Structures

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date
from enum import Enum

class LoanType(str, Enum):
    EDUCATION = "education"
    HOME = "home"
    PERSONAL = "personal"
    VEHICLE = "vehicle"
    GOLD = "gold"
    OTHER = "other"

class DocumentMetadata(BaseModel):
    document_id: str
    file_name: str
    file_type: str  # pdf, jpeg, png, tiff
    upload_timestamp: date
    file_size_bytes: int
    page_count: int
    storage_path: str

class BankInfo(BaseModel):
    bank_name: str
    branch_name: Optional[str]
    bank_code: Optional[str]

class CoSignerDetails(BaseModel):
    name: str
    relationship: str
    contact: Optional[str]

class FeeItem(BaseModel):
    fee_type: str  # processing, administrative, documentation
    amount: float
    currency: str = "INR"
    conditions: Optional[str]

class PaymentScheduleEntry(BaseModel):
    payment_number: int
    payment_date: date
    total_amount: float
    principal_component: float
    interest_component: float
    outstanding_balance: float

class TableData(BaseModel):
    table_id: str
    headers: List[str]
    rows: List[List[str]]
    nested_columns: Optional[Dict[str, List[str]]]
    table_type: str  # payment_schedule, fee_structure, other

class NormalizedLoanData(BaseModel):
    loan_id: str
    document_id: str
    loan_type: LoanType
    bank_info: BankInfo
    
    # Core loan terms
    principal_amount: float
    currency: str = "INR"
    interest_rate: float  # Annual percentage
    tenure_months: int
    moratorium_period_months: Optional[int]
    
    # Fees and charges
    fees: List[FeeItem]
    processing_fee: Optional[float]
    late_payment_penalty: Optional[str]
    prepayment_penalty: Optional[str]
    
    # Repayment details
    repayment_mode: Optional[str]  # EMI, bullet, step-up
    payment_schedule: Optional[List[PaymentScheduleEntry]]
    
    # Additional details
    co_signer: Optional[CoSignerDetails]
    collateral_details: Optional[str]
    disbursement_terms: Optional[str]
    
    # Metadata
    extraction_confidence: float  # 0.0 to 1.0
    extraction_timestamp: date
    
class ComparisonMetrics(BaseModel):
    loan_id: str
    total_cost_estimate: float
    effective_interest_rate: float
    flexibility_score: float  # 0.0 to 10.0
    monthly_emi: Optional[float]
    total_interest_payable: float
    
class ComparisonResult(BaseModel):
    loans: List[NormalizedLoanData]
    metrics: List[ComparisonMetrics]
    best_by_cost: str  # loan_id
    best_by_flexibility: str  # loan_id
    comparison_notes: Dict[str, str]
```

### Database Schema

**PostgreSQL Tables**:

```sql
-- Documents table
CREATE TABLE documents (
    document_id UUID PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    upload_timestamp TIMESTAMP NOT NULL,
    file_size_bytes BIGINT,
    page_count INT,
    storage_path VARCHAR(500) NOT NULL,
    processing_status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Loans table
CREATE TABLE loans (
    loan_id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id),
    loan_type VARCHAR(50) NOT NULL,
    bank_name VARCHAR(255),
    principal_amount DECIMAL(15, 2),
    interest_rate DECIMAL(5, 2),
    tenure_months INT,
    extracted_data JSONB NOT NULL,
    extraction_confidence DECIMAL(3, 2),
    extraction_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comparison metrics table
CREATE TABLE comparison_metrics (
    metric_id UUID PRIMARY KEY,
    loan_id UUID REFERENCES loans(loan_id),
    total_cost_estimate DECIMAL(15, 2),
    effective_interest_rate DECIMAL(5, 2),
    flexibility_score DECIMAL(3, 1),
    monthly_emi DECIMAL(15, 2),
    total_interest_payable DECIMAL(15, 2),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Processing jobs table (for batch processing)
CREATE TABLE processing_jobs (
    job_id UUID PRIMARY KEY,
    status VARCHAR(50) DEFAULT 'queued',
    total_documents INT,
    processed_documents INT DEFAULT 0,
    failed_documents INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_loans_document_id ON loans(document_id);
CREATE INDEX idx_loans_loan_type ON loans(loan_type);
CREATE INDEX idx_loans_bank_name ON loans(bank_name);
CREATE INDEX idx_documents_status ON documents(processing_status);
```

## Error Handling

### Error Categories

1. **Input Validation Errors**
   - Invalid file format
   - File size exceeds limit
   - Corrupted file

2. **Processing Errors**
   - OCR failure
   - Table detection failure
   - Low confidence extraction

3. **Data Validation Errors**
   - Missing required fields
   - Invalid data types
   - Schema validation failure

4. **System Errors**
   - Storage failure
   - Database connection error
   - External service timeout

### Error Handling Strategy

```python
class ProcessingError(Exception):
    def __init__(self, error_type: str, message: str, document_id: str):
        self.error_type = error_type
        self.message = message
        self.document_id = document_id
        self.timestamp = datetime.now()

class ErrorHandler:
    def handle_error(self, error: ProcessingError) -> ErrorResponse:
        # Log error
        logger.error(f"{error.error_type}: {error.message} for document {error.document_id}")
        
        # Update document status
        self.update_document_status(error.document_id, "failed")
        
        # Store error details
        self.store_error_log(error)
        
        # Return user-friendly error response
        return ErrorResponse(
            success=False,
            error_type=error.error_type,
            message=self.get_user_message(error),
            document_id=error.document_id
        )
```

### Retry Logic

- OCR failures: Retry up to 3 times with different preprocessing
- Table extraction failures: Fall back to text-based extraction
- Storage failures: Retry with exponential backoff
- Low confidence extractions: Flag for manual review

## Testing Strategy

### Unit Testing

**Components to Test**:
- Document format validation
- OCR text extraction accuracy
- Table detection and extraction
- Field extraction logic
- Data normalization
- Schema validation
- Metrics calculation

**Test Data**:
- Sample documents from each loan type
- Documents from different banks
- Edge cases (handwritten, poor quality scans, multi-page tables)

### Integration Testing

**Scenarios**:
- End-to-end document processing pipeline
- API endpoint functionality
- Database operations
- Storage operations
- Batch processing workflow

### Performance Testing

**Metrics**:
- Processing time per document (target: <15s for ≤10 pages)
- Throughput (documents per minute)
- API response times
- Database query performance
- Memory usage during processing

### Accuracy Testing

**Validation**:
- Ground truth comparison for extraction accuracy (target: F1 ≥ 94%)
- Manual review of sample extractions
- Confidence score calibration
- Cross-validation with multiple OCR engines

## Deployment Architecture

### Containerization

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/loanextractor
      - S3_ENDPOINT=http://minio:9000
    depends_on:
      - db
      - minio
      - redis
  
  dashboard:
    build: ./dashboard
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
  
  worker:
    build: ./worker
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/loanextractor
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=loanextractor
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio_data:/data
  
  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  minio_data:
```

### Cloud Deployment (AWS)

**Services**:
- **EC2/ECS**: Host API and worker containers
- **RDS PostgreSQL**: Managed database
- **S3**: Document storage
- **ElastiCache Redis**: Caching and job queue
- **CloudFront**: CDN for dashboard
- **ALB**: Load balancing for API
- **CloudWatch**: Monitoring and logging

### Scaling Strategy

**Horizontal Scaling**:
- Multiple API instances behind load balancer
- Worker pool for parallel document processing
- Database read replicas for query performance

**Vertical Scaling**:
- Increase worker memory for large documents
- GPU instances for deep learning OCR models

## Security Considerations

### Data Protection

1. **Encryption at Rest**: AES-256 for stored documents
2. **Encryption in Transit**: TLS 1.3 for all API communications
3. **Access Control**: JWT-based authentication, RBAC for user permissions
4. **Data Retention**: Configurable retention policies, secure deletion

### Compliance

- **GDPR**: Right to erasure, data portability, consent management
- **COPPA**: Parental consent for users under 13, data minimization
- **PCI DSS**: If handling payment information, tokenization of sensitive data

### Security Best Practices

- Input sanitization to prevent injection attacks
- Rate limiting on API endpoints
- Audit logging for all data access
- Regular security scanning of dependencies
- Secrets management using environment variables or vault services

## Monitoring and Observability

### Metrics to Track

**System Metrics**:
- CPU and memory usage
- API response times
- Database query performance
- Storage usage

**Business Metrics**:
- Documents processed per day
- Average processing time
- Extraction accuracy rates
- User engagement (uploads, comparisons)

**Error Metrics**:
- Error rates by type
- Failed document processing
- Low confidence extractions

### Logging Strategy

```python
import logging
import structlog

# Structured logging configuration
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Usage
logger.info("document_processed", 
            document_id=doc_id, 
            processing_time=elapsed_time,
            confidence=confidence_score)
```

### Alerting

- Processing time exceeds threshold
- Error rate spikes
- Storage capacity warnings
- Database connection failures

## Future Enhancements

1. **Machine Learning Improvements**
   - Fine-tune OCR models on loan document corpus
   - Train custom NER model for loan-specific entities
   - Implement active learning for continuous improvement

2. **Advanced Features**
   - Multi-language support for international loans
   - Automated anomaly detection in loan terms
   - Predictive analytics for loan affordability

3. **Integration Capabilities**
   - Webhook notifications for processing completion
   - Integration with financial planning tools
   - Export to Excel/CSV for offline analysis

4. **User Experience**
   - Real-time processing progress updates
   - Interactive data correction interface
   - Mobile app for document capture and upload
