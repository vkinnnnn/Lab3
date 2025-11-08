# Structured Data Output Generation

This module implements structured JSON output generation and comparison metrics calculation for loan document data.

## Overview

The output generation system provides:

1. **JSON Output Generation**: Converts normalized loan data into structured JSON format with proper data types and preserved table relationships
2. **Comparison Metrics Calculation**: Calculates key metrics for objective loan comparison including total cost, effective interest rate, and flexibility scores
3. **Unified Output Service**: Combines both capabilities into a single, easy-to-use interface

## Components

### Data Models (`data_models.py`)

Defines Pydantic models for structured loan data:

- `LoanType`: Enumeration of loan types (education, home, personal, vehicle, gold)
- `DocumentMetadata`: Document upload and storage metadata
- `BankInfo`: Lending institution information
- `CoSignerDetails`: Co-signer information
- `FeeItem`: Individual fee or charge
- `PaymentScheduleEntry`: Single payment schedule entry
- `TableData`: Structured table data with headers and rows
- `NormalizedLoanData`: Complete normalized loan data structure
- `ComparisonMetrics`: Calculated comparison metrics
- `ComparisonResult`: Multi-loan comparison results

### JSON Output Generator (`output_generator.py`)

Generates structured JSON output documents:

**Key Features:**
- Converts loan data to JSON format with all extracted fields
- Preserves table structures with row-column relationships
- Handles nested column hierarchies
- Formats mixed content (text, numbers, special characters) with proper data types
- Links output to source documents
- Saves to file or returns JSON string

**Usage:**
```python
from normalization import JSONOutputGenerator, NormalizedLoanData

generator = JSONOutputGenerator(output_directory="./output")

# Generate output document
output_doc = generator.generate_output_document(
    loan_data,
    comparison_metrics=metrics,
    save_to_file=True
)

# Get JSON string
json_str = generator.generate_json_string(loan_data, pretty=True)
```

### Comparison Metrics Calculator (`comparison_calculator.py`)

Calculates metrics for loan comparison:

**Calculated Metrics:**

1. **Total Cost Estimate**: Principal + Interest + All Fees
2. **Effective Interest Rate**: Nominal rate adjusted for fees
3. **Flexibility Score** (0-10): Based on:
   - Moratorium period (0-3 points)
   - Prepayment penalty terms (0-4 points)
   - Repayment mode options (0-3 points)
4. **Monthly EMI**: Calculated using standard EMI formula
5. **Total Interest Payable**: Total interest over loan tenure

**Usage:**
```python
from normalization import ComparisonMetricsCalculator

calculator = ComparisonMetricsCalculator()

# Calculate metrics for single loan
metrics = calculator.calculate_metrics(loan_data)

# Compare multiple loans
comparison = calculator.compare_loans([loan1, loan2, loan3])
```

### Output Service (`output_service.py`)

Unified interface combining output generation and metrics calculation:

**Usage:**
```python
from normalization import OutputService

service = OutputService(output_directory="./output")

# Generate complete output with metrics
output_doc = service.generate_complete_output(
    loan_data,
    source_document_path="/path/to/source.pdf",
    save_to_file=True
)

# Compare multiple loans
comparison_result = service.generate_comparison_output(
    [loan1, loan2, loan3],
    save_to_file=True
)
```

## Output Document Structure

The generated JSON output has the following structure:

