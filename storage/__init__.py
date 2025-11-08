"""
Storage module for the Student Loan Document Extractor Platform.

This module provides:
- PostgreSQL database management for structured data
- S3/MinIO object storage for documents
- Unified storage service for coordinated operations
- Security features including encryption and access control
"""

from .database import (
    DatabaseManager,
    Document,
    Loan,
    ComparisonMetric,
    ProcessingJob,
    get_database_manager,
    init_database
)

from .object_storage import (
    ObjectStorageManager,
    get_object_storage_manager
)

from .storage_service import (
    StorageService,
    get_storage_service
)

from .security import (
    EncryptionManager,
    AccessControlManager,
    TLSConfig,
    AuditLogger,
    UserRole,
    get_encryption_manager,
    get_access_control_manager,
    get_audit_logger
)

__all__ = [
    # Database
    'DatabaseManager',
    'Document',
    'Loan',
    'ComparisonMetric',
    'ProcessingJob',
    'get_database_manager',
    'init_database',
    
    # Object Storage
    'ObjectStorageManager',
    'get_object_storage_manager',
    
    # Storage Service
    'StorageService',
    'get_storage_service',
    
    # Security
    'EncryptionManager',
    'AccessControlManager',
    'TLSConfig',
    'AuditLogger',
    'UserRole',
    'get_encryption_manager',
    'get_access_control_manager',
    'get_audit_logger'
]
