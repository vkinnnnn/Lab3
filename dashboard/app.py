"""
Complete Document Extractor Dashboard
Streamlit UI for document extraction with accuracy metrics
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
import json
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Complete Document Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://api:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .accuracy-excellent {
        color: #28a745;
        font-weight: bold;
    }
    .accuracy-good {
        color: #17a2b8;
        font-weight: bold;
    }
    .accuracy-fair {
        color: #ffc107;
        font-weight: bold;
    }
    .accuracy-review {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Header
    st.markdown('<p class="main-header">📄 Complete Document Extractor</p>', unsafe_allow_html=True)
    st.markdown("**Extract ALL text, data, numbers, tables, and boxes with accuracy validation**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("🔧 Settings")
        st.markdown("---")
        
        st.subheader("Processors")
        st.info("✓ Form Parser\n✓ Document OCR")
        
        st.subheader("Features")
        st.success("""
        ✓ Complete text extraction
        ✓ All numbers extraction
        ✓ Form fields & boxes
        ✓ Tables with nested columns
        ✓ Accuracy metrics
        ✓ Dual processor validation
        """)
        
        st.markdown("---")
        st.caption("Powered by Google Document AI")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Extract", "📊 View Results", "ℹ️ About"])
    
    with tab1:
        show_upload_tab()
    
    with tab2:
        show_results_tab()
    
    with tab3:
        show_about_tab()

def show_upload_tab():
    """Upload and extraction tab"""
    
    st.header("Upload Document")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a document",
            type=["pdf", "jpg", "jpeg", "png", "tiff", "tif"],
            help="Upload PDF or image files for complete extraction"
        )
        
        if uploaded_file:
            st.success(f"✓ File loaded: {uploaded_file.name}")
            st.info(f"Size: {uploaded_file.size / 1024:.2f} KB")
            
            if st.button("🚀 Extract Complete Document", type="primary", use_container_width=True):
                extract_document(uploaded_file)
    
    with col2:
        st.subheader("What Gets Extracted")
        st.markdown("""
        **Text Elements:**
        - All blocks
        - All paragraphs
        - All lines
        - All tokens
        
        **Data:**
        - All numbers
        - All form fields
        - All tables
        - All boxes
        
        **Structure:**
        - Nested columns
        - Merged cells
        - Layout info
        
        **Validation:**
        - Accuracy metrics
        - Confidence scores
        - Quality flags
        """)

def extract_document(uploaded_file):
    """Extract document and display results"""
    
    with st.spinner("🔄 Extracting document with both processors..."):
        try:
            # Upload to API
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(
                f"{API_BASE_URL}/api/v1/extract",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Store in session state
                st.session_state.extraction_result = result
                st.session_state.extracted_filename = uploaded_file.name
                
                st.success("✓ Extraction complete!")
                
                # Display summary
                display_extraction_summary(result)
                
            else:
                st.error(f"❌ Extraction failed: {response.text}")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def display_extraction_summary(result: Dict[str, Any]):
    """Display extraction summary"""
    
    st.markdown("---")
    st.subheader("📊 Extraction Summary")
    
    # Accuracy metrics
    accuracy = result.get("accuracy_metrics", {})
    overall_accuracy = accuracy.get("overall_accuracy", 0)
    
    # Display overall accuracy
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        accuracy_class = get_accuracy_class(overall_accuracy)
        st.markdown(f'<div class="metric-card"><h3>Overall Accuracy</h3><p class="{accuracy_class}">{overall_accuracy:.1%}</p></div>', unsafe_allow_html=True)
    
    with col2:
        form_accuracy = accuracy.get("form_parser_accuracy", 0)
        st.markdown(f'<div class="metric-card"><h3>Form Parser</h3><p>{form_accuracy:.1%}</p></div>', unsafe_allow_html=True)
    
    with col3:
        ocr_accuracy = accuracy.get("ocr_accuracy", 0)
        st.markdown(f'<div class="metric-card"><h3>Document OCR</h3><p>{ocr_accuracy:.1%}</p></div>', unsafe_allow_html=True)
    
    with col4:
        processors = result.get("processors_used", [])
        st.markdown(f'<div class="metric-card"><h3>Processors</h3><p>{len(processors)}/2</p></div>', unsafe_allow_html=True)
    
    # Extraction stats
    st.markdown("### 📈 Extraction Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        text_elements = len(result.get("all_text_elements", []))
        st.metric("Text Elements", text_elements)
    
    with col2:
        numbers = len(result.get("all_numbers", []))
        st.metric("Numbers Found", numbers)
    
    with col3:
        form_fields = len(result.get("all_form_fields", []))
        st.metric("Form Fields", form_fields)
    
    with col4:
        tables = len(result.get("all_tables", []))
        st.metric("Tables", tables)
    
    # Low confidence items
    low_conf = accuracy.get("low_confidence_items", [])
    if low_conf:
        st.warning(f"⚠️ {len(low_conf)} items with low confidence (< 85%) - review recommended")
    
    st.info("💡 Switch to 'View Results' tab to see complete extraction details")

def show_results_tab():
    """View extraction results tab"""
    
    if "extraction_result" not in st.session_state:
        st.info("👆 Upload and extract a document first")
        return
    
    result = st.session_state.extraction_result
    filename = st.session_state.get("extracted_filename", "document")
    
    st.header(f"📄 Results: {filename}")
    
    # Tabs for different data types
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Complete Text",
        "🔢 Numbers",
        "📋 Form Fields",
        "📊 Tables",
        "📏 Accuracy",
        "💾 Download"
    ])
    
    with tab1:
        show_text_results(result)
    
    with tab2:
        show_numbers_results(result)
    
    with tab3:
        show_form_fields_results(result)
    
    with tab4:
        show_tables_results(result)
    
    with tab5:
        show_accuracy_results(result)
    
    with tab6:
        show_download_options(result, filename)

def show_text_results(result: Dict[str, Any]):
    """Display text extraction results"""
    
    st.subheader("Complete Text Content")
    
    complete_text = result.get("complete_text", {})
    
    # Text source selector
    text_source = st.radio(
        "Select text source:",
        ["Merged (Best)", "Form Parser", "Document OCR"],
        horizontal=True
    )
    
    if text_source == "Merged (Best)":
        text = complete_text.get("merged_text", "")
    elif text_source == "Form Parser":
        text = complete_text.get("form_parser_text", "")
    else:
        text = complete_text.get("ocr_text", "")
    
    if text:
        st.text_area("Extracted Text", text, height=400)
        st.info(f"📊 Total characters: {len(text)}")
    else:
        st.warning("No text extracted")
    
    # Text elements breakdown
    st.markdown("---")
    st.subheader("Text Elements Breakdown")
    
    text_elements = result.get("all_text_elements", [])
    if text_elements:
        df = pd.DataFrame(text_elements)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No text elements found")

def show_numbers_results(result: Dict[str, Any]):
    """Display extracted numbers"""
    
    st.subheader("All Numbers Extracted")
    
    numbers = result.get("all_numbers", [])
    
    if numbers:
        # Group by type
        number_types = {}
        for num in numbers:
            num_type = num.get("type", "unknown")
            if num_type not in number_types:
                number_types[num_type] = []
            number_types[num_type].append(num["value"])
        
        # Display by type
        for num_type, values in number_types.items():
            with st.expander(f"📊 {num_type.replace('_', ' ').title()} ({len(values)})"):
                st.write(", ".join(values[:50]))
                if len(values) > 50:
                    st.caption(f"... and {len(values) - 50} more")
        
        # Full table
        st.markdown("---")
        df = pd.DataFrame(numbers)
        st.dataframe(df, use_container_width=True)
        
        st.success(f"✓ Total numbers found: {len(numbers)}")
    else:
        st.info("No numbers found in document")

def show_form_fields_results(result: Dict[str, Any]):
    """Display form fields"""
    
    st.subheader("All Form Fields")
    
    form_fields = result.get("all_form_fields", [])
    
    if form_fields:
        for field in form_fields:
            with st.expander(f"📝 {field.get('field_name', 'Unnamed')} (Page {field.get('page', '?')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Field Name:**", field.get("field_name", ""))
                    st.write("**Field Value:**", field.get("field_value", ""))
                with col2:
                    st.write("**Name Confidence:**", f"{field.get('name_confidence', 0):.1%}")
                    st.write("**Value Confidence:**", f"{field.get('value_confidence', 0):.1%}")
                    st.write("**Source:**", field.get("source", ""))
        
        st.success(f"✓ Total form fields: {len(form_fields)}")
    else:
        st.info("No form fields found")

def show_tables_results(result: Dict[str, Any]):
    """Display tables"""
    
    st.subheader("All Tables")
    
    tables = result.get("all_tables", [])
    
    if tables:
        for table in tables:
            table_id = table.get("table_id", "?")
            page = table.get("page", "?")
            rows = table.get("total_rows", 0)
            cols = table.get("total_columns", 0)
            
            with st.expander(f"📊 Table {table_id} (Page {page}) - {rows}x{cols}"):
                # Display headers
                headers = table.get("header_rows", [])
                if headers:
                    st.write("**Headers:**")
                    for header_row in headers:
                        header_texts = [cell.get("text", "") if isinstance(cell, dict) else cell for cell in header_row]
                        st.write(" | ".join(header_texts))
                
                # Display body rows
                body_rows = table.get("body_rows", [])
                if body_rows:
                    st.write("**Data:**")
                    for row in body_rows[:10]:  # Show first 10 rows
                        row_texts = [cell.get("text", "") if isinstance(cell, dict) else cell for cell in row]
                        st.write(" | ".join(row_texts))
                    if len(body_rows) > 10:
                        st.caption(f"... and {len(body_rows) - 10} more rows")
                
                # Nested structures
                nested = table.get("nested_structures", [])
                if nested:
                    st.write(f"**Nested Structures:** {len(nested)} merged cells")
        
        st.success(f"✓ Total tables: {len(tables)}")
    else:
        st.info("No tables found")

def show_accuracy_results(result: Dict[str, Any]):
    """Display accuracy metrics"""
    
    st.subheader("Accuracy Metrics")
    
    accuracy = result.get("accuracy_metrics", {})
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        overall = accuracy.get("overall_accuracy", 0)
        st.metric("Overall Accuracy", f"{overall:.1%}", 
                 delta=get_accuracy_label(overall))
    
    with col2:
        form_acc = accuracy.get("form_parser_accuracy", 0)
        st.metric("Form Parser", f"{form_acc:.1%}")
    
    with col3:
        ocr_acc = accuracy.get("ocr_accuracy", 0)
        st.metric("Document OCR", f"{ocr_acc:.1%}")
    
    # Detailed metrics
    st.markdown("---")
    st.subheader("Detailed Confidence Scores")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        text_conf = accuracy.get("text_extraction_confidence", 0)
        st.metric("Text Extraction", f"{text_conf:.1%}")
    
    with col2:
        table_conf = accuracy.get("table_extraction_confidence", 0)
        st.metric("Table Extraction", f"{table_conf:.1%}")
    
    with col3:
        field_conf = accuracy.get("form_field_confidence", 0)
        st.metric("Form Fields", f"{field_conf:.1%}")
    
    # Page confidences
    st.markdown("---")
    st.subheader("Page-by-Page Confidence")
    
    page_confs = accuracy.get("page_confidences", [])
    if page_confs:
        df = pd.DataFrame(page_confs)
        st.bar_chart(df.set_index("page")["confidence"])
    
    # Low confidence items
    st.markdown("---")
    st.subheader("Low Confidence Items (< 85%)")
    
    low_conf = accuracy.get("low_confidence_items", [])
    if low_conf:
        st.warning(f"⚠️ {len(low_conf)} items need review")
        df = pd.DataFrame(low_conf)
        st.dataframe(df, use_container_width=True)
    else:
        st.success("✓ All items have good confidence!")

def show_download_options(result: Dict[str, Any], filename: str):
    """Download options"""
    
    st.subheader("Download Extraction Results")
    
    # JSON download
    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Download Complete JSON",
            data=json_str,
            file_name=f"{filename}_complete_extraction.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Text only download
        complete_text = result.get("complete_text", {}).get("merged_text", "")
        st.download_button(
            label="📥 Download Text Only",
            data=complete_text,
            file_name=f"{filename}_text.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Stats
    st.info(f"""
    **Extraction Stats:**
    - Text elements: {len(result.get('all_text_elements', []))}
    - Numbers: {len(result.get('all_numbers', []))}
    - Form fields: {len(result.get('all_form_fields', []))}
    - Tables: {len(result.get('all_tables', []))}
    - Overall accuracy: {result.get('accuracy_metrics', {}).get('overall_accuracy', 0):.1%}
    """)

def show_about_tab():
    """About tab"""
    
    st.header("About Complete Document Extractor")
    
    st.markdown("""
    ### 🎯 Purpose
    
    This system extracts **EVERYTHING** from documents:
    - All text, data, and numbers
    - All form fields and boxes
    - All tables with nested columns
    - Complete structure preservation
    - Real accuracy validation
    
    ### 🔧 Technology
    
    **Dual Processor System:**
    - **Form Parser**: Best for structured forms and tables
    - **Document OCR**: Best for general text extraction
    - **Combined**: Maximum accuracy through cross-validation
    
    ### 📊 Accuracy Metrics
    
    - **Overall Accuracy**: Combined confidence from both processors
    - **Per-Processor**: Individual accuracy scores
    - **Element-Level**: Confidence for text, tables, fields
    - **Quality Flags**: Low confidence items identified
    
    ### ✅ Quality Thresholds
    
    - **Excellent**: > 95% (0.95)
    - **Good**: 90-95% (0.90-0.95)
    - **Fair**: 85-90% (0.85-0.90)
    - **Review**: < 85% (< 0.85)
    
    ### 📚 Supported Formats
    
    - PDF documents (`.pdf`)
    - Images (`.jpg`, `.jpeg`, `.png`)
    - TIFF files (`.tiff`, `.tif`)
    - Multi-page documents
    
    ### 🚀 Features
    
    ✓ Complete text extraction (blocks, paragraphs, lines, tokens)
    ✓ All numbers extraction (integers, decimals, currency, percentages)
    ✓ Form fields with original names
    ✓ Tables with nested columns and merged cells
    ✓ Real accuracy metrics with validation
    ✓ Dual processor cross-validation
    ✓ Low confidence item flagging
    ✓ JSON export with complete data
    
    ### 📖 Documentation
    
    See `README_COMPLETE_EXTRACTOR.md` for complete documentation.
    """)

def get_accuracy_class(accuracy: float) -> str:
    """Get CSS class for accuracy"""
    if accuracy >= 0.95:
        return "accuracy-excellent"
    elif accuracy >= 0.90:
        return "accuracy-good"
    elif accuracy >= 0.85:
        return "accuracy-fair"
    else:
        return "accuracy-review"

def get_accuracy_label(accuracy: float) -> str:
    """Get label for accuracy"""
    if accuracy >= 0.95:
        return "Excellent"
    elif accuracy >= 0.90:
        return "Good"
    elif accuracy >= 0.85:
        return "Fair"
    else:
        return "Review"

if __name__ == "__main__":
    main()
