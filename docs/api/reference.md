# API Reference

## Overview

The Student Loan Intelligence System API provides comprehensive endpoints for document processing, loan comparison, chatbot interactions, and translation services. The API is built with FastAPI and follows RESTful principles.

## Base URL
```
Production: https://api.student-loan-intelligence.com
Development: http://localhost:8000
```

## Authentication

All API endpoints (except public ones) require authentication using JWT tokens.

### Authorization Header
```
Authorization: Bearer <your_jwt_token>
```

### Getting a Token
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Document Processing API

### Upload Document
```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>

Form Data:
- file: <binary_file_data> (required)
- document_type: string (optional)
- ocr_engine: string (optional, values: "tesseract", "easyocr", "auto")
- format: string (optional, values: "json", "csv", "xlsx")
```

**Response:**
```json
{
  "document_id": "doc_123456789",
  "status": "processing",
  "uploaded_at": "2025-01-15T10:30:00Z",
  "estimated_completion": "2025-01-15T10:35:00Z"
}
```

### Get Processing Status
```http
GET /api/v1/documents/{document_id}/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "document_id": "doc_123456789",
  "status": "completed",
  "progress": 100,
  "uploaded_at": "2025-01-15T10:30:00Z",
  "processed_at": "2025-01-15T10:32:15Z",
  "processing_time_ms": 135000,
  "confidence_score": 0.98
}
```

### Get Extracted Data
```http
GET /api/v1/documents/{document_id}/data
Authorization: Bearer <token>
```

**Query Parameters:**
- `format`: Output format (json, xml, csv)
- `include_confidence`: Include confidence scores

**Response:**
```json
{
  "document_id": "doc_123456789",
 extracted_data: {
    "personal_info": {
      "name": {
        "value": "John Doe",
        "confidence": 0.99,
        "source_bounding_box": [100, 50, 200, 80],
        "extraction_method": "ai_field_detection"
      },
      "ssn": {
        "value": "123-45-6789",
        "confidence": 0.97,
        "source_bounding_box": [100, 90, 150, 110],
        "extraction_method": "ai_field_detection"
      }
    },
    "financial_data": {
      "income": {
        "value": 75000.00,
        "confidence": 0.98,
        "source_bounding_box": [100, 130, 180, 150],
        "extraction_method": "ai_field_detection"
      }
    }
  },
  "processing_metadata": {
    "ocr_engine": "easyocr",
    "confidence_score": 0.98,
    "processing_time_ms": 135000,
    "field_count": 12
  }
}
```

### Correct Extracted Data
```http
POST /api/v1/documents/{document_id}/correct
Content-Type: application/json
Authorization: Bearer <token>

{
  "corrections": {
    "personal_info.name": "John D. Smith",
    "financial_data.income": 85000.00
  },
  "reason": "User correction",
  "confidence": 1.0
}
```

### Delete Document
```http
DELETE /api/v1/documents/{document_id}
Authorization: Bearer <token>
```

## Chatbot API

### Send Message
```http
POST /api/v1/chatbot/message
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "What is the difference between subsidized and unsubsidized loans?",
  "context": {
    "document_id": "doc_123456789",
    "conversation_id": "conv_456789"
  },
  "model": "claude-3-sonnet-20241022",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "message_id": "msg_987654321",
  "conversation_id": "conv_456789",
  "response": "Subsidized loans don't accrue interest while you're in school...",
  "model_used": "claude-3-sonnet-20241022",
  "tokens_used": 245,
  "processing_time_ms": 1250,
  "confidence": 0.94,
  "sources": [
    {
      "title": "Federal Student Aid Guide",
      "url": "https://studentaid.gov/...",
      "relevance_score": 0.89
    }
  ],
  "timestamp": "2025-01-15T11:45:30Z"
}
```

### Get Conversation History
```http
GET /api/v1/chatbot/conversations/{conversation_id}/history
Authorization: Bearer <token>

Query Parameters:
- limit: Number of messages (default: 50)
- offset: Pagination offset (default: 0)
```

**Response:**
```json
{
  "conversation_id": "conv_456789",
  "messages": [
    {
      "message_id": "msg_123456789",
      "message": "What is the difference between subsidized and unsubsidized loans?",
      "sender": "user",
      "timestamp": "2025-01-15T11:44:00Z"
    },
    {
      "message_id": "msg_987654321",
      "message": "Subsidized loans don't accrue interest while you're in school...",
      "sender": "bot",
      "timestamp": "2025-01-15T11:45:30Z",
      "model_used": "claude-3-sonnet-20241022",
      "tokens_used": 245
    }
  ],
  "total_messages": 22,
  "has_more": false
}
```

### Stream Chat Response
```http
POST /api/v1/chatbot/stream
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "Explain loan consolidation",
  "stream": true
}
```

**Response:** Server-Sent Events (SSE) stream

## Loan Comparison API

### Compare Loans
```http
POST /api/v1/comparison/compare
Content-Type: application/json
Authorization: Bearer <token>

{
  "loan_offers": [
    {
      "document_id": "doc_loan_1",
      "principal": 50000,
      "interest_rate": 4.5,
      "term_years": 10,
      "fees": 1500,
      "lender": "Bank A"
    },
    {
      "document_id": "doc_loan_2", 
      "principal": 50000,
      "interest_rate": 5.2,
      "term_years": 10,
      "fees": 0,
      "lender": "Bank B"
    }
  ],
  "analysis_type": "comprehensive"
}
```

