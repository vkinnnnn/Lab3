# Multi-stage Dockerfile for Student Loan Document Extractor Platform
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    poppler-utils \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Copy service account key for Document AI
COPY service-account-key.json /app/service-account-key.json

# Create necessary directories
RUN mkdir -p /app/uploads /app/temp /app/processing

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# API Service Stage
FROM base as api
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dashboard Service Stage
FROM base as dashboard
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Worker Service Stage
FROM base as worker
CMD ["python", "-m", "worker.processor"]
