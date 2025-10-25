<div align="center">

# 📄 Complete Document Extractor

### *Enterprise-Grade Document Intelligence Platform*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)

**Powered by Google Document AI | 90-99% Accuracy | Production Ready**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Tech Stack](#-tech-stack)

---

</div>

## 🎯 Overview

A comprehensive **document extraction system** that leverages Google Document AI to extract **ALL** text, numbers, tables, and form fields from documents with **real-time accuracy validation**. Built for production with a modern tech stack and enterprise-grade reliability.

### Why This Project?

- 🚀 **Complete Extraction**: Captures every piece of data - text, numbers, tables, nested columns
- 🎯 **Dual Processor System**: Uses both Form Parser and Document OCR for maximum accuracy
- 📊 **Real Accuracy Metrics**: Actual confidence scores (90-99%) with quality validation
- 🖥️ **Modern UI**: Beautiful Streamlit dashboard with real-time processing
- 🔌 **REST API**: Complete API for seamless integration
- 🐳 **Docker Ready**: One-command deployment with full orchestration

---

## ✨ Features

### 📝 Complete Text Extraction
- All blocks, paragraphs, lines, tokens
- Multi-processor validation
- Original formatting preserved

### 🔢 Smart Number Detection
- Integers, decimals, percentages
- Currency values ($1,234.56)
- Context-aware extraction

### 📋 Form Field Processing
- Original field names preserved
- Checkbox and radio button states
- Field-level confidence scores

### 📊 Advanced Table Extraction
- Complete structure preservation
- Nested columns & merged cells
- Row/column span detection

### 🎯 Accuracy Validation
- Overall accuracy (90-99%)
- Per-processor metrics
- Page-by-page confidence

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (20.10+)
- Google Cloud Account with Document AI API
- Git

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/vkinnnnn/Lab3.git
cd Lab3

# 2. Setup Google Cloud credentials
# - Create service account
# - Enable Document AI API
# - Download service-account-key.json

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Deploy
docker-compose up -d

# 5. Access services
# Dashboard: http://localhost:8501
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **AI/ML** | Google Document AI |
| **Backend** | FastAPI, Python 3.11 |
| **Frontend** | Streamlit |
| **Database** | PostgreSQL 15 |
| **Cache** | Redis 7 |
| **Storage** | MinIO |
| **Container** | Docker, Docker Compose |

---

## 📖 Usage

### Web Dashboard

1. Open http://localhost:8501
2. Upload document (PDF, JPG, PNG)
3. Click "Extract Complete Document"
4. View results and download JSON

### API Example

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@document.pdf"
```

### Python Example

```python
import requests

with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/extract',
        files={'file': f}
    )

result = response.json()
print(f"Accuracy: {result['accuracy_metrics']['overall_accuracy']:.1%}")
```

---

## 📊 Performance

- **Accuracy**: 90-99% typical
- **Processing Time**: 10-30 seconds per document
- **Supported Formats**: PDF, JPG, PNG, TIFF
- **Max File Size**: 20MB per document

---

## 🐳 Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| API | 8000 | FastAPI backend |
| Dashboard | 8501 | Streamlit UI |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache |
| MinIO | 9000-9001 | Object storage |

---

## 📁 Project Structure

```
Lab3/
├── api/                    # FastAPI application
├── dashboard/              # Streamlit UI
├── processing/             # Document processing
├── worker/                 # Background tasks
├── docker-compose.yml      # Docker config
└── requirements.txt        # Dependencies
```

---

## 🔐 Security

- ✅ Service Account Authentication
- ✅ Environment Variables
- ✅ Data Masking Capabilities
- ✅ Secure Docker Networking

---

## 📚 Documentation

- [SETUP.md](SETUP.md) - Complete setup guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- Google Document AI
- FastAPI
- Streamlit
- Docker

---

<div align="center">

### Built with ❤️ using Google Document AI

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Google Cloud](https://img.shields.io/badge/Powered%20by-Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)

**⭐ Star this repo if you find it useful!**

</div>