**Response:**
```json
{
  "comparison_id": "comp_789012345",
  "analysis_type": "comprehensive",
  "generated_at": "2025-01-15T12:15:00Z",
  "summary": {
    "best_overall": "Bank A",
    "lowest_monthly_payment": "Bank A",
    "lowest_total_cost": "Bank A",
    "lowest_fees": "Bank B"
  },
  "detailed_comparison": {
    "monthly_payments": {
      "Bank A": 518.64,
      "Bank B": 538.23,
      "difference": -19.59
    },
    "total_costs": {
      "Bank A": 62230.80,
      "Bank B": 64587.60,
      "difference": -2356.80
    }
  },
  "recommendations": [
    {
      "loan": "Bank A",
      "reason": "Lower monthly payment and total cost",
      "confidence": 0.92,
      "impact_savings": 2356.80
    }
  ],
  "risk_assessment": {
    "Bank A": {
      "affordability_score": 0.85,
      "default_risk": 0.12,
      "debt_to_income_ratio": 0.15
    },
    "Bank B": {
      "affordability_score": 0.82,
      "default_risk": 0.15,
      "debt_to_income_ratio": 0.16
    }
  }
}
```

### Get Comparison Results
```http
GET /api/v1/comparison/{comparison_id}
Authorization: Bearer <token>
```

## Translation API

### Translate Document
```http
POST /api/v1/translation/translate
Content-Type: application/json
Authorization: Bearer <token>

{
  "document_id": "doc_123456789",
  "source_language": "en",
  "target_language": "es",
  "format": "preserving",
  "translate_fields": ["personal_info", "loan_terms"]
}
```

**Response:**
```json
{
  "translation_id": "trans_789012345",
  "source_language": "en",
  "target_language": "es",
  "translated_data": {
    "personal_info": {
      "name": {
        "original": "John Doe",
        "translated": "Juan Pérez",
        "confidence": 0.98
      }
    },
    "translation_metadata": {
      "total_fields_translated": 8,
      "average_confidence": 0.96,
      "model_used": "gpt-4-turbo",
      "processing_time_ms": 2100
    }
  }
}
```

### Get Supported Languages
```http
GET /api/v1/translation/languages
```

**Response:**
```json
{
  "supported_languages": [
    {
      "code": "en",
      "name": "English",
      "is_source": true,
      "is_target": true
    },
    {
      "code": "es",
      "name": "Spanish",
      "is_source": true,
      "is_target": true
    },
    {
      "code": "fr",
      "name": "French",
      "is_source": true,
      "is_target": true
    }
  ]
}
```

## Analytics API

### Get User Statistics
```http
GET /api/v1/analytics/user/stats
Authorization: Bearer <token>

Query Parameters:
- start_date: ISO 8601 date
- end_date: ISO 8601 date
```

**Response:**
```json
{
  "period": {
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-01-31T23:59:59Z"
  },
  "document_usage": {
    "documents_processed": 45,
    "processing_success_rate": 0.98,
    "average_processing_time_ms": 125000,
    "total_pages_processed": 234
  },
  "chatbot_usage": {
    "messages_sent": 156,
    "average_response_time_ms": 1450,
    "satisfaction_score": 4.6
  },
  "comparison_usage": {
    "comparisons_made": 12,
    "average_savings_identified": 3500.00,
    "recommendation_acceptance_rate": 0.75
  }
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "type": "ValidationError",
    "code": "VALIDATION_ERROR",
    "message": "Invalid file format",
    "details": {
      "field": "file_type",
      "value": "txt",
      "constraint": "Must be one of: pdf, docx, jpg, jpeg, png, tiff, bmp"
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Validation failed |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 413 | Payload Too Large - File exceeds size limit |
| 422 | Unprocessable Entity - Data format issues |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Unexpected error |
| 503 | Service Unavailable - Temporary outage |

## Rate Limits

| Endpoint | Limit | Time Window |
|----------|-------|-------------|
| Document Upload | 50 requests | 1 hour |
| Chatbot Message | 500 requests | 1 hour |
| API Request (other) | 1000 requests | 1 hour |

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1642297200
```

## SDK Examples

### Python SDK
```python
from student_loan_intelligence import StudentLoanAPI

# Initialize client
client = StudentLoanAPI(api_key="your_api_key")

# Upload document
doc = client.documents.upload(
    file_path="loan_application.pdf",
    document_type="student_loan_application"
)

# Wait for processing
result = client.documents.wait_for_completion(doc.id)

# Get extracted data
data = client.documents.get_data(doc.id)
print(data.extracted_data.personal_info.name.value)
```

### JavaScript SDK
```javascript
import { StudentLoanAPI } from 'student-loan-intelligence';

// Initialize client
const client = new StudentLoanAPI({ apiKey: 'your_api_key' });

// Upload and process document
const document = await client.documents.upload({
  file: loanPdf,
  documentType: 'student_loan_application'
});

// Send chatbot message
const response = await client.chatbot.sendMessage({
  message: 'What is the interest rate?',
  context: { documentId: document.id }
});
```

## Webhook Integration

### Configure Webhook
```http
POST /api/v1/webhooks/configure
Content-Type: application/json
Authorization: Bearer <token>

{
  "url": "https://your-app.com/webhooks/processing-complete",
  "events": ["document.completed", "document.failed"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload
```json
{
  "event": "document.completed",
  "timestamp": "2025-01-15T10:35:00Z",
  "data": {
    "document_id": "doc_123456789",
    "status": "completed",
    "processing_time_ms": 135000,
    "confidence_score": 0.98
  },
  "signature": "sha256=abc123def456..."
}
```
