"""
Data masking and anonymization for sensitive user information
"""
import re
import hashlib
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class DataMasker:
    """
    Mask and anonymize sensitive user data before storage or display
    """
    
    def __init__(self, mask_level: str = "standard"):
        """
        Initialize data masker
        
        Args:
            mask_level: "minimal", "standard", or "strict"
        """
        self.mask_level = mask_level
        self.masked_fields = set()
    
    def mask_document_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mask sensitive information in extracted document data
        
        Args:
            data: Extracted document data
            
        Returns:
            Data with sensitive information masked
        """
        try:
            logger.info(f"Masking data with level: {self.mask_level}")
            
            # Create a copy to avoid modifying original
            masked_data = data.copy()
            
            # Mask different types of sensitive information
            masked_data = self._mask_personal_info(masked_data)
            masked_data = self._mask_financial_info(masked_data)
            masked_data = self._mask_contact_info(masked_data)
            masked_data = self._mask_identification(masked_data)
            masked_data = self._mask_text_content(masked_data)
            
            # Add masking metadata
            masked_data["_data_masking"] = {
                "masked": True,
                "mask_level": self.mask_level,
                "masked_fields": list(self.masked_fields),
                "note": "Sensitive information has been masked for privacy"
            }
            
            logger.info(f"Masked {len(self.masked_fields)} fields")
            return masked_data
            
        except Exception as e:
            logger.error(f"Error masking data: {str(e)}")
            return data
    
    def _mask_personal_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask personal information like names, addresses"""
        
        # Mask borrower/co-signer names
        if "borrower_name" in data:
            data["borrower_name"] = self._mask_name(data["borrower_name"])
            self.masked_fields.add("borrower_name")
        
        if "co_signer" in data and isinstance(data["co_signer"], dict):
            if "name" in data["co_signer"]:
                data["co_signer"]["name"] = self._mask_name(data["co_signer"]["name"])
                self.masked_fields.add("co_signer.name")
        
        # Mask addresses
        if "address" in data:
            data["address"] = self._mask_address(data["address"])
            self.masked_fields.add("address")
        
        if "borrower_address" in data:
            data["borrower_address"] = self._mask_address(data["borrower_address"])
            self.masked_fields.add("borrower_address")
        
        # Recursively mask in nested structures
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._mask_personal_info(value)
            elif isinstance(value, list):
                data[key] = [self._mask_personal_info(item) if isinstance(item, dict) else item for item in value]
        
        return data
    
    def _mask_financial_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive financial information"""
        
        if self.mask_level == "strict":
            # In strict mode, mask account numbers and specific amounts
            if "account_number" in data:
                data["account_number"] = self._mask_account_number(data["account_number"])
                self.masked_fields.add("account_number")
            
            if "bank_account" in data:
                data["bank_account"] = self._mask_account_number(data["bank_account"])
                self.masked_fields.add("bank_account")
            
            # Mask loan account numbers
            if "loan_account_number" in data:
                data["loan_account_number"] = self._mask_account_number(data["loan_account_number"])
                self.masked_fields.add("loan_account_number")
        
        return data
    
    def _mask_contact_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask contact information"""
        
        # Mask email addresses
        for key in list(data.keys()):
            if isinstance(data[key], str):
                if self._is_email(data[key]):
                    data[key] = self._mask_email(data[key])
                    self.masked_fields.add(key)
                elif self._is_phone(data[key]):
                    data[key] = self._mask_phone(data[key])
                    self.masked_fields.add(key)
            elif isinstance(data[key], dict):
                data[key] = self._mask_contact_info(data[key])
            elif isinstance(data[key], list):
                data[key] = [self._mask_contact_info(item) if isinstance(item, dict) else 
                            (self._mask_email(item) if isinstance(item, str) and self._is_email(item) else
                             self._mask_phone(item) if isinstance(item, str) and self._is_phone(item) else item)
                            for item in data[key]]
        
        # Mask specific contact fields
        if "contact_information" in data and isinstance(data["contact_information"], dict):
            contact = data["contact_information"]
            
            if "emails" in contact and isinstance(contact["emails"], list):
                contact["emails"] = [self._mask_email(email) for email in contact["emails"]]
                self.masked_fields.add("contact_information.emails")
            
            if "phone_numbers" in contact and isinstance(contact["phone_numbers"], list):
                contact["phone_numbers"] = [self._mask_phone(phone) for phone in contact["phone_numbers"]]
                self.masked_fields.add("contact_information.phone_numbers")
        
        return data
    
    def _mask_identification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask identification numbers (SSN, ID numbers, etc.)"""
        
        # Mask SSN
        if "ssn" in data:
            data["ssn"] = self._mask_ssn(data["ssn"])
            self.masked_fields.add("ssn")
        
        if "social_security_number" in data:
            data["social_security_number"] = self._mask_ssn(data["social_security_number"])
            self.masked_fields.add("social_security_number")
        
        # Mask ID numbers
        if "id_number" in data:
            data["id_number"] = self._mask_id(data["id_number"])
            self.masked_fields.add("id_number")
        
        if "driver_license" in data:
            data["driver_license"] = self._mask_id(data["driver_license"])
            self.masked_fields.add("driver_license")
        
        return data
    
    def _mask_text_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive information in text fields"""
        
        text_fields = ["raw_text_preview", "document_text", "extracted_text", "full_text"]
        
        for field in text_fields:
            if field in data and isinstance(data[field], str):
                original_text = data[field]
                masked_text = original_text
                
                # Mask emails in text
                masked_text = re.sub(
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    lambda m: self._mask_email(m.group()),
                    masked_text
                )
                
                # Mask phone numbers in text
                masked_text = re.sub(
                    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                    lambda m: self._mask_phone(m.group()),
                    masked_text
                )
                
                # Mask SSN patterns in text
                masked_text = re.sub(
                    r'\b\d{3}-\d{2}-\d{4}\b',
                    'XXX-XX-XXXX',
                    masked_text
                )
                
                if masked_text != original_text:
                    data[field] = masked_text
                    self.masked_fields.add(field)
        
        return data
    
    # Masking helper methods
    
    def _mask_name(self, name: str) -> str:
        """Mask a person's name"""
        if not name or not isinstance(name, str):
            return name
        
        if self.mask_level == "minimal":
            # Keep first name, mask last name
            parts = name.split()
            if len(parts) > 1:
                return f"{parts[0]} {'*' * len(parts[-1])}"
            return name
        
        elif self.mask_level == "standard":
            # Keep first letter of first name, mask rest
            parts = name.split()
            if len(parts) > 0:
                return f"{parts[0][0]}*** {'*' * len(' '.join(parts[1:]))}"
            return "***"
        
        else:  # strict
            # Mask everything
            return "*" * len(name)
    
    def _mask_email(self, email: str) -> str:
        """Mask email address"""
        if not email or '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        
        if self.mask_level == "minimal":
            # Show first 2 chars of local part
            masked_local = local[:2] + '*' * (len(local) - 2) if len(local) > 2 else '**'
            return f"{masked_local}@{domain}"
        
        elif self.mask_level == "standard":
            # Show first char of local part, mask domain partially
            masked_local = local[0] + '*' * (len(local) - 1) if len(local) > 0 else '*'
            domain_parts = domain.split('.')
            masked_domain = '*' * len(domain_parts[0]) + '.' + '.'.join(domain_parts[1:])
            return f"{masked_local}@{masked_domain}"
        
        else:  # strict
            return "***@***.***"
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone number"""
        if not phone:
            return phone
        
        # Remove non-digits
        digits = re.sub(r'\D', '', phone)
        
        if self.mask_level == "minimal":
            # Show last 4 digits
            if len(digits) >= 4:
                return f"***-***-{digits[-4:]}"
            return "***-****"
        
        elif self.mask_level == "standard":
            # Show area code, mask rest
            if len(digits) >= 10:
                return f"({digits[:3]}) ***-****"
            return "***-***-****"
        
        else:  # strict
            return "***-***-****"
    
    def _mask_address(self, address: str) -> str:
        """Mask physical address"""
        if not address or not isinstance(address, str):
            return address
        
        if self.mask_level == "minimal":
            # Keep city and state, mask street
            parts = address.split(',')
            if len(parts) > 1:
                return f"*** {', '.join(parts[-2:])}"
            return "*** [Address Masked]"
        
        elif self.mask_level == "standard":
            # Keep only state/country
            parts = address.split(',')
            if len(parts) > 0:
                return f"*** {parts[-1].strip()}"
            return "[Address Masked]"
        
        else:  # strict
            return "[Address Masked]"
    
    def _mask_account_number(self, account: str) -> str:
        """Mask account number"""
        if not account:
            return account
        
        digits = re.sub(r'\D', '', str(account))
        
        if self.mask_level == "minimal" and len(digits) >= 4:
            return f"****{digits[-4:]}"
        else:
            return "****" + "*" * min(4, len(digits))
    
    def _mask_ssn(self, ssn: str) -> str:
        """Mask Social Security Number"""
        return "XXX-XX-XXXX"
    
    def _mask_id(self, id_num: str) -> str:
        """Mask ID number"""
        if not id_num:
            return id_num
        return "*" * len(str(id_num))
    
    # Detection helper methods
    
    def _is_email(self, text: str) -> bool:
        """Check if text is an email"""
        return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', text))
    
    def _is_phone(self, text: str) -> bool:
        """Check if text is a phone number"""
        digits = re.sub(r'\D', '', text)
        return len(digits) >= 10 and len(digits) <= 15


def mask_sensitive_data(data: Dict[str, Any], mask_level: str = "standard") -> Dict[str, Any]:
    """
    Convenience function to mask sensitive data
    
    Args:
        data: Data to mask
        mask_level: "minimal", "standard", or "strict"
        
    Returns:
        Masked data
    """
    masker = DataMasker(mask_level=mask_level)
    return masker.mask_document_data(data)
