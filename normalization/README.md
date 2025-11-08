# Normalization Module

The normalization module provides data validation, field mapping, and schema standardization for extracted loan document data. It transforms raw extracted data into validated, standardized `NormalizedLoanData` objects.

## Features

- **Pydantic Data Models**: Type-safe data structures with automatic validation
- **Field Mapping**: Maps bank-specific field names to standardized schema
- **Data Type Normalization**: Handles currency symbols, percentages, dates, and various formats
- **Schema Validation**: Validates data against defined schemas with detailed error reporting
- **Business Rule Validation**: Applies domain-specific validation rules
- **Batch Processing**: Normalize multiple documents efficiently
- **Graceful Error Handling**: Provides detailed error messages and warnings

## Components

### Data Models (`data_models.py`)

Pydantic models defining the standardized data structures:

- `LoanType`: Enum for loan types (education, home, personal, vehicle, gold, other)
- `DocumentMetadata`: Document metadata (ID, filename, size, etc.)
- `BankInfo`: Lending institution information
- `CoSignerDetails`: Co-signer/guarantor information
- `FeeItem`: Individual fee or charge
- `PaymentScheduleEntry`: Single payment in schedule
- `TableData`: Structured table data
- `NormalizedLoanData`: Complete normalized loan data
- `ComparisonMetrics`: Calculated comparison metrics
- `ComparisonResult`: Multi-loan comparison result
- `ValidationError`: Validation error details
- `ValidationResult`: Validation result with errors/warnings

### Field Mapper (`field_mapper.py`)

Maps extracted fields to standardized schema:

- Handles multiple field name variations (e.g., "principal", "loan_amount", "principal_amount")
- Normalizes currency values (removes symbols, handles commas)
- Normalizes percentages (removes % symbol)
- Converts tenure to months (handles "years" and "months")
- Parses dates in multiple formats
- Handles missing optional fields gracefully

### Schema Validator (`schema_validator.py`)

Validates data against Pydantic schemas:

- Validates required fields
- Validates data types and ranges
- Applies business logic rules (reasonable amounts, rates, tenure)
- Validates payment schedule consistency
- Provides detailed error reporting
- Supports strict mode (warnings as errors)

### Normalization Service (`normalization_service.py`)

Orchestrates the normalization pipeline:

- Coordinates field mapping and validation
- Generates unique loan IDs
- Supports batch processing
- Provides convenience methods for common operations
- Returns structured validation results

## Usage

### Basic Normalization

```python
from normalization import normalize_loan_data

# Raw extracted data
extracted_data = {
    'loan_type': 'education',
    'bank_name': 'State Bank of India',
    'principal_amount': '₹5,00,000',
    'interest_rate': '8.5%',
    'tenure': '5 years',
    'confidence': 0.95
}

# Normalize
result = normalize_loan_data(extracted_data, document_id='doc_12345')

if result.is_valid:
    loan = result.validated_data
    print(f"Principal: {loan.principal_amount}")
    print(f"Rate: {loan.interest_rate}%")
    print(f"Tenure: {loan.tenure_months} months")
else:
    print("Validation failed:")
    for error in result.errors:
        print(f"  - {error.field}: {error.message}")
```

### Using the Service Class

```python
from normalization import NormalizationService

service = NormalizationService(strict_validation=False)

# Normalize single document
result = service.normalize(extracted_data, document_id='doc_001')

# Get as dictionary
if result.is_valid:
    data_dict = service.get_normalized_dict(result)
    
# Get as JSON
if result.is_valid:
    json_str = service.get_normalized_json(result)
```

### Batch Normalization

```python
from normalization import NormalizationService

service = NormalizationService()

extracted_data_list = [data1, data2, data3]
document_ids = ['doc_001', 'doc_002', 'doc_003']

results = service.normalize_batch(extracted_data_list, document_ids)

for result in results:
    if result.is_valid:
        print(f"✓ {result.validated_data.loan_id}")
    else:
        print(f"✗ Failed with {len(result.errors)} errors")
```

### Quick Normalize

```python
from normalization import quick_normalize

# Returns NormalizedLoanData or None
loan_data = quick_normalize(extracted_data, document_id='doc_001')

if loan_data:
    print(f"Loan ID: {loan_data.loan_id}")
```

### With Payment Schedule

```python
extracted_data = {
    'loan_type': 'personal',
    'bank_name': 'HDFC Bank',
    'principal': 200000,
    'interest_rate': 12.5,
    'tenure': '24 months',
    'payment_schedule': [
        {
            'payment_number': 1,
            'payment_date': '2024-02-01',
            'total_amount': 9456.78,
            'principal': 7373.45,
            'interest': 2083.33,
            'balance': 192626.55
        },
        # ... more entries
    ],
    'confidence': 0.92
}

result = normalize_loan_data(extracted_data, 'doc_001')
```

### With Multiple Fees

```python
extracted_data = {
    'loan_type': 'home',
    'bank_name': 'ICICI Bank',
    'principal_amount': 5000000,
    'interest_rate': 7.5,
    'tenure_months': 240,
    'fees': [
        {
            'type': 'Processing Fee',
            'amount': 25000,
            'currency': 'INR'
        },
        {
            'type': 'Legal Fee',
            'amount': 15000,
            'currency': 'INR'
        }
    ],
    'confidence': 0.88
}

result = normalize_loan_data(extracted_data, 'doc_001')
```

