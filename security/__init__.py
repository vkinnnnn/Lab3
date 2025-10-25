"""
Security module for data protection and privacy
"""
from .data_masking import DataMasker, mask_sensitive_data

__all__ = ['DataMasker', 'mask_sensitive_data']
