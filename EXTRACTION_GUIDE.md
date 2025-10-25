# Document Extraction Guide

## Overview

This system extracts **ALL information** from loan-related documents using **Google Document AI** and outputs the data in **professional JSON format**.

### Key Features

- **99%+ Accuracy**: Uses Google Document AI (enterprise-grade OCR)
- **Complete Extraction**: Extracts all text, forms, tables, numbers, and details
- **Professional Output**: Clean JSON format with proper spacing
- **No Extras**: No emojis, no web searches, just the exact data from documents
- **Loan-Focused**: Optimized for loan documents, forms, policies, and agreements

---

## What Gets Extracted

### 1. Document Metadata
- Document name
- Extraction timestamp
- Confidence scores
- Number of pages
- Processors used

### 2. Loan Information
- Loan amount / Principal
- Interest rate / APR
- Loan tenure / Term
- Monthly payment / EMI
- Bank name / Lender
- Loan type / Product
- Borrower name
- Processing fees
- Application number
- Sanctioned amount
- Disbursement date
- Maturity date
- Collateral / Security
- Guarantor information

### 3. Form Fields
- All form fields with values
- Confidence scores for each field
- Exact text as it appears in document

### 4. Tables
- Complete table structure
- Headers and data rows
- All numbers and text preserved
- Table dimensions

### 5. Entities
- Names, dates, amounts
- Organizations, locations
- Document-specific entities

### 6. Full Text Content
- Complete text from all pages
- Exact formatting preserved
- All numbers and details

### 7. Page Details
- Page-by-page information
- Dimensions and confidence
- Page numbering

---

## JSON Output Format

```json
{
  "document_metadata": {
    "document_name": "loan_agreement.pdf",
    "extraction_timestamp": "2025-10-25T10:30:00",
    "extraction_method": "Google Document AI",
    "processors_used": ["Form Parser", "Document OCR"],
    "confidence_score": 0.9850,
    "total_pages": 5
  },
  
  "loan_information": {
    "loan_amount": "500000",
    "interest_rate": "8.5%",
    "loan_tenure": "240 months",
    "monthly_payment": "4182",
    "bank_name": "ABC Bank",
    "loan_type": "Home Loan",
    "borrower_name": "John Doe",
    "processing_fee": "5000"
  },
  
  "form_fields": {
    "applicant_name": {
      "value": "John Doe",
      "confidence": 0.9900
    },
    "loan_amount": {
      "value": "500000",
      "confidence": 0.9850
    }
  },
  
  "tables": [
    {
      "table_id": 1,
      "rows": 10,
      "columns": 4,
      "headers": [["Month", "Principal", "Interest", "Balance"]],
      "data": [
        ["1", "2500", "1682", "497500"],
        ["2", "2510", "1672", "494990"]
      ]
    }
  ],
  
  "entities": [
    {
      "type": "person_name",
      "text": "John Doe",
      "confidence": 0.9900
    }
  ],
  
  "full_text_content": "Complete text from all pages...",
  
  "page_details": [
    {
      "page_number": 1,
      "dimensions": {
        "width": 612,
        "height": 792
      },
      "confidence": 0.9850
    }
  ]
}
```

---

## How to Use

### Method 1: Python Script

```python
from processing.document_processor import DocumentProcessor

# Initialize processor
processor = DocumentProcessor()

# Read your PDF
with open('loan_document.pdf', 'rb') as f:
    file_content = f.read()

# Extract data
result = processor.process_document(
    file_content,
    "application/pdf",
    "loan_document.pdf"
)

# Get professional JSON
json_output = processor.get_professional_json(
    file_content,
    "application/pdf",
    "loan_document.pdf"
)

# Save to file
processor.save_json_output(
    file_content,
    "application/pdf",
    "loan_document.pdf",
    "output/extracted_data.json"
)
```

### Method 2: Test Script

```bash
# Test extraction with any PDF
python Lab3/test_extraction.py path/to/your/document.pdf

# Example
python Lab3/test_extraction.py Lab3/uploads/loan_agreement.pdf
```

### Method 3: API Endpoint

```bash
# Start the API server
cd Lab3
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Upload and extract
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@loan_document.pdf"

# Get formatted JSON
curl -X POST "http://localhost:8000/api/v1/extract/json" \
  -F "file=@loan_document.pdf"

# Extract and save
curl -X POST "http://localhost:8000/api/v1/extract/save" \
  -F "file=@loan_document.pdf"
```

### Method 4: Docker

```bash
# Build and run
docker-compose up

# Upload document
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@loan_document.pdf"
```

