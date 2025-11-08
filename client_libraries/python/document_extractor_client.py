"""
Document Extractor API Client
Easy-to-use Python client for your friends
"""
import requests
from typing import Optional, Dict, Any
import json
from pathlib import Path


class DocumentExtractorClient:
    """
    Simple client for Document Extraction API
    
    Usage:
        client = DocumentExtractorClient(api_key="your-key")
        result = client.extract("document.pdf")
        print(result['complete_text']['merged_text'])
    """
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000/api/v1"):
        """
        Initialize client
        
        Args:
            api_key: Your API key
            base_url: API base URL (default: localhost)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {"X-API-Key": api_key}
        self.last_usage = None
    
    def _make_request(self, endpoint: str, files: Dict = None, data: Dict = None) -> Dict:
        """Make API request and handle errors"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.post(url, headers=self.headers, files=files, data=data)
            
            # Store rate limit info from headers
            if 'X-RateLimit-Remaining' in response.headers:
                self.last_usage = {
                    'limit': response.headers.get('X-RateLimit-Limit'),
                    'remaining': response.headers.get('X-RateLimit-Remaining'),
                    'reset': response.headers.get('X-RateLimit-Reset')
                }
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise Exception("Invalid API key")
            elif response.status_code == 429:
                error_data = response.json()
                raise Exception(f"Rate limit exceeded: {error_data.get('detail', {}).get('message', 'Too many requests')}")
            else:
                raise Exception(f"API Error {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Connection error: {str(e)}")
    
    def extract(self, file_path: str, smart: bool = False) -> Dict[str, Any]:
        """
        Extract document
        
        Args:
            file_path: Path to document file
            smart: Use smart extraction (auto-detects handwriting & language)
            
        Returns:
            Complete extraction result with all data
        """
        endpoint = "/extract/smart" if smart else "/extract"
        
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f)}
            result = self._make_request(endpoint, files=files)
        
        # Print usage info if available
        if 'api_usage' in result:
            self._print_usage(result['api_usage'])
        
        return result
    
    def get_text(self, file_path: str, smart: bool = False) -> str:
        """
        Get just the extracted text
        
        Args:
            file_path: Path to document file
            smart: Use smart extraction
            
        Returns:
            Extracted text as string
        """
        result = self.extract(file_path, smart)
        return result['complete_text']['merged_text']
    
    def get_numbers(self, file_path: str, smart: bool = False) -> list:
        """
        Get all numbers from document
        
        Args:
            file_path: Path to document file
            smart: Use smart extraction
            
        Returns:
            List of numbers with types
        """
        result = self.extract(file_path, smart)
        return result['all_numbers']
    
    def get_tables(self, file_path: str, smart: bool = False) -> list:
        """
        Get all tables from document
        
        Args:
            file_path: Path to document file
            smart: Use smart extraction
            
        Returns:
            List of tables with headers and data
        """
        result = self.extract(file_path, smart)
        return result['all_tables']
    
    def get_form_fields(self, file_path: str, smart: bool = False) -> Dict[str, str]:
        """
        Get form fields as dictionary
        
        Args:
            file_path: Path to document file
            smart: Use smart extraction
            
        Returns:
            Dictionary of field_name: field_value
        """
        result = self.extract(file_path, smart)
        fields = {}
        for field in result.get('all_form_fields', []):
            fields[field['field_name']] = field['field_value']
        return fields
    
    def get_usage(self) -> Dict[str, Any]:
        """
        Get current API usage statistics
        
        Returns:
            Usage information with visual indicator
        """
        url = f"{self.base_url}/usage"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            usage = response.json()
            self._print_usage_detailed(usage)
            return usage
        else:
            raise Exception(f"Failed to get usage: {response.text}")
    
    def _print_usage(self, usage: Dict):
        """Print simple usage info"""
        print(f"\n📊 API Usage:")
        print(f"   Used: {usage['requests_used']}/{usage['daily_limit']}")
        print(f"   Remaining: {usage['requests_remaining']}")
        print(f"   Tier: {usage['tier']}")
    
    def _print_usage_detailed(self, usage: Dict):
        """Print detailed usage with visual indicator"""
        print(f"\n{'='*60}")
        print(f"📊 API Usage for {usage['user']}")
        print(f"{'='*60}")
        print(f"Tier: {usage['tier'].upper()}")
        print(f"\nDaily Limit: {usage['usage']['limit']} requests")
        print(f"Used: {usage['usage']['used']} requests")
        print(f"Remaining: {usage['usage']['remaining']} requests")
        print(f"\nProgress: {usage['visual']['indicator']}")
        print(f"Status: {usage['usage']['status']}")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = DocumentExtractorClient(
        api_key="demo-key-12345",
        base_url="http://localhost:8000/api/v1"
    )
    
    # Check usage
    print("Checking API usage...")
    client.get_usage()
    
    # Extract document
    print("\nExtracting document...")
    result = client.extract("sample_document.pdf")
    
    # Get specific data
    text = result['complete_text']['merged_text']
    numbers = result['all_numbers']
    tables = result['all_tables']
    
    print(f"\nExtracted {len(text)} characters")
    print(f"Found {len(numbers)} numbers")
    print(f"Found {len(tables)} tables")
    
    # Check usage again
    print("\nUpdated usage:")
    client.get_usage()
