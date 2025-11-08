# Multi-Document Comparison Engine

## Overview

The Multi-Document Comparison Engine enables comprehensive comparison of multiple loan documents, identifying the best options by cost and flexibility, and generating detailed pros/cons analysis for each loan.

## Features

1. **Multi-Document Processing**: Accept and compare multiple loan documents simultaneously
2. **Comparison Table Generation**: Create structured comparison tables with key loan fields
3. **Best Option Identification**: Automatically identify best loans by:
   - Total cost (lowest)
   - Flexibility (highest repayment flexibility)
4. **Pros/Cons Analysis**: Generate detailed advantages and disadvantages for each loan
5. **Comprehensive Metrics**: Calculate and compare:
   - Total cost estimate
   - Effective interest rate
   - Flexibility score
   - Monthly EMI
   - Total interest payable

## Architecture

### Components

1. **ComparisonService**: Main service orchestrating loan comparison
2. **ComparisonMetricsCalculator**: Calculates financial metrics for each loan
3. **LoanComparison**: Data structure for detailed loan comparison results

### Data Flow

```
Multiple NormalizedLoanData
         ↓
  ComparisonService
         ↓
  ┌──────┴──────┐
  ↓             ↓
Metrics    Pros/Cons
Calculator  Analysis
  ↓             ↓
  └──────┬──────┘
         ↓
  ComparisonResult
```

## Usage

### Basic Comparison

```python
from normalization.comparison_service import ComparisonService
from normalization.data_models import NormalizedLoanData, LoanType, BankInfo

# Create loan data objects
loan1 = NormalizedLoanData(
    loan_id="loan_001",
    document_id="doc_001",
    loan_type=LoanType.EDUCATION,
    bank_info=BankInfo(bank_name="Bank A"),
    principal_amount=500000.0,
    interest_rate=8.5,
    tenure_months=120,
    moratorium_period_months=12,
    processing_fee=5000.0,
    prepayment_penalty="No penalty",
    repayment_mode="EMI"
)

loan2 = NormalizedLoanData(
    loan_id="loan_002",
    document_id="doc_002",
    loan_type=LoanType.EDUCATION,
    bank_info=BankInfo(bank_name="Bank B"),
    principal_amount=500000.0,
    interest_rate=9.0,
    tenure_months=120,
    moratorium_period_months=6,
    processing_fee=10000.0,
    prepayment_penalty="2% penalty",
    repayment_mode="EMI"
)

# Initialize service
service = ComparisonService()

# Compare loans
result = service.compare_loans([loan1, loan2])

print(f"Best by cost: {result.best_by_cost}")
print(f"Best by flexibility: {result.best_by_flexibility}")
```

### Generate Comparison Table

```python
# Generate comparison table
table = service.generate_comparison_table([loan1, loan2])

print("Headers:", table["headers"])
for row in table["rows"]:
    print("Row:", row)
```

### Generate Detailed Comparison with Pros/Cons

```python
# Generate detailed comparison
detailed = service.generate_detailed_comparison([loan1, loan2])

for loan in detailed:
    print(f"\nLoan: {loan['loan_id']}")
    print(f"Bank: {loan['bank_name']}")
    print("\nPros:")
    for pro in loan['pros']:
        print(f"  ✓ {pro}")
    print("\nCons:")
    for con in loan['cons']:
        print(f"  ✗ {con}")
```

## API Endpoints

### POST /api/v1/compare

Compare multiple loan documents and get comprehensive analysis.

**Request Body:**
```json
{
  "loans": [
    {
      "loan_id": "loan_001",
      "document_id": "doc_001",
      "loan_type": "education",
      "bank_info": {
        "bank_name": "State Bank of India"
      },
      "principal_amount": 500000.0,
      "interest_rate": 8.5,
      "tenure_months": 120,
      "moratorium_period_months": 12,
      "processing_fee": 5000.0,
      "prepayment_penalty": "No penalty",
      "repayment_mode": "EMI",
      "fees": [],
      "extraction_confidence": 0.95
    },
    {
      "loan_id": "loan_002",
      "document_id": "doc_002",
      "loan_type": "education",
      "bank_info": {
        "bank_name": "HDFC Bank"
      },
      "principal_amount": 500000.0,
      "interest_rate": 9.0,
      "tenure_months": 120,
      "moratorium_period_months": 6,
      "processing_fee": 10000.0,
      "prepayment_penalty": "2% penalty",
      "repayment_mode": "EMI",
      "fees": [],
      "extraction_confidence": 0.92
    }
  ]
}
```

