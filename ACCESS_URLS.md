# Quick Access URLs

## Services

### 🚀 API Service
**URL**: http://localhost:8000
**Status**: ✓ Running
**Docs**: http://localhost:8000/docs (FastAPI auto-docs)

### 📊 Dashboard
**URL**: http://localhost:8501
**Status**: ✓ Running
**Purpose**: Upload and view extraction results

### 💾 MinIO Console
**URL**: http://localhost:9001
**Status**: ✓ Running
**Purpose**: Object storage management

---

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Extraction Service Health
```bash
curl http://localhost:8000/api/v1/health
```

### Extract Document
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@document.pdf"
```

### Get Formatted JSON
```bash
curl -X POST "http://localhost:8000/api/v1/extract/json" \
  -F "file=@document.pdf"
```

### Extract and Save
```bash
curl -X POST "http://localhost:8000/api/v1/extract/save" \
  -F "file=@document.pdf"
```

---

## Quick Test

```bash
# Test extraction (replace with your file)
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@your_loan_document.pdf" \
  | python -m json.tool
```

---

## Management

### View Logs
```bash
docker-compose logs -f api
```

### Restart Services
```bash
docker-compose restart
```

### Stop Services
```bash
docker-compose down
```

---

**All services are running and ready to use!**
