"""
Test script for document extraction with professional JSON output
"""
import sys
import os

# Add Lab3 to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from processing.document_processor import DocumentProcessor


def test_extraction(pdf_path: str):
    """
    Test document extraction with a PDF file
    
    Args:
        pdf_path: Path to PDF file
    """
    print(f"\n{'='*80}")
    print(f"Testing Document Extraction")
    print(f"{'='*80}\n")
    
    # Initialize processor
    print("Initializing Document Processor (Document AI only)...")
    processor = DocumentProcessor()
    print("✓ Processor initialized\n")
    
    # Read PDF file
    print(f"Reading file: {pdf_path}")
    with open(pdf_path, 'rb') as f:
        file_content = f.read()
    print(f"✓ File read ({len(file_content)} bytes)\n")
    
    # Extract filename
    filename = os.path.basename(pdf_path)
    
    # Process document
    print("Processing document with Google Document AI...")
    print("This may take 10-30 seconds...\n")
    
    result = processor.process_document(
        file_content,
        "application/pdf",
        filename
    )
    
    print("✓ Extraction complete\n")
    
    # Display summary
    print(f"{'='*80}")
    print(f"EXTRACTION SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"Document: {result.get('document_name', 'Unknown')}")
    print(f"Processors: {', '.join(result.get('processors_used', []))}")
    print(f"Confidence: {result.get('extraction_confidence', 0):.2%}")
    print(f"Pages: {len(result.get('pages', []))}")
    print(f"Form Fields: {len(result.get('form_fields', {}))}")
    print(f"Tables: {len(result.get('tables', []))}")
    print(f"Entities: {len(result.get('entities', []))}")
    
    # Show loan data if available
    loan_data = result.get('loan_data', {})
    if loan_data:
        print(f"\nLoan Information Found:")
        for key, value in loan_data.items():
            print(f"  - {key}: {value}")
    
    print(f"\n{'='*80}")
    print(f"PROFESSIONAL JSON OUTPUT")
    print(f"{'='*80}\n")
    
    # Get professional JSON
    json_output = processor.get_professional_json(
        file_content,
        "application/pdf",
        filename
    )
    
    # Display JSON (first 2000 characters)
    print(json_output[:2000])
    if len(json_output) > 2000:
        print(f"\n... (showing first 2000 of {len(json_output)} characters)")
    
    # Save to file
    output_path = os.path.join("Lab3", "output", f"{os.path.splitext(filename)[0]}_extracted.json")
    saved_path = processor.save_json_output(
        file_content,
        "application/pdf",
        filename,
        output_path
    )
    
    print(f"\n{'='*80}")
    print(f"✓ JSON saved to: {saved_path}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_extraction.py <path_to_pdf>")
        print("\nExample:")
        print("  python test_extraction.py Lab3/uploads/loan_document.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    test_extraction(pdf_path)
