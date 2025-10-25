# Quick Start Guide - Document Extraction

## What This Does

Extracts **ALL information** from loan documents using Google Document AI and outputs **professional JSON** with no extras.

---

## 3 Ways to Use

### 1. Test Script (Easiest)

```bash
python Lab3/test_extraction.py your_document.pdf
```

Output saved to: `Lab3/output/your_document_extracted.json`

### 2. Python Code

```python
from processing.document_processor import DocumentProcessor

processor = DocumentProcessor()

with open('document.pdf', 'rb') as f:
    content = f.read()

# Get result
result = processor.process_document(content, "application/pdf", "document.pdf")

# Get JSON string
json_output = processor.get_professional_json(content, "application/pdf", "document.pdf")

# Save to file
processor.save_json_output(content, "application/pdf", "document.pdf", "output.json")
```

### 3. API

```bash
# Start server
cd Lab3
uvicorn api.main:app --port 8000

# Extract document
curl -X POST "http://localhost:8000/api/v1/extract" -F "file=@document.pdf"
```

---

## What You Get

Professional JSON with:

```json
{
  "document_metadata": {
    "document_name": "...",
    "confidence_score": 0.98,
    "total_pages": 5
  },
  "loan_information": {
    "loan_amount": "...",
    "interest_rate": "...",
    "monthly_payment": "..."
  },
  "form_fields": {...},
  "tables": [...],
  "full_text_content": "..."
}
```

---

## Requirements

1. Google Cloud service account key at: `Lab3/service-account-key.json`
2. Python packages: `pip install -r requirements.txt`
3. Document AI processors configured (already set up)

---

## Output Features

✓ Clean JSON with 2-space indentation
✓ All text, numbers, and tables extracted
✓ Confidence scores for validation
✓ No emojis or extras
✓ Exact data from source document

---

## Example

```bash
# Test with your loan document
python Lab3/test_extraction.py Lab3/uploads/loan_agreement.pdf

# Check output
cat Lab3/output/loan_agreement_extracted.json
```

---

## Supported Files

- PDF documents (`.pdf`)
- Images (`.jpg`, `.png`)
- Multi-page documents
- Scanned documents

---

## Need Help?

See full documentation: `Lab3/EXTRACTION_GUIDE.md`
