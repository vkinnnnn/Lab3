# Quick Start Guide - Document Ingestion Module

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

1. **Navigate to the Lab3 directory**:
   ```bash
   cd Lab3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies** (for OCR support):
   
   **Windows**:
   - Tesseract OCR: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Poppler (for pdf2image): Download from https://github.com/oschwartz10612/poppler-windows/releases
   
   **Linux**:
   ```bash
   sudo apt-get install tesseract-ocr poppler-utils
   ```
   
   **macOS**:
   ```bash
   brew install tesseract poppler
   ```

4. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update settings as needed.

## Running the API

Start the FastAPI server:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## Testing the Implementation

### Option 1: Using the Test Script

```bash
python test_ingestion.py
```

This will test document upload with a sample PDF from the `sample-loan-docs` directory.

### Option 2: Using the API

1. Open your browser and go to http://localhost:8000/docs

2. Try the `/api/v1/documents/upload` endpoint:
   - Click "Try it out"
   - Choose a file (PDF, JPEG, PNG, or TIFF)
   - Click "Execute"

3. You should receive a response with document metadata:
   ```json
   {
     "document_id": "uuid-here",
     "file_name": "your-file.pdf",
     "file_type": "pdf",
     "upload_timestamp": "2024-10-23T...",
     "file_size_bytes": 123456,
     "page_count": 5,
     "storage_path": "uploads/uuid.pdf",
     "file_hash": "sha256-hash",
     "additional_metadata": {...}
   }
   ```

### Option 3: Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/document.pdf"
```

## Batch Upload

To upload multiple documents at once:

```bash
curl -X POST "http://localhost:8000/api/v1/documents/batch-upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf" \
  -F "files=@document3.pdf"
```

## Supported File Formats

- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- TIFF (`.tif`, `.tiff`) - including multi-page

## File Limits

- Maximum file size: 50 MB
- Maximum pages: 50 pages per document

## Troubleshooting

### Import Error: No module named 'magic'

Install python-magic:
```bash
pip install python-magic python-magic-bin
```

### PDF Conversion Error

Ensure poppler is installed and accessible in your system PATH.

### Tesseract Not Found

Set the TESSERACT_CMD in your `.env` file:
```
TESSERACT_CMD=/path/to/tesseract
```

## Next Steps

Once the document ingestion module is working:
1. Integrate with OCR processing (Task 3)
2. Implement data extraction (Task 4)
3. Set up database storage (Task 5)
4. Build the web dashboard (Task 6)