---

## Supported Document Types

- **Loan Agreements**: Home loans, personal loans, auto loans
- **Loan Applications**: Application forms with borrower details
- **Loan Statements**: Payment schedules, account statements
- **Policies**: Loan policies, terms and conditions
- **Brochures**: Product information, rate sheets
- **Forms**: Any structured loan-related forms

### Supported File Formats

- PDF (`.pdf`)
- Images (`.jpg`, `.jpeg`, `.png`)
- TIFF (`.tiff`, `.tif`)

---

## Configuration

### Google Document AI Setup

The system uses two Document AI processors:

1. **Form Parser** (`337aa94aac26006`)
   - Best for structured forms
   - Extracts form fields with high accuracy
   - Handles checkboxes, radio buttons

2. **Document OCR** (`c0c01b0942616db6`)
   - Extracts all text content
   - Handles unstructured documents
   - Backup for form parser

### Service Account

Place your Google Cloud service account key at:
```
Lab3/service-account-key.json
```

Required permissions:
- `documentai.documents.process`
- `documentai.processors.use`

---

## Output Quality

### Confidence Scores

- **0.95 - 1.00**: Excellent (99%+ accuracy)
- **0.90 - 0.95**: Very Good (95%+ accuracy)
- **0.85 - 0.90**: Good (90%+ accuracy)
- **Below 0.85**: Review recommended

### What Makes Output Professional

✓ Clean JSON structure with consistent formatting
✓ Proper indentation (2 spaces)
✓ No emojis or decorative elements
✓ Exact data from source document
✓ Organized by logical sections
✓ Confidence scores for validation
✓ Complete metadata for traceability

---

## Troubleshooting

### Low Confidence Scores

If confidence is below 0.90:
- Check document quality (scan resolution)
- Ensure text is clear and readable
- Verify document is not handwritten
- Try re-scanning at higher DPI

### Missing Data

If expected data is not extracted:
- Check if field names match common patterns
- Review the `form_fields` section
- Look in `full_text_content` for manual extraction
- Verify document is not password-protected

### API Errors

```bash
# Check service account permissions
gcloud auth activate-service-account --key-file=service-account-key.json

# Verify processors are accessible
gcloud documentai processors list --location=us
```

---

## Examples

### Example 1: Home Loan Agreement

Input: 5-page home loan agreement PDF

Output includes:
- Loan amount: $500,000
- Interest rate: 8.5% APR
- Tenure: 20 years (240 months)
- Monthly EMI: $4,182
- Bank: ABC Home Loans
- Borrower details
- Complete amortization table
- All terms and conditions

### Example 2: Loan Application Form

Input: 2-page application form

Output includes:
- Applicant personal information
- Employment details
- Income information
- Requested loan amount
- All form field values
- Signatures and dates

### Example 3: Rate Sheet

Input: 1-page rate comparison sheet

Output includes:
- All interest rates
- Loan products
- Tenure options
- Processing fees
- Complete table data

---

## Best Practices

1. **Document Quality**: Use high-resolution scans (300 DPI minimum)
2. **File Format**: PDF is preferred over images
3. **Validation**: Always check confidence scores
4. **Review**: Manually verify critical financial data
5. **Storage**: Save JSON outputs for audit trail

---

## API Reference

### POST /api/v1/extract

Extract data from document

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF or image)

**Response:**
```json
{
  "document_metadata": {...},
  "loan_information": {...},
  "form_fields": {...},
  "tables": [...],
  "entities": [...],
  "full_text_content": "...",
  "page_details": [...]
}
```

### POST /api/v1/extract/json

Get formatted JSON string

**Response:**
```json
{
  "json_output": "{\n  \"document_metadata\": {...}\n}"
}
```

### POST /api/v1/extract/save

Extract and save to file

**Response:**
```json
{
  "status": "success",
  "message": "Document processed and saved",
  "output_file": "Lab3/output/document_extracted.json"
}
```

---

## Support

For issues or questions:
1. Check confidence scores in output
2. Review full_text_content for missing data
3. Verify service account permissions
4. Check Document AI processor status

---

## Summary

This system provides **enterprise-grade document extraction** with:
- ✓ 99%+ accuracy using Google Document AI
- ✓ Complete data extraction (all text, numbers, tables)
- ✓ Professional JSON output with clean formatting
- ✓ No extras (no emojis, no web searches)
- ✓ Optimized for loan documents
- ✓ Easy to use via API, script, or Docker

**Result**: Exact data from your documents in professional JSON format.
