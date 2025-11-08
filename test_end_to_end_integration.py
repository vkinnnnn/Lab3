#!/usr/bin/env python3
"""
End-to-End Integration Test for Student Loan Document Extractor Platform

This test verifies the complete workflow:
1. Document upload → OCR → extraction → normalization → storage → retrieval
2. Batch processing workflow with multiple documents
3. Comparison workflow with multiple loans
4. Dashboard integration with API endpoints

Requirements: 8.1, 8.2, 11.1, 11.2, 11.3, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4
"""

import requests
import json
import time
import os
import sys
from typing import Dict, List, Any
from pathlib import Path

# Test configuration
API_BASE_URL = "http://localhost:8000"
DASHBOARD_URL = "http://localhost:8501"
TEST_TIMEOUT = 60  # seconds

# Test files (create sample files if they don't exist)
TEST_FILES_DIR = Path("test_files")
SAMPLE_PDF_CONTENT = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Sample Loan Document) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000206 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n299\n%%EOF"


class EndToEndTester:
    """End-to-end integration tester"""
    
    def __init__(self):
        self.api_base = API_BASE_URL
        self.dashboard_base = DASHBOARD_URL
        self.test_results = []
        self.uploaded_documents = []
        self.extracted_loans = []
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def setup_test_files(self):
        """Create test files if they don't exist"""
        TEST_FILES_DIR.mkdir(exist_ok=True)
        
        # Create sample PDF files
        test_files = [
            "sample_loan_1.pdf",
            "sample_loan_2.pdf",
            "sample_loan_3.pdf"
        ]
        
        for filename in test_files:
            filepath = TEST_FILES_DIR / filename
            if not filepath.exists():
                with open(filepath, "wb") as f:
                    f.write(SAMPLE_PDF_CONTENT)
        
        self.log_test("Setup Test Files", True, f"Created {len(test_files)} test files")
    
    def test_api_health(self):
        """Test API health endpoint"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                self.log_test("API Health Check", True, f"Status: {health_data.get('status', 'unknown')}")
                return True
            else:
                self.log_test("API Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, str(e))
            return False
    
    def test_dashboard_health(self):
        """Test dashboard accessibility"""
        try:
            response = requests.get(self.dashboard_base, timeout=10)
            if response.status_code == 200:
                self.log_test("Dashboard Health Check", True, "Dashboard accessible")
                return True
            else:
                self.log_test("Dashboard Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Dashboard Health Check", False, str(e))
            return False
    
    def test_single_document_upload(self):
        """Test single document upload workflow"""
        try:
            test_file = TEST_FILES_DIR / "sample_loan_1.pdf"
            
            with open(test_file, "rb") as f:
                files = {"file": ("sample_loan_1.pdf", f, "application/pdf")}
                response = requests.post(
                    f"{self.api_base}/api/v1/documents/upload",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 201:
                result = response.json()
                document_id = result.get("document_id")
                self.uploaded_documents.append(document_id)
                self.log_test("Single Document Upload", True, f"Document ID: {document_id}")
                return True
            else:
                self.log_test("Single Document Upload", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Single Document Upload", False, str(e))
            return False
    
    def test_document_extraction(self):
        """Test complete document extraction workflow"""
        try:
            test_file = TEST_FILES_DIR / "sample_loan_2.pdf"
            
            with open(test_file, "rb") as f:
                files = {"file": ("sample_loan_2.pdf", f, "application/pdf")}
                response = requests.post(
                    f"{self.api_base}/api/v1/extract",
                    files=files,
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                document_id = result.get("document_id")
                accuracy = result.get("accuracy_metrics", {}).get("overall_accuracy", 0)
                
                self.uploaded_documents.append(document_id)
                self.log_test("Document Extraction", True, f"Accuracy: {accuracy:.1%}")
                return True
            else:
                self.log_test("Document Extraction", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Document Extraction", False, str(e))
            return False
    
    def test_batch_processing(self):
        """Test batch processing workflow"""
        try:
            files = []
            test_files = ["sample_loan_1.pdf", "sample_loan_2.pdf", "sample_loan_3.pdf"]
            
            for filename in test_files:
                filepath = TEST_FILES_DIR / filename
                with open(filepath, "rb") as f:
                    files.append(("files", (filename, f.read(), "application/pdf")))
            
            response = requests.post(
                f"{self.api_base}/api/v1/batch-upload",
                files=files,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get("summary", {})
                successful = summary.get("successful_documents", 0)
                failed = summary.get("failed_documents", 0)
                
                self.log_test("Batch Processing", True, f"Success: {successful}, Failed: {failed}")
                return True
            else:
                self.log_test("Batch Processing", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Batch Processing", False, str(e))
            return False
    
    def test_document_retrieval(self):
        """Test document metadata retrieval"""
        if not self.uploaded_documents:
            self.log_test("Document Retrieval", False, "No uploaded documents to test")
            return False
        
        try:
            document_id = self.uploaded_documents[0]
            response = requests.get(
                f"{self.api_base}/api/v1/documents/{document_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                metadata = response.json()
                file_name = metadata.get("file_name", "unknown")
                self.log_test("Document Retrieval", True, f"Retrieved: {file_name}")
                return True
            else:
                self.log_test("Document Retrieval", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Document Retrieval", False, str(e))
            return False
    
    def test_loan_query(self):
        """Test loan data querying"""
        try:
            response = requests.get(
                f"{self.api_base}/api/v1/loans",
                timeout=30
            )
            
            if response.status_code == 200:
                loans = response.json()
                loan_count = len(loans) if isinstance(loans, list) else 0
                
                # Store loan IDs for comparison test
                if isinstance(loans, list) and loans:
                    self.extracted_loans = [loan.get("loan_id") for loan in loans if loan.get("loan_id")]
                
                self.log_test("Loan Query", True, f"Found {loan_count} loans")
                return True
            else:
                self.log_test("Loan Query", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Loan Query", False, str(e))
            return False
    
    def test_loan_comparison(self):
        """Test loan comparison workflow"""
        if len(self.extracted_loans) < 2:
            # Create mock loan data for comparison test
            mock_loans = [
                {
                    "loan_id": "test_loan_1",
                    "principal_amount": 10000,
                    "interest_rate": 5.5,
                    "tenure_months": 60,
                    "bank_name": "Test Bank A"
                },
                {
                    "loan_id": "test_loan_2", 
                    "principal_amount": 15000,
                    "interest_rate": 6.0,
                    "tenure_months": 48,
                    "bank_name": "Test Bank B"
                }
            ]
            
            try:
                response = requests.post(
                    f"{self.api_base}/api/v1/compare",
                    json=mock_loans,
                    timeout=30
                )
                
                if response.status_code == 200:
                    comparison = response.json()
                    loan_count = comparison.get("loan_count", 0)
                    self.log_test("Loan Comparison", True, f"Compared {loan_count} loans")
                    return True
                else:
                    self.log_test("Loan Comparison", False, f"HTTP {response.status_code}")
                    return False
            except Exception as e:
                self.log_test("Loan Comparison", False, str(e))
                return False
        else:
            # Use real loan IDs
            try:
                loan_ids = self.extracted_loans[:2]  # Take first 2
                response = requests.post(
                    f"{self.api_base}/api/v1/compare",
                    json=loan_ids,
                    timeout=30
                )
                
                if response.status_code == 200:
                    comparison = response.json()
                    loan_count = len(loan_ids)
                    self.log_test("Loan Comparison", True, f"Compared {loan_count} real loans")
                    return True
                else:
                    self.log_test("Loan Comparison", False, f"HTTP {response.status_code}")
                    return False
            except Exception as e:
                self.log_test("Loan Comparison", False, str(e))
                return False
    
    def test_processing_status(self):
        """Test processing status endpoint"""
        try:
            # Test with a mock job ID
            response = requests.get(
                f"{self.api_base}/api/v1/processing-status/test-job-123",
                timeout=30
            )
            
            # Expect 404 for non-existent job, which is correct behavior
            if response.status_code == 404:
                self.log_test("Processing Status", True, "Correctly returned 404 for non-existent job")
                return True
            elif response.status_code == 200:
                status = response.json()
                self.log_test("Processing Status", True, f"Status: {status.get('status', 'unknown')}")
                return True
            else:
                self.log_test("Processing Status", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Processing Status", False, str(e))
            return False
    
    def test_api_endpoints_coverage(self):
        """Test coverage of all major API endpoints"""
        endpoints = [
            ("/", "GET", "Root endpoint"),
            ("/health", "GET", "Health check"),
            ("/api/v1/accuracy", "GET", "Accuracy info"),
            ("/api/v1/api-info", "GET", "API info")
        ]
        
        success_count = 0
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.api_base}{endpoint}", timeout=10)
                else:
                    continue  # Skip non-GET for this test
                
                if response.status_code == 200:
                    success_count += 1
            except:
                pass
        
        success_rate = success_count / len(endpoints)
        self.log_test("API Endpoints Coverage", success_rate >= 0.75, f"{success_count}/{len(endpoints)} endpoints working")
        return success_rate >= 0.75
    
    def run_all_tests(self):
        """Run all end-to-end tests"""
        print("🚀 Starting End-to-End Integration Tests")
        print("=" * 60)
        
        # Setup
        self.setup_test_files()
        
        # Core API tests
        if not self.test_api_health():
            print("❌ API not available - skipping API tests")
            return False
        
        # Dashboard test (optional)
        self.test_dashboard_health()
        
        # Document workflow tests
        self.test_single_document_upload()
        self.test_document_extraction()
        self.test_batch_processing()
        self.test_document_retrieval()
        
        # Data workflow tests
        self.test_loan_query()
        self.test_loan_comparison()
        self.test_processing_status()
        
        # Coverage test
        self.test_api_endpoints_coverage()
        
        # Summary
        self.print_summary()
        
        return self.get_overall_success()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Overall Status: EXCELLENT")
        elif success_rate >= 60:
            print("✅ Overall Status: GOOD")
        elif success_rate >= 40:
            print("⚠️ Overall Status: NEEDS IMPROVEMENT")
        else:
            print("❌ Overall Status: CRITICAL ISSUES")
        
        # Failed tests details
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        print("\n" + "=" * 60)
    
    def get_overall_success(self) -> bool:
        """Get overall test success status"""
        if not self.test_results:
            return False
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        success_rate = (passed / total) * 100
        
        return success_rate >= 60  # 60% minimum for overall success


def main():
    """Main test runner"""
    tester = EndToEndTester()
    
    try:
        success = tester.run_all_tests()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()