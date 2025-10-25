"""
Professional JSON formatter - Complete extraction output
Outputs EVERYTHING exactly as it appears in the original document
"""
import json
from typing import Dict, Any
from datetime import datetime


class ProfessionalFormatter:
    """
    Format complete extraction result into professional JSON
    Preserves original document format and structure
    """
    
    def format_extraction_result(self, document_ai_result: Dict[str, Any]) -> str:
        """
        Format complete Document AI extraction into professional JSON
        
        Args:
            document_ai_result: Complete extraction result from Document AI
            
        Returns:
            Professional JSON string with all extracted data
        """
        
        # Create output with EVERYTHING extracted
        complete_output = {
            "document_metadata": {
                "document_name": document_ai_result.get("document_name", ""),
                "extraction_timestamp": datetime.now().isoformat(),
                "extraction_method": document_ai_result.get("extraction_method", "google_document_ai"),
                "processors_used": document_ai_result.get("processors_used", []),
                "confidence_score": round(document_ai_result.get("extraction_confidence", 0.0), 4),
                "total_pages": document_ai_result.get("total_pages", 0)
            },
            
            # COMPLETE TEXT - exactly as it appears in the document
            "complete_text_content": document_ai_result.get("complete_text", ""),
            
            # ALL PAGES - with complete details
            "pages": document_ai_result.get("pages", []),
            
            # ALL FORM FIELDS - no filtering
            "form_fields": document_ai_result.get("form_fields", []),
            
            # ALL TABLES - complete structure
            "tables": document_ai_result.get("tables", []),
            
            # ALL ENTITIES - everything detected
            "entities": document_ai_result.get("entities", []),
            
            # ALL PARAGRAPHS - with layout
            "paragraphs": document_ai_result.get("paragraphs", []),
            
            # ALL LINES - with positions
            "lines": document_ai_result.get("lines", [])
        }
        
        # Format as professional JSON with 2-space indentation
        return json.dumps(complete_output, indent=2, ensure_ascii=False, sort_keys=False)


def format_as_professional_json(data: Dict[str, Any]) -> str:
    """
    Convenience function to format data professionally
    
    Args:
        data: Complete extraction data
        
    Returns:
        Professional JSON string
    """
    formatter = ProfessionalFormatter()
    return formatter.format_extraction_result(data)
