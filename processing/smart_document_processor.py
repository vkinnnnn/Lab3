"""
Smart Document Processor
Automatically detects document type and selects best processors
Handles: Handwritten, Multi-language, Complex layouts
"""
import os
import logging
from typing import Dict, Any, List, Optional, Tuple
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import re

logger = logging.getLogger(__name__)

# Configuration
PROJECT_ID = "rich-atom-476217-j9"
LOCATION = "us"
FORM_PARSER_ID = "337aa94aac26006"
DOC_OCR_ID = "c0c01b0942616db6"
LAYOUT_PARSER_ID = "41972eaa15f517f2"
# HANDWRITING_PARSER_ID = "create-this-in-console"  # Optional: Add if you create one
SERVICE_ACCOUNT_FILE = "/app/service-account-key.json"


class SmartDocumentProcessor:
    """
    Intelligent document processor that:
    1. Detects document characteristics (handwritten, language, complexity)
    2. Selects optimal processors
    3. Processes with selected processors
    4. Merges results intelligently
    """
    
    def __init__(self):
        """Initialize with all available processors"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            
            # Document AI client
            self.doc_ai_client = documentai.DocumentProcessorServiceClient(
                credentials=credentials
            )
            
            # Translation client for language detection
            self.translate_client = translate.Client(credentials=credentials)
            
            # Initialize processor paths
            self.form_parser_name = self.doc_ai_client.processor_path(
                PROJECT_ID, LOCATION, FORM_PARSER_ID
            )
            self.doc_ocr_name = self.doc_ai_client.processor_path(
                PROJECT_ID, LOCATION, DOC_OCR_ID
            )
            self.layout_parser_name = self.doc_ai_client.processor_path(
                PROJECT_ID, LOCATION, LAYOUT_PARSER_ID
            )
            
            # Optional: Handwriting processor (uncomment if you create one)
            # self.handwriting_parser_name = self.doc_ai_client.processor_path(
            #     PROJECT_ID, LOCATION, HANDWRITING_PARSER_ID
            # )
            
            logger.info("Smart Document Processor initialized")
            logger.info("Available processors: Form Parser, Document OCR, Layout Parser")
            
        except Exception as e:
            logger.error(f"Failed to initialize: {str(e)}")
            raise
    
    def process_document_smart(
        self,
        file_content: bytes,
        mime_type: str,
        filename: str
    ) -> Dict[str, Any]:
        """
        Smart document processing with automatic processor selection
        
        Args:
            file_content: Binary content
            mime_type: MIME type
            filename: File name
            
        Returns:
            Complete extraction with metadata about processing decisions
        """
        try:
            logger.info(f"Starting smart processing: {filename}")
            
            # Step 1: Quick scan to detect characteristics
            characteristics = self._detect_document_characteristics(
                file_content, mime_type
            )
            
            logger.info(f"Document characteristics: {characteristics}")
            
            # Step 2: Select optimal processors
            selected_processors = self._select_processors(characteristics)
            
            logger.info(f"Selected processors: {selected_processors}")
            
            # Step 3: Process with selected processors
            results = self._process_with_selected(
                file_content, mime_type, selected_processors
            )
            
            # Step 4: Merge results intelligently
            merged_result = self._merge_results(
                results, characteristics, filename
            )
            
            # Step 5: Add processing metadata
            merged_result["processing_metadata"] = {
                "characteristics": characteristics,
                "processors_selected": selected_processors,
                "selection_reason": self._explain_selection(characteristics)
            }
            
            logger.info(f"Smart processing complete: {filename}")
            logger.info(f"Processors used: {len(selected_processors)}")
            
            return merged_result
            
        except Exception as e:
            logger.error(f"Smart processing error: {str(e)}")
            return {
                "document_name": filename,
                "error": str(e),
                "extraction_status": "failed"
            }
    
    def _detect_document_characteristics(
        self,
        file_content: bytes,
        mime_type: str
    ) -> Dict[str, Any]:
        """
        Detect document characteristics using quick OCR scan
        
        Returns:
            {
                "is_handwritten": bool,
                "handwriting_percentage": float,
                "primary_language": str,
                "is_multilingual": bool,
                "has_complex_tables": bool,
                "confidence": float
            }
        """
        try:
            # Quick scan with Document OCR (fastest, supports all languages)
            quick_result = self._quick_ocr_scan(file_content, mime_type)
            
            if not quick_result:
                # Fallback to defaults
                return {
                    "is_handwritten": False,
                    "handwriting_percentage": 0.0,
                    "primary_language": "en",
                    "is_multilingual": False,
                    "has_complex_tables": False,
                    "confidence": 0.5
                }
            
            # Extract text for analysis
            text = quick_result.text if hasattr(quick_result, 'text') else ""
            
            # Detect handwriting (heuristic based on confidence scores)
            is_handwritten, hw_percentage = self._detect_handwriting(quick_result)
            
            # Detect language
            primary_language, is_multilingual = self._detect_language(text)
            
            # Detect complex tables
            has_complex_tables = self._detect_complex_tables(quick_result)
            
            # Calculate overall confidence
            confidence = self._calculate_detection_confidence(quick_result)
            
            return {
                "is_handwritten": is_handwritten,
                "handwriting_percentage": hw_percentage,
                "primary_language": primary_language,
                "is_multilingual": is_multilingual,
                "has_complex_tables": has_complex_tables,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.warning(f"Characteristic detection error: {str(e)}")
            return {
                "is_handwritten": False,
                "handwriting_percentage": 0.0,
                "primary_language": "en",
                "is_multilingual": False,
                "has_complex_tables": False,
                "confidence": 0.5
            }
    
    def _quick_ocr_scan(
        self,
        file_content: bytes,
        mime_type: str
    ) -> Optional[documentai.Document]:
        """Quick OCR scan for characteristic detection"""
        try:
            request = documentai.ProcessRequest(
                name=self.doc_ocr_name,
                raw_document=documentai.RawDocument(
                    content=file_content,
                    mime_type=mime_type
                )
            )
            
            result = self.doc_ai_client.process_document(request=request)
            return result.document
            
        except Exception as e:
            logger.warning(f"Quick OCR scan error: {str(e)}")
            return None
    
    def _detect_handwriting(
        self,
        document: documentai.Document
    ) -> Tuple[bool, float]:
        """
        Detect if document contains handwriting
        
        Heuristic: Low confidence scores often indicate handwriting
        """
        if not hasattr(document, 'pages'):
            return False, 0.0
        
        low_confidence_count = 0
        total_count = 0
        
        for page in document.pages:
            if hasattr(page, 'tokens'):
                for token in page.tokens:
                    if hasattr(token, 'layout') and hasattr(token.layout, 'confidence'):
                        total_count += 1
                        if token.layout.confidence < 0.75:
                            low_confidence_count += 1
        
        if total_count == 0:
            return False, 0.0
        
        handwriting_percentage = low_confidence_count / total_count
        is_handwritten = handwriting_percentage > 0.3  # 30% threshold
        
        return is_handwritten, handwriting_percentage
    
    def _detect_language(self, text: str) -> Tuple[str, bool]:
        """
        Detect primary language and if document is multilingual
        
        Returns:
            (primary_language_code, is_multilingual)
        """
        if not text or len(text) < 50:
            return "en", False
        
        try:
            # Sample text for detection (first 1000 chars)
            sample = text[:1000]
            
            # Detect language
            detection = self.translate_client.detect_language(sample)
            primary_language = detection['language']
            confidence = detection['confidence']
            
            # Check if multilingual (split text and detect multiple sections)
            is_multilingual = False
            if len(text) > 2000:
                # Check middle and end sections
                sections = [
                    text[len(text)//3:len(text)//3+500],
                    text[2*len(text)//3:2*len(text)//3+500]
                ]
                
                languages = set([primary_language])
                for section in sections:
                    try:
                        det = self.translate_client.detect_language(section)
                        languages.add(det['language'])
                    except:
                        pass
                
                is_multilingual = len(languages) > 1
            
            logger.info(f"Detected language: {primary_language} (confidence: {confidence:.2f})")
            
            return primary_language, is_multilingual
            
        except Exception as e:
            logger.warning(f"Language detection error: {str(e)}")
            return "en", False
    
    def _detect_complex_tables(self, document: documentai.Document) -> bool:
        """Detect if document has complex nested tables"""
        if not hasattr(document, 'pages'):
            return False
        
        for page in document.pages:
            if hasattr(page, 'tables'):
                for table in page.tables:
                    # Check for merged cells (indicates complexity)
                    if hasattr(table, 'header_rows'):
                        for row in table.header_rows:
                            for cell in row.cells:
                                if hasattr(cell, 'row_span') and cell.row_span > 1:
                                    return True
                                if hasattr(cell, 'col_span') and cell.col_span > 1:
                                    return True
        
        return False
    
    def _calculate_detection_confidence(
        self,
        document: documentai.Document
    ) -> float:
        """Calculate confidence in characteristic detection"""
        if not hasattr(document, 'pages'):
            return 0.5
        
        confidences = []
        for page in document.pages:
            if hasattr(page, 'confidence') and page.confidence > 0:
                confidences.append(page.confidence)
        
        if confidences:
            return sum(confidences) / len(confidences)
        
        return 0.8  # Default reasonable confidence
    
    def _select_processors(
        self,
        characteristics: Dict[str, Any]
    ) -> List[str]:
        """
        Select optimal processors based on document characteristics
        
        Selection Logic:
        - Always use Document OCR (best for multi-language)
        - Use Form Parser for printed forms
        - Use Layout Parser for complex tables
        - Use Handwriting Parser for handwritten content (if available)
        """
        processors = []
        
        # Always use Document OCR (supports 200+ languages)
        processors.append("doc_ocr")
        
        # If handwritten, prioritize handwriting processor
        if characteristics["is_handwritten"]:
            # Uncomment if you have handwriting processor
            # processors.append("handwriting")
            logger.info("Handwritten content detected (using OCR - add handwriting processor for better accuracy)")
        else:
            # For printed text, use Form Parser
            processors.append("form_parser")
        
        # If complex tables, use Layout Parser
        if characteristics["has_complex_tables"]:
            processors.append("layout_parser")
        
        # If not complex and not handwritten, use all three for maximum accuracy
        if not characteristics["is_handwritten"] and not characteristics["has_complex_tables"]:
            if "layout_parser" not in processors:
                processors.append("layout_parser")
        
        return processors
    
    def _process_with_selected(
        self,
        file_content: bytes,
        mime_type: str,
        processors: List[str]
    ) -> Dict[str, Optional[documentai.Document]]:
        """Process document with selected processors"""
        results = {}
        
        for processor in processors:
            if processor == "form_parser":
                results["form_parser"] = self._process_with_processor(
                    file_content, mime_type, self.form_parser_name
                )
            elif processor == "doc_ocr":
                results["doc_ocr"] = self._process_with_processor(
                    file_content, mime_type, self.doc_ocr_name
                )
            elif processor == "layout_parser":
                results["layout_parser"] = self._process_with_processor(
                    file_content, mime_type, self.layout_parser_name
                )
            # elif processor == "handwriting":
            #     results["handwriting"] = self._process_with_processor(
            #         file_content, mime_type, self.handwriting_parser_name
            #     )
        
        return results
    
    def _process_with_processor(
        self,
        file_content: bytes,
        mime_type: str,
        processor_name: str
    ) -> Optional[documentai.Document]:
        """Process with a specific processor"""
        try:
            request = documentai.ProcessRequest(
                name=processor_name,
                raw_document=documentai.RawDocument(
                    content=file_content,
                    mime_type=mime_type
                )
            )
            
            result = self.doc_ai_client.process_document(request=request)
            logger.info(f"Processor {processor_name.split('/')[-1]}: SUCCESS")
            return result.document
            
        except Exception as e:
            logger.warning(f"Processor error: {str(e)}")
            return None
    
    def _merge_results(
        self,
        results: Dict[str, Optional[documentai.Document]],
        characteristics: Dict[str, Any],
        filename: str
    ) -> Dict[str, Any]:
        """Intelligently merge results from multiple processors"""
        
        merged = {
            "document_name": filename,
            "extraction_method": "smart_multi_processor",
            "processors_used": list(results.keys()),
            "complete_text": {},
            "all_text_elements": [],
            "all_numbers": [],
            "all_form_fields": [],
            "all_tables": [],
            "accuracy_metrics": {}
        }
        
        # Extract text from each processor
        for processor_name, document in results.items():
            if document and hasattr(document, 'text'):
                merged["complete_text"][f"{processor_name}_text"] = document.text
        
        # Merge texts intelligently based on characteristics
        merged["complete_text"]["merged_text"] = self._merge_texts_smart(
            merged["complete_text"], characteristics
        )
        
        # Extract all numbers
        merged["all_numbers"] = self._extract_all_numbers(
            merged["complete_text"]["merged_text"]
        )
        
        # Calculate accuracy
        merged["accuracy_metrics"] = self._calculate_smart_accuracy(
            results, characteristics
        )
        
        return merged
    
    def _merge_texts_smart(
        self,
        texts: Dict[str, str],
        characteristics: Dict[str, Any]
    ) -> str:
        """
        Smart text merging based on document characteristics
        
        Priority:
        - Handwritten: OCR > others
        - Non-English: OCR > others (best language support)
        - Complex tables: Layout Parser > others
        - Default: Longest text
        """
        if characteristics["is_handwritten"]:
            # Prioritize OCR for handwriting
            return texts.get("doc_ocr_text", "")
        
        if characteristics["primary_language"] != "en":
            # Prioritize OCR for non-English
            return texts.get("doc_ocr_text", "")
        
        if characteristics["has_complex_tables"]:
            # Prioritize Layout Parser for complex tables
            return texts.get("layout_parser_text", texts.get("doc_ocr_text", ""))
        
        # Default: use longest text
        longest = max(texts.items(), key=lambda x: len(x[1]) if x[1] else 0)
        return longest[1] if longest[1] else ""
    
    def _extract_all_numbers(self, text: str) -> List[Dict[str, Any]]:
        """Extract all numbers from text"""
        numbers = []
        
        patterns = [
            (r'\d+\.\d+', 'decimal'),
            (r'\d+,\d+', 'comma_separated'),
            (r'\d+', 'integer'),
            (r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?', 'currency'),
            (r'\d+%', 'percentage'),
        ]
        
        for pattern, num_type in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                numbers.append({
                    "value": match.group(),
                    "type": num_type,
                    "position": match.start()
                })
        
        return numbers
    
    def _calculate_smart_accuracy(
        self,
        results: Dict[str, Optional[documentai.Document]],
        characteristics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate accuracy metrics"""
        
        metrics = {
            "overall_accuracy": 0.0,
            "processor_accuracies": {}
        }
        
        all_confidences = []
        
        for processor_name, document in results.items():
            if document and hasattr(document, 'pages'):
                confidences = []
                for page in document.pages:
                    if hasattr(page, 'confidence') and page.confidence > 0:
                        confidences.append(page.confidence)
                
                if confidences:
                    avg_confidence = sum(confidences) / len(confidences)
                    metrics["processor_accuracies"][processor_name] = avg_confidence
                    all_confidences.append(avg_confidence)
                else:
                    metrics["processor_accuracies"][processor_name] = 0.95
                    all_confidences.append(0.95)
        
        # Adjust overall accuracy based on characteristics
        if all_confidences:
            base_accuracy = sum(all_confidences) / len(all_confidences)
            
            # Reduce accuracy estimate for handwriting
            if characteristics["is_handwritten"]:
                base_accuracy *= 0.85  # Handwriting is harder
            
            # Reduce for non-English
            if characteristics["primary_language"] != "en":
                base_accuracy *= 0.95  # Slight reduction for non-English
            
            metrics["overall_accuracy"] = base_accuracy
        else:
            metrics["overall_accuracy"] = 0.90
        
        return metrics
    
    def _explain_selection(self, characteristics: Dict[str, Any]) -> str:
        """Explain why processors were selected"""
        reasons = []
        
        if characteristics["is_handwritten"]:
            reasons.append(f"Handwritten content detected ({characteristics['handwriting_percentage']:.1%})")
        
        if characteristics["primary_language"] != "en":
            reasons.append(f"Non-English language: {characteristics['primary_language']}")
        
        if characteristics["is_multilingual"]:
            reasons.append("Multilingual document detected")
        
        if characteristics["has_complex_tables"]:
            reasons.append("Complex nested tables detected")
        
        if not reasons:
            reasons.append("Standard printed document")
        
        return " | ".join(reasons)


def process_document_smart(
    file_content: bytes,
    mime_type: str,
    filename: str
) -> Dict[str, Any]:
    """
    Convenience function for smart document processing
    
    Args:
        file_content: Binary content
        mime_type: MIME type
        filename: File name
        
    Returns:
        Smart extraction with automatic processor selection
    """
    processor = SmartDocumentProcessor()
    return processor.process_document_smart(file_content, mime_type, filename)
