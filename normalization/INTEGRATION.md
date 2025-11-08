# Normalization Module Integration Guide

This guide explains how the normalization module integrates with other components of the Student Loan Document Extractor Platform.

## Architecture Overview

```
┌─────────────────┐
│   Extraction    │
│     Module      │
└────────┬────────┘
         │ Raw extracted data
         ▼
┌─────────────────┐
│  Normalization  │
│     Module      │
│  ┌───────────┐  │
│  │Field      │  │
│  │Mapper     │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │Schema     │  │
│  │Validator  │  │
│  └───────────┘  │
└────────┬────────┘
         │ Validated NormalizedLoanData
         ▼
┌─────────────────┐
│    Storage      │
│     Module      │
└─────────────────┘
```

## Integration Points

### 1. With Extraction Module

The normalization module receives raw extracted data from the extraction module.

**Extraction Module Output Format:**

```python
{
    'loan_type': 'education',
    'bank_name': 'State Bank of India',
    'branch_name': 'Mumbai Central',
    'principal_amount': '₹5,00,000',
    'interest_rate': '8.5%',
    'tenure': '5 years',
    'moratorium_period': '6 months',
    'processing_fee': '₹5,000',
    'fees': [...],
    'payment_schedule': [...],
    'confidence': 0.95,
    # ... other extracted fields
}
```

**Integration Code:**

```python
from extraction import ExtractionService
from normalization import NormalizationService

# Initialize services
extraction_service = ExtractionService()
normalization_service = NormalizationService()

# Extract data from document
extracted_data = extraction_service.extract_from_document(document_path)

# Normalize extracted data
result = normalization_service.normalize(
    extracted_data=extracted_data,
    document_id=document_id
)

if result.is_valid:
    normalized_loan = result.validated_data
    # Proceed to storage
else:
    # Handle validation errors
    log_errors(result.errors)
```

### 2. With Storage Module

The normalization module outputs validated `NormalizedLoanData` objects that can be stored.

**Storage Integration:**

```python
from normalization import normalize_loan_data
from storage import StorageService

# Normalize data
result = normalize_loan_data(extracted_data, document_id)

if result.is_valid:
    # Store in database
    storage = StorageService()
    
    # Convert to dictionary for storage
    loan_dict = result.validated_data.model_dump()
    
    # Store in PostgreSQL
    storage.store_loan_data(loan_dict)
    
    # Store as JSON in S3
    json_data = result.validated_data.model_dump_json()
    storage.store_json(document_id, json_data)
```

### 3. With API Layer

The normalization module can be used in API endpoints to validate incoming data.

**API Integration:**

```python
from fastapi import APIRouter, HTTPException
from normalization import NormalizationService, NormalizedLoanData

router = APIRouter()
normalization_service = NormalizationService()

@router.post("/api/v1/loans/normalize")
async def normalize_loan(extracted_data: dict, document_id: str):
    """Normalize extracted loan data."""
    
    result = normalization_service.normalize(
        extracted_data=extracted_data,
        document_id=document_id
    )
    
    if not result.is_valid:
        raise HTTPException(
            status_code=422,
            detail={
                'errors': [
                    {
                        'field': err.field,
                        'type': err.error_type,
                        'message': err.message
                    }
                    for err in result.errors
                ],
                'warnings': result.warnings
            }
        )
    
    return {
        'loan_id': result.validated_data.loan_id,
        'data': result.validated_data.model_dump(),
        'warnings': result.warnings
    }

@router.get("/api/v1/loans/{loan_id}", response_model=NormalizedLoanData)
async def get_loan(loan_id: str):
    """Get normalized loan data."""
    # Retrieve from storage and return as NormalizedLoanData
    loan_data = storage.get_loan(loan_id)
    return NormalizedLoanData(**loan_data)
```

### 4. With Comparison Module

The normalization module provides the standardized data format needed for loan comparison.

**Comparison Integration:**