```json
{
  "document_info": {
    "loan_id": "uuid",
    "document_id": "uuid",
    "extraction_timestamp": "ISO-8601 datetime",
    "extraction_confidence": 0.95
  },
  "loan_classification": {
    "loan_type": "education",
    "bank_info": {
      "bank_name": "Bank Name",
      "branch_name": "Branch",
      "bank_code": "CODE"
    }
  },
  "core_terms": {
    "principal_amount": 500000.0,
    "currency": "INR",
    "interest_rate": 8.5,
    "tenure_months": 60,
    "moratorium_period_months": 6,
    "repayment_mode": "EMI"
  },
  "fees_and_charges": {
    "processing_fee": 5000.0,
    "late_payment_penalty": "2% per month",
    "prepayment_penalty": "No penalty after 12 months",
    "detailed_fees": [
      {
        "fee_type": "processing",
        "amount": 5000.0,
        "currency": "INR",
        "conditions": "One-time"
      }
    ]
  },
  "payment_schedule": [
    {
      "payment_number": 1,
      "payment_date": "2024-01-15",
      "total_amount": 8500.0,
      "principal_component": 5000.0,
      "interest_component": 3500.0,
      "outstanding_balance": 495000.0
    }
  ],
  "additional_details": {
    "co_signer": {
      "name": "John Doe",
      "relationship": "Father",
      "contact": "+91-9876543210"
    },
    "collateral_details": "None",
    "disbursement_terms": "Direct to institution"
  },
  "extracted_tables": [
    {
      "table_id": "table_001",
      "table_type": "fee_structure",
      "headers": ["Fee Type", "Amount", "Conditions"],
      "data": [
        ["Processing Fee", 5000, "One-time"],
        ["Administrative Fee", 1000, "Annual"]
      ],
      "structured_data": [
        {
          "Fee Type": "Processing Fee",
          "Amount": 5000,
          "Conditions": "One-time"
        }
      ]
    }
  ],
  "raw_fields": {
    "original_principal": "Rs. 5,00,000"
  },
  "comparison_metrics": {
    "total_cost_estimate": 712500.0,
    "effective_interest_rate": 8.65,
    "flexibility_score": 7.0,
    "monthly_emi": 10250.50,
    "total_interest_payable": 206000.0,
    "calculation_timestamp": "ISO-8601 datetime"
  },
  "source_document": {
    "path": "/path/to/source.pdf",
    "linked_at": "ISO-8601 datetime"
  }
}
```

## Key Features

### Mixed Content Handling

The output generator automatically formats mixed content with proper data types:

- Numbers are converted to `int` or `float`
- Currency symbols and percentage signs are preserved in context
- Text remains as strings
- Special characters are maintained

Example:
```python
# Input: "₹5,00,000"
# Output: 500000 (as number)

# Input: "8.5%"
# Output: 8.5 (as number)

# Input: "No penalty"
# Output: "No penalty" (as string)
```

### Table Structure Preservation

Tables are preserved with:
- Original headers and rows
- Nested column hierarchies (if present)
- Structured data mapping headers to values
- Proper data type formatting for each cell

### Comparison Metrics

The flexibility score provides an objective measure of loan flexibility:

| Factor | Points | Criteria |
|--------|--------|----------|
| Moratorium Period | 0-3 | 3 pts: ≥12 months, 2 pts: ≥6 months, 1 pt: ≥3 months |
| Prepayment Penalty | 0-4 | 4 pts: No penalty, 2 pts: Conditional waiver, 1 pt: Minimal |
| Repayment Mode | 0-3 | 3 pts: Step-up/Flexible, 2 pts: Bullet, 1 pt: EMI |

## Requirements Satisfied

This implementation satisfies the following requirements:

- **4.1-4.12**: Structured data output in JSON format with all fields
- **5.1**: Total cost estimate calculation
- **5.2**: Effective interest rate calculation
- **5.3**: Flexibility score calculation
- **5.4**: Metrics storage in output document

## Example Usage

See `example_output_usage.py` for a complete demonstration of:
- Creating sample loan data
- Generating JSON output with metrics
- Comparing multiple loans
- Accessing comparison results

Run the example:
```bash
cd Lab3/normalization
python example_output_usage.py
```

## Integration

This module integrates with:
- **Extraction Module**: Receives normalized loan data
- **Storage Module**: Saves output documents to storage
- **API Layer**: Provides output for API responses
- **Dashboard**: Supplies data for visualization

## Future Enhancements

Potential improvements:
- XML output format support
- CSV export for tabular data
- Custom metric formulas
- Advanced comparison algorithms
- Visualization data generation