## Field Mapping

The field mapper recognizes multiple variations of field names:

| Standard Field | Recognized Variations |
|----------------|----------------------|
| `principal` | principal, loan_amount, principal_amount, amount, loan_amt, sanctioned_amount |
| `interest_rate` | interest_rate, rate, interest, roi, rate_of_interest, annual_rate, apr |
| `tenure` | tenure, loan_tenure, period, loan_period, duration, term, loan_term |
| `moratorium` | moratorium, grace_period, moratorium_period, grace, holiday_period |
| `bank_name` | bank_name, lender, bank, lender_name, institution |
| `processing_fee` | processing_fee, processing_charges, processing, upfront_fee |

## Data Type Normalization

### Currency Values

Handles various currency formats:
- `₹5,00,000` → `500000.0`
- `Rs. 50000` → `50000.0`
- `$1,000` → `1000.0`

### Percentages

Normalizes percentage values:
- `8.5%` → `8.5`
- `12.5 percent` → `12.5`

### Tenure

Converts to months:
- `5 years` → `60`
- `24 months` → `24`
- `3.5 years` → `42`

### Dates

Parses multiple date formats:
- `2024-02-01`
- `01-02-2024`
- `01/02/2024`
- `01-Feb-2024`
- `01 February 2024`

## Validation Rules

### Required Fields

- `loan_id`
- `document_id`
- `loan_type`
- `bank_info.bank_name`
- `principal_amount` (must be > 0)
- `interest_rate` (must be 0-100)
- `tenure_months` (must be > 0)
- `extraction_confidence` (must be 0.0-1.0)

### Business Rules

- Principal amount: warns if < 1,000 or > 100,000,000
- Interest rate: warns if < 0.1% or > 50%
- Tenure: warns if < 1 month or > 360 months
- Moratorium: warns if > tenure or > 60 months
- Total fees: warns if > 10% of principal
- Extraction confidence: warns if < 0.7

### Payment Schedule Validation

- Payment numbers must be sequential
- Dates must be chronological
- Outstanding balance must decrease
- Final balance should be close to zero
- Number of payments should match tenure

## Error Handling

### Validation Result

```python
result = normalize_loan_data(extracted_data, document_id)

# Check validity
if result.is_valid:
    loan_data = result.validated_data
else:
    # Handle errors
    for error in result.errors:
        print(f"Field: {error.field}")
        print(f"Type: {error.error_type}")
        print(f"Message: {error.message}")

# Check warnings
if result.warnings:
    for warning in result.warnings:
        print(f"Warning: {warning}")
```

### Common Error Types

- `value_error`: Invalid value for field
- `type_error`: Wrong data type
- `missing`: Required field missing
- `validation_error`: Failed validation rule
- `normalization_error`: Error during normalization

## Integration

### With Extraction Module

```python
from extraction import ExtractionService
from normalization import NormalizationService

# Extract data
extraction_service = ExtractionService()
extracted_data = extraction_service.extract(document)

# Normalize data
normalization_service = NormalizationService()
result = normalization_service.normalize(
    extracted_data=extracted_data,
    document_id=document.id
)

if result.is_valid:
    # Store normalized data
    store_loan_data(result.validated_data)
```

### With Storage Module

```python
from normalization import normalize_loan_data
from storage import StorageService

result = normalize_loan_data(extracted_data, document_id)

if result.is_valid:
    storage = StorageService()
    storage.store_loan(result.validated_data)
```

## Examples

See `example_usage.py` for comprehensive examples including:

1. Basic normalization
2. Normalization with payment schedule
3. Normalization with multiple fees
4. Validation error handling
5. Quick normalize convenience function
6. Batch normalization

Run examples:

```bash
cd Lab3/normalization
python example_usage.py
```

## Testing

The normalization module includes comprehensive validation:

- Pydantic model validation
- Field mapping validation
- Business rule validation
- Payment schedule consistency checks
- Data type normalization

## Dependencies

- `pydantic`: Data validation and schema definition
- `python-dateutil` (optional): Enhanced date parsing

## API Reference

### NormalizationService

#### `__init__(strict_validation: bool = False)`
Initialize service with optional strict validation mode.

#### `normalize(extracted_data: Dict, document_id: str, loan_id: Optional[str] = None) -> ValidationResult`
Normalize extracted loan data.

#### `normalize_batch(extracted_data_list: List[Dict], document_ids: List[str]) -> List[ValidationResult]`
Normalize multiple documents.

#### `validate_only(loan_data: Dict) -> ValidationResult`
Validate without field mapping.

#### `get_normalized_dict(result: ValidationResult) -> Optional[Dict]`
Get normalized data as dictionary.

#### `get_normalized_json(result: ValidationResult) -> Optional[str]`
Get normalized data as JSON string.

### Convenience Functions

#### `normalize_loan_data(extracted_data: Dict, document_id: str, loan_id: Optional[str] = None, strict: bool = False) -> ValidationResult`
Quick normalization function.

#### `quick_normalize(extracted_data: Dict, document_id: str) -> Optional[NormalizedLoanData]`
Returns normalized data or None.

#### `validate_loan_data_quick(data: Dict) -> bool`
Quick validation check returning boolean.

## License

Part of the Student Loan Document Extractor Platform.