```python
from normalization import NormalizationService, ComparisonResult, ComparisonMetrics
from typing import List

class ComparisonService:
    def __init__(self):
        self.normalization_service = NormalizationService()
    
    def compare_loans(
        self,
        extracted_data_list: List[dict],
        document_ids: List[str]
    ) -> ComparisonResult:
        """Compare multiple loans."""
        
        # Normalize all loans
        results = self.normalization_service.normalize_batch(
            extracted_data_list,
            document_ids
        )
        
        # Filter valid loans
        valid_loans = [
            r.validated_data for r in results if r.is_valid
        ]
        
        if not valid_loans:
            raise ValueError("No valid loans to compare")
        
        # Calculate metrics for each loan
        metrics = [
            self._calculate_metrics(loan) for loan in valid_loans
        ]
        
        # Find best options
        best_by_cost = min(metrics, key=lambda m: m.total_cost_estimate).loan_id
        best_by_flexibility = max(metrics, key=lambda m: m.flexibility_score).loan_id
        
        return ComparisonResult(
            loans=valid_loans,
            metrics=metrics,
            best_by_cost=best_by_cost,
            best_by_flexibility=best_by_flexibility,
            comparison_notes=self._generate_notes(valid_loans, metrics)
        )
```

## Complete Pipeline Example

Here's a complete example showing the full pipeline from document upload to storage:

```python
from pathlib import Path
from api.document_ingestion import DocumentIngestionService
from ocr import OCRService
from extraction import ExtractionService
from normalization import NormalizationService
from storage import StorageService

class LoanDocumentPipeline:
    """Complete document processing pipeline."""
    
    def __init__(self):
        self.ingestion = DocumentIngestionService()
        self.ocr = OCRService()
        self.extraction = ExtractionService()
        self.normalization = NormalizationService()
        self.storage = StorageService()
    
    def process_document(self, file_path: Path) -> dict:
        """Process a loan document through the complete pipeline."""
        
        # Step 1: Ingest and preprocess document
        print("Step 1: Ingesting document...")
        doc_metadata = self.ingestion.upload_document(file_path)
        document_id = doc_metadata.document_id
        
        # Step 2: OCR and layout analysis
        print("Step 2: Performing OCR...")
        ocr_result = self.ocr.process_document(file_path)
        
        # Step 3: Extract loan fields
        print("Step 3: Extracting loan data...")
        extracted_data = self.extraction.extract_loan_data(ocr_result)
        
        # Step 4: Normalize and validate
        print("Step 4: Normalizing data...")
        norm_result = self.normalization.normalize(
            extracted_data=extracted_data,
            document_id=document_id
        )
        
        if not norm_result.is_valid:
            print(f"Validation failed with {len(norm_result.errors)} errors")
            return {
                'success': False,
                'document_id': document_id,
                'errors': [
                    {
                        'field': err.field,
                        'message': err.message
                    }
                    for err in norm_result.errors
                ]
            }
        
        # Step 5: Store normalized data
        print("Step 5: Storing data...")
        loan_data = norm_result.validated_data
        
        # Store in database
        self.storage.store_loan_data(loan_data.model_dump())
        
        # Store original document
        self.storage.store_document(file_path, document_id)
        
        print(f"✓ Processing complete! Loan ID: {loan_data.loan_id}")
        
        return {
            'success': True,
            'document_id': document_id,
            'loan_id': loan_data.loan_id,
            'loan_type': loan_data.loan_type.value,
            'principal': loan_data.principal_amount,
            'warnings': norm_result.warnings
        }

# Usage
pipeline = LoanDocumentPipeline()
result = pipeline.process_document(Path("sample-loan-docs/education-loan.pdf"))
```

## Error Handling Strategy

### Graceful Degradation

```python
def process_with_fallback(extracted_data: dict, document_id: str):
    """Process with fallback for validation failures."""
    
    service = NormalizationService(strict_validation=False)
    result = service.normalize(extracted_data, document_id)
    
    if result.is_valid:
        # Full success
        return {
            'status': 'success',
            'data': result.validated_data,
            'warnings': result.warnings
        }
    else:
        # Partial success - store raw data for manual review
        return {
            'status': 'needs_review',
            'raw_data': extracted_data,
            'errors': result.errors,
            'warnings': result.warnings
        }
```

### Retry with Relaxed Validation

```python
def normalize_with_retry(extracted_data: dict, document_id: str):
    """Try strict validation first, then relaxed."""
    
    # Try strict validation
    strict_service = NormalizationService(strict_validation=True)
    result = strict_service.normalize(extracted_data, document_id)
    
    if result.is_valid:
        return result
    
    # Retry with relaxed validation
    relaxed_service = NormalizationService(strict_validation=False)
    result = relaxed_service.normalize(extracted_data, document_id)
    
    if result.is_valid:
        # Log that we used relaxed validation
        logger.warning(f"Used relaxed validation for {document_id}")
    
    return result
```