**Response:**
```json
{
  "comparison_summary": {
    "total_loans": 2,
    "best_by_cost": "loan_001",
    "best_by_flexibility": "loan_001",
    "comparison_notes": {
      "summary": "Compared 2 loan options",
      "cost_range": "Total cost ranges from 1,006,000.00 to 1,062,000.00",
      "rate_range": "Effective interest rate ranges from 8.62% to 9.24%",
      "flexibility_range": "Flexibility scores range from 5.0 to 8.0",
      "best_cost": "Loan loan_001 offers the lowest total cost",
      "best_flexibility": "Loan loan_001 offers the most flexible terms",
      "recommendation": "Loan loan_001 is the best overall option"
    }
  },
  "comparison_table": {
    "headers": ["Loan ID", "Bank", "Loan Type", "Principal Amount", ...],
    "rows": [...]
  },
  "detailed_comparison": [
    {
      "loan_id": "loan_001",
      "bank_name": "State Bank of India",
      "key_fields": {...},
      "metrics": {...},
      "pros": [
        "Lowest total cost among all options",
        "Below-average interest rate",
        "Most flexible repayment terms",
        "Generous moratorium period of 12 months",
        "No prepayment penalty"
      ],
      "cons": [
        "No significant drawbacks identified"
      ]
    }
  ],
  "metrics": [...]
}
```

### POST /api/v1/compare/table

Generate comparison table only (lightweight endpoint).

**Request Body:** Same as `/compare`

**Response:**
```json
{
  "headers": ["Loan ID", "Bank", "Loan Type", ...],
  "rows": [[...], [...]],
  "row_count": 2
}
```

### POST /api/v1/compare/detailed

Generate detailed comparison with pros/cons only.

**Request Body:** Same as `/compare`

**Response:**
```json
{
  "loans": [
    {
      "loan_id": "loan_001",
      "pros": [...],
      "cons": [...]
    }
  ]
}
```

## Comparison Metrics

### Total Cost Estimate
Calculated as: Principal + Total Interest + All Fees

### Effective Interest Rate
Nominal interest rate adjusted for fees and charges:
```
Effective Rate = Nominal Rate + (Total Fees / Principal) × (12 / Tenure) × 100
```

### Flexibility Score (0.0 - 10.0)
Calculated based on:
- **Moratorium Period** (0-3 points):
  - ≥12 months: 3 points
  - ≥6 months: 2 points
  - ≥3 months: 1 point
  
- **Prepayment Penalty** (0-4 points):
  - No penalty: 4 points
  - Conditional waiver: 2 points
  - Minimal penalty: 1 point
  
- **Repayment Mode** (0-3 points):
  - Step-up/Flexible: 3 points
  - Bullet payment: 2 points
  - Standard EMI: 1 point

### Monthly EMI
Calculated using standard EMI formula:
```
EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]
where:
  P = Principal amount
  R = Monthly interest rate
  N = Tenure in months
```

## Pros/Cons Analysis

The engine automatically generates pros and cons by comparing each loan against:
- Average metrics across all loans
- Best and worst values in the comparison set

### Factors Considered

**Pros:**
- Lowest total cost
- Competitive/below-average interest rate
- High flexibility score
- Generous moratorium period
- No/low prepayment penalty
- Low processing fees
- No co-signer requirement
- No collateral requirement

**Cons:**
- Highest total cost
- Above-average interest rate
- Limited flexibility
- No moratorium period
- High prepayment penalty
- High processing fees
- Co-signer required
- Collateral required

## Requirements Satisfied

This implementation satisfies the following requirements from the specification:

- **Requirement 6.1**: Accept multiple Loan Documents for simultaneous processing ✓
- **Requirement 6.2**: Generate comparison table showing principal, interest rate, tenure, fees, and total cost ✓
- **Requirement 6.3**: Identify best option by total cost ✓
- **Requirement 6.4**: Identify best option by repayment flexibility ✓
- **Requirement 6.5**: Provide detailed pros and cons for each loan option ✓

## Error Handling

The comparison engine handles various error scenarios:

1. **Empty loan list**: Raises `ValueError`
2. **Single loan**: Logs warning but proceeds with limited insights
3. **Invalid loan data**: Returns default metrics for failed calculations
4. **Missing fields**: Gracefully handles optional fields with None values

## Testing

Run the test script to verify functionality:

```bash
python test_comparison_engine.py
```

The test script demonstrates:
1. Full comparison with multiple loans
2. Comparison table generation
3. Detailed pros/cons analysis

## Integration

The comparison engine integrates with:
- **Normalization Module**: Uses `NormalizedLoanData` as input
- **Comparison Calculator**: Leverages existing metrics calculation
- **API Layer**: Exposed via REST endpoints
- **Storage Layer**: Can persist comparison results

## Future Enhancements

Potential improvements:
1. Machine learning-based recommendation system
2. User preference weighting (cost vs. flexibility)
3. Historical comparison tracking
4. Export to PDF/Excel formats
5. Visual comparison charts and graphs
6. What-if scenario analysis
7. Loan affordability calculator integration
