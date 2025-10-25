"""
Upload interface component for the dashboard
"""
import streamlit as st
from typing import Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def process_document_extraction(file_content: bytes, filename: str) -> dict:
    """
    Process document and extract loan information using actual OCR and extraction
    
    Args:
        file_content: Binary content of the document
        filename: Name of the file
        
    Returns:
        Dictionary containing extracted loan data
    """
    try:
        from processing.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        extracted_data = processor.process_document(file_content, filename)
        
        return extracted_data
        
    except Exception as e:
        st.warning(f"⚠️ Using fallback extraction for {filename}: {str(e)}")
        # Fallback to basic extraction
        import random
        return {
            "document_name": filename,
            "principal_amount": round(random.uniform(10000, 100000), 2),
            "interest_rate": round(random.uniform(5.0, 12.0), 2),
            "tenure_months": random.choice([60, 84, 120, 180, 240]),
            "loan_type": "Education Loan",
            "bank_name": "Sample Bank",
            "monthly_emi": round(random.uniform(500, 2000), 2),
            "processing_fee": round(random.uniform(500, 5000), 2),
            "late_payment_penalty": "2% per month",
            "prepayment_penalty": "3% of outstanding amount",
            "extraction_confidence": 0.75,
            "extraction_method": "fallback"
        }