## Data Flow Diagram

```
┌──────────────┐
│   Document   │
│   Upload     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│     OCR      │
│   Service    │
└──────┬───────┘
       │ Raw text + layout
       ▼
┌──────────────┐
│  Extraction  │
│   Service    │
└──────┬───────┘
       │ Extracted fields (raw format)
       │ {
       │   'principal': '₹5,00,000',
       │   'rate': '8.5%',
       │   'tenure': '5 years'
       │ }
       ▼
┌──────────────┐
│Field Mapper  │
│              │
└──────┬───────┘
       │ Normalized fields
       │ {
       │   'principal_amount': 500000.0,
       │   'interest_rate': 8.5,
       │   'tenure_months': 60
       │ }
       ▼
┌──────────────┐
│   Schema     │
│  Validator   │
└──────┬───────┘
       │ ValidationResult
       │ {
       │   'is_valid': True,
       │   'validated_data': NormalizedLoanData(...)
       │ }
       ▼
┌──────────────┐
│   Storage    │
│   Service    │
└──────────────┘
```

## Configuration

### Environment Variables

```python
# config.py
import os

NORMALIZATION_CONFIG = {
    'strict_validation': os.getenv('STRICT_VALIDATION', 'false').lower() == 'true',
    'default_currency': os.getenv('DEFAULT_CURRENCY', 'INR'),
    'max_principal': float(os.getenv('MAX_PRINCIPAL', '100000000')),
    'min_principal': float(os.getenv('MIN_PRINCIPAL', '1000')),
    'max_interest_rate': float(os.getenv('MAX_INTEREST_RATE', '50')),
    'max_tenure_months': int(os.getenv('MAX_TENURE_MONTHS', '360')),
}
```

### Using Configuration

```python
from config import NORMALIZATION_CONFIG
from normalization import NormalizationService

service = NormalizationService(
    strict_validation=NORMALIZATION_CONFIG['strict_validation']
)
```

## Testing Integration

```python
import pytest
from normalization import normalize_loan_data

def test_extraction_to_normalization():
    """Test integration between extraction and normalization."""
    
    # Simulate extraction output
    extracted_data = {
        'loan_type': 'education',
        'bank_name': 'Test Bank',
        'principal': '100000',
        'interest_rate': '8.5',
        'tenure': '48 months',
        'confidence': 0.95
    }
    
    # Normalize
    result = normalize_loan_data(extracted_data, 'test_doc_001')
    
    # Verify
    assert result.is_valid
    assert result.validated_data.principal_amount == 100000.0
    assert result.validated_data.interest_rate == 8.5
    assert result.validated_data.tenure_months == 48
```

## Best Practices

1. **Always validate before storage**: Never store unvalidated data
2. **Log warnings**: Even if validation passes, log warnings for review
3. **Handle missing optional fields**: Use None for missing optional fields
4. **Preserve raw data**: Keep raw extracted data for debugging
5. **Use batch processing**: For multiple documents, use batch methods
6. **Monitor confidence scores**: Flag low-confidence extractions
7. **Implement retry logic**: Retry with relaxed validation if strict fails

## Troubleshooting

### Common Issues

**Issue**: Validation fails with "Principal amount is required"
- **Cause**: Field mapper couldn't find principal in extracted data
- **Solution**: Check field name variations in extracted data

**Issue**: Date parsing fails
- **Cause**: Unsupported date format
- **Solution**: Add format to `_parse_date()` in field_mapper.py

**Issue**: Currency normalization incorrect
- **Cause**: Unrecognized currency symbol
- **Solution**: Add symbol to `CURRENCY_PATTERNS` in field_mapper.py

**Issue**: Payment schedule validation warnings
- **Cause**: Inconsistent schedule data
- **Solution**: Review extraction logic for payment schedules

## Support

For issues or questions about the normalization module:
1. Check the README.md for usage examples
2. Review example_usage.py for code samples
3. Check logs for detailed error messages
4. Review validation warnings for data quality issues
