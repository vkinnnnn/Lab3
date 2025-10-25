"""
Configuration settings for the Student Loan Document Extractor Platform
"""
import os
from typing import Optional


class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://loanuser:loanpass123@db:5432/loanextractor"
    )
    
    # Object Storage (S3/MinIO)
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "http://minio:9000")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "minioadmin123")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "loan-documents")
    S3_REGION: str = os.getenv("S3_REGION", "us-east-1")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "4"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "your-encryption-key-change-in-production")
    
    # OCR Configuration
    TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
    
    # Processing Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    MAX_PAGES: int = int(os.getenv("MAX_PAGES", "50"))
    
    # Worker Configuration
    WORKER_CONCURRENCY: int = int(os.getenv("WORKER_CONCURRENCY", "2"))
    WORKER_QUEUE: str = os.getenv("WORKER_QUEUE", "document-processing")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


# Create global config instance
config = Config()
