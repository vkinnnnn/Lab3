"""
Main document processor - uses ONLY Document AI for extraction
Professional JSON output with no extras
"""
import logging
from typing import Dict, Any
from .document_ai_processor import DocumentAIProcessor
from .professional_formatter import ProfessionalFormatter

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Main document processor for loan documents
    Uses Google Document AI for 99%+ accuracy extraction
    Outputs professional JSON format
    """
    
    def __init__(self):
        """Initialize processor with Document AI only"""
        self.document_ai = DocumentAIProcessor()
        self.formatter = ProfessionalFormatter()
        logger.info("Document Processor initialized (Document AI only)")
    
    def process_document(
        self, 
        file_content: bytes, 
        mime_type: str,
        filename: str
    ) -> Dict[str, Any]:
        """
        Process document and return professional JSON output
        
        Args:
            file_content: Binary content of the document
            mime_type: MIME type (application/pdf, image/jpeg, etc.)
            filename: Name of the file
            
        Returns:
            Professional formatted extraction result
        """
        try:
            logger.info(f"Processing document: {filename}")
            
            # Step 1: Extract data using Document AI
            extraction_result = self.document_ai.process_document(
                file_content, 
                mime_type, 
                filename
            )
            
            logger.info(f"Document AI extraction complete: {filename}")
            logger.info(f"Confidence: {extraction_result.get('extraction_confidence', 0):.2%}")
            
            # Step 2: Return the result (already in good format)
            return extraction_result
            
        except Exception as e:
            logger.error(f"Document processing error: {str(e)}")
            return {
                "document_name": filename,
                "error": str(e),
                "extraction_status": "failed"
            }
    
    def get_professional_json(
        self, 
        file_content: bytes, 
        mime_type: str,
        filename: str
    ) -> str:
        """
        Process document and return professional JSON string
        
        Args:
            file_content: Binary content of the document
            mime_type: MIME type
            filename: Name of the file
            
        Returns:
            Professional JSON string with clean spacing
        """
        # Process document
        result = self.process_document(file_content, mime_type, filename)
        
        # Format as professional JSON
        json_output = self.formatter.format_extraction_result(result)
        
        return json_output
    
    def save_json_output(
        self,
        file_content: bytes,
        mime_type: str,
        filename: str,
        output_path: str
    ) -> str:
        """
        Process document and save as professional JSON file
        
        Args:
            file_content: Binary content
            mime_type: MIME type
            filename: File name
            output_path: Path to save JSON file
            
        Returns:
            Path to saved JSON file
        """
        import os
        
        # Get professional JSON
        json_output = self.get_professional_json(file_content, mime_type, filename)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        logger.info(f"JSON output saved to: {output_path}")
        return output_path


def process_loan_document(
    file_content: bytes,
    mime_type: str,
    filename: str
) -> Dict[str, Any]:
    """
    Convenience function to process loan document
    
    Args:
        file_content: Binary content
        mime_type: MIME type
        filename: File name
        
    Returns:
        Extraction result
    """
    processor = DocumentProcessor()
    return processor.process_document(file_content, mime_type, filename)


def get_professional_json_output(
    file_content: bytes,
    mime_type: str,
    filename: str
) -> str:
    """
    Convenience function to get professional JSON output
    
    Args:
        file_content: Binary content
        mime_type: MIME type
        filename: File name
        
    Returns:
        Professional JSON string
    """
    processor = DocumentProcessor()
    return processor.get_professional_json(file_content, mime_type, filename)
