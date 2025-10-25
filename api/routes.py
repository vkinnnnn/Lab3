"""
API routes for complete document extraction
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.complete_document_extractor import CompleteDocumentExtractor

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize complete extractor
extractor = CompleteDocumentExtractor()


@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    """
    Complete document extraction
    Extracts ALL text, data, numbers, tables, boxes, nested columns
    Uses both Form Parser and Document OCR
    Returns complete extraction with accuracy metrics
    """
    try:
        logger.info(f"Starting complete extraction: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        
        # Determine MIME type
        mime_type = file.content_type or "application/pdf"
        
        # Extract complete document
        result = extractor.extract_complete_document(
            file_content,
            mime_type,
            file.filename
        )
        
        logger.info(f"Extraction complete: {file.filename}")
        logger.info(f"Accuracy: {result.get('accuracy_metrics', {}).get('overall_accuracy', 0):.2%}")
        
        # Return complete extraction
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/formatted")
async def extract_document_formatted(file: UploadFile = File(...)):
    """
    Extract and return formatted JSON string
    """
    try:
        logger.info(f"Formatted extraction: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        
        # Determine MIME type
        mime_type = file.content_type or "application/pdf"
        
        # Extract complete document
        result = extractor.extract_complete_document(
            file_content,
            mime_type,
            file.filename
        )
        
        # Format as JSON string
        json_output = json.dumps(result, indent=2, ensure_ascii=False)
        
        # Return formatted JSON
        return JSONResponse(
            content={"formatted_json": json_output},
            media_type="application/json"
        )
        
    except Exception as e:
        logger.error(f"Formatted extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/save")
async def extract_and_save(file: UploadFile = File(...)):
    """
    Extract and save complete extraction as JSON file
    """
    try:
        logger.info(f"Extract and save: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        
        # Determine MIME type
        mime_type = file.content_type or "application/pdf"
        
        # Extract complete document
        result = extractor.extract_complete_document(
            file_content,
            mime_type,
            file.filename
        )
        
        # Create output path
        output_filename = f"{os.path.splitext(file.filename)[0]}_complete_extraction.json"
        output_path = os.path.join("/app", "output", output_filename)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved to: {output_path}")
        
        return {
            "status": "success",
            "message": "Complete extraction saved",
            "output_file": output_path,
            "accuracy": result.get("accuracy_metrics", {}).get("overall_accuracy", 0),
            "processors_used": result.get("processors_used", [])
        }
        
    except Exception as e:
        logger.error(f"Save error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check for complete extraction service"""
    return {
        "status": "healthy",
        "service": "complete_document_extraction",
        "processors": ["Form Parser", "Document OCR"],
        "features": [
            "Complete text extraction",
            "All numbers extraction",
            "Form fields and boxes",
            "Tables with nested columns",
            "Accuracy metrics",
            "Dual processor validation"
        ]
    }

@router.get("/accuracy")
async def get_accuracy_info():
    """Get information about accuracy calculation"""
    return {
        "accuracy_metrics": {
            "overall_accuracy": "Combined confidence from both processors",
            "form_parser_accuracy": "Form Parser confidence score",
            "ocr_accuracy": "Document OCR confidence score",
            "text_extraction_confidence": "Confidence for all text elements",
            "table_extraction_confidence": "Confidence for table data",
            "form_field_confidence": "Confidence for form fields",
            "page_confidences": "Per-page confidence scores",
            "low_confidence_items": "Items with confidence < 85%"
        },
        "processors": {
            "form_parser": "Best for structured forms and tables",
            "document_ocr": "Best for general text extraction"
        },
        "validation": "Both processors used for cross-validation"
    }