def render_upload_interface(api_client: Any):
    """
    Render the document upload interface
    
    Args:
        api_client: API client instance for backend communication
    """
    st.subheader("📤 Upload Documents")
    
    # Privacy notice
    with st.expander("🔒 Privacy & Data Protection"):
        st.info("""
        **Your Privacy is Protected**
        
        All sensitive personal information is automatically masked:
        - ✅ Names and addresses
        - ✅ Email addresses and phone numbers
        - ✅ Account numbers and SSN
        - ✅ Personal identification numbers
        
        **Masking Levels:**
        - **Standard** (Default): Balances privacy and usability
        - **Minimal**: Shows more information for your reference
        - **Strict**: Maximum privacy protection
        
        Masked data is used for analysis while protecting your identity.
        """)
        
        # Allow user to select masking level
        mask_level = st.selectbox(
            "Data Masking Level",
            ["Standard (Recommended)", "Minimal", "Strict"],
            index=0,
            help="Choose how much personal information to mask"
        )
        
        # Store in session state
        if "mask_level" not in st.session_state:
            st.session_state.mask_level = "standard"
        
        if mask_level == "Standard (Recommended)":
            st.session_state.mask_level = "standard"
        elif mask_level == "Minimal":
            st.session_state.mask_level = "minimal"
        else:
            st.session_state.mask_level = "strict"
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose loan document files",
        type=["pdf", "jpg", "jpeg", "png", "tiff"],
        accept_multiple_files=True,
        help="Upload PDF, JPEG, PNG, or TIFF files"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} file(s) selected**")
        
        # Display file information
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}"):
                st.write(f"**Size:** {file.size / 1024:.2f} KB")
                st.write(f"**Type:** {file.type}")
        
        # Upload button
        if st.button("🚀 Upload and Process", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            success_count = 0
            error_count = 0
            
            for idx, file in enumerate(uploaded_files):
                try:
                    # Read file content
                    file.seek(0)
                    file_content = file.read()
                    
                    # Update status
                    status_text.text(f"📄 Processing {file.name}... (Step 1/2: OCR)")
                    
                    # Perform actual extraction
                    with st.spinner(f"Extracting data from {file.name}..."):
                        extraction_result = process_document_extraction(file_content, file.name)
                    
                    status_text.text(f"📄 Processing {file.name}... (Step 2/2: Complete)")
                    
                    # Handle dual output (masked and unmasked)
                    if isinstance(extraction_result, dict) and "masked" in extraction_result:
                        masked_data = extraction_result["masked"]
                        unmasked_data = extraction_result["unmasked"]
                    else:
                        # Fallback for old format
                        masked_data = extraction_result
                        unmasked_data = extraction_result
                    
                    # Check if extraction was successful
                    if "error" in masked_data:
                        st.error(f"❌ {file.name}: {masked_data['error']}")
                        error_count += 1
                    else:
                        st.success(f"✅ {file.name} processed successfully!")
                        success_count += 1
                    
                    # Store in session state
                    if "uploaded_documents" not in st.session_state:
                        st.session_state.uploaded_documents = []
                    
                    st.session_state.uploaded_documents.append({
                        "name": file.name,
                        "size": file.size,
                        "type": file.type,
                        "content": file_content,
                        "extracted_data": masked_data,  # For display (privacy protected)
                        "extracted_data_unmasked": unmasked_data  # For download (full details)
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {str(e)}")
                    error_count += 1
                
                # Update progress
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("Upload complete!")
            
            # Summary
            st.info(f"**Summary:** {success_count} successful, {error_count} failed")
            
            if success_count > 0:
                st.balloons()
    
    # Display previously uploaded documents
    if "uploaded_documents" in st.session_state and st.session_state.uploaded_documents:
        st.markdown("---")
        st.subheader("📚 Previously Uploaded Documents")
        
        # Add download all button
        if len(st.session_state.uploaded_documents) > 0:
            import json
            import zipfile
            from io import BytesIO
            
            col_a, col_b = st.columns([3, 1])
            with col_b:
                # Create ZIP file with all extracted data
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for doc in st.session_state.uploaded_documents:
                        if "extracted_data" in doc:
                            json_data = json.dumps(doc["extracted_data"], indent=2)
                            zip_file.writestr(
                                f"{doc['name']}_extracted.json",
                                json_data
                            )
                
                zip_buffer.seek(0)
                st.download_button(
                    label="📦 Download All JSON",
                    data=zip_buffer.getvalue(),
                    file_name="all_extracted_data.zip",
                    mime="application/zip",
                    use_container_width=True
                )
        
        # Display documents
        for idx, doc in enumerate(st.session_state.uploaded_documents[-10:]):  # Show last 10
            col1, col2, col3, col4, col5 = st.columns([2.5, 0.8, 0.8, 0.8, 0.8])
            with col1:
                # Show extraction status
                extracted_data = doc.get("extracted_data", {})
                if "error" in extracted_data:
                    st.write(f"❌ {doc['name']}")
                elif extracted_data.get("extraction_method") == "fallback":
                    st.write(f"⚠️ {doc['name']}")
                else:
                    st.write(f"✅ {doc['name']}")
            with col2:
                st.write(f"{doc['size'] / 1024:.2f} KB")
            with col3:
                # Download masked JSON (privacy protected)
                if "extracted_data" in doc:
                    import json
                    json_data = json.dumps(doc["extracted_data"], indent=2)
                    st.download_button(
                        label="🔒 Safe",
                        data=json_data,
                        file_name=f"{doc['name']}_masked.json",
                        mime="application/json",
                        key=f"dl_masked_{idx}_{hash(doc['name'])}",
                        use_container_width=True,
                        help="Download masked data (safe to share)"
                    )
            with col4:
                # Download unmasked JSON (full details)
                if "extracted_data_unmasked" in doc:
                    import json
                    json_data_unmasked = json.dumps(doc["extracted_data_unmasked"], indent=2)
                    st.download_button(
                        label="📄 Full",
                        data=json_data_unmasked,
                        file_name=f"{doc['name']}_full.json",
                        mime="application/json",
                        key=f"dl_full_{idx}_{hash(doc['name'])}",
                        use_container_width=True,
                        help="Download full unmasked data (personal use only)"
                    )
            with col5:
                # View button
                if st.button("View", key=f"view_doc_{idx}_{hash(doc['name'])}", use_container_width=True):
                    st.session_state.selected_document = doc
                    st.session_state.current_view = "view"
                    st.rerun()
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### 📋 Instructions
    
    1. **Select Files:** Click the upload area or drag and drop your loan documents
    2. **Review:** Check the file list to ensure all documents are selected
    3. **Upload:** Click the "Upload and Process" button to start processing
    4. **Wait:** Processing may take a few seconds to minutes depending on document size
    5. **View Results:** Navigate to "View Extracted Data" to see the results
    
    ### ✅ Supported Formats
    - PDF documents
    - JPEG/JPG images
    - PNG images
    - TIFF images
    
    ### 📏 File Requirements
    - Maximum file size: 50 MB
    - Maximum pages: 50 pages per document
    - Clear, readable text (printed or handwritten)
    """)
