"""
Data viewer component for the dashboard
"""
import streamlit as st
from typing import Any, Dict, Optional
import json
import pandas as pd


def render_data_viewer(api_client: Any):
    """
    Render the extracted data viewer interface
    
    Args:
        api_client: API client instance for backend communication
    """
    st.subheader("📊 Extracted Loan Data")
    
    # Check if there are any uploaded documents
    if "uploaded_documents" not in st.session_state or not st.session_state.uploaded_documents:
        st.info("👆 No documents uploaded yet. Please upload documents first.")
        if st.button("Go to Upload"):
            st.session_state.current_view = "upload"
            st.rerun()
        return
    
    # Document selector
    doc_names = [doc["name"] for doc in st.session_state.uploaded_documents]
    selected_doc_name = st.selectbox(
        "Select a document to view",
        doc_names,
        index=0
    )
    
    # Find selected document
    selected_doc = next(
        (doc for doc in st.session_state.uploaded_documents if doc["name"] == selected_doc_name),
        None
    )
    
    if not selected_doc:
        st.error("Document not found")
        return
    
    # Display document info
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Document Name", selected_doc["name"])
    with col2:
        st.metric("File Size", f"{selected_doc['size'] / 1024:.2f} KB")
    with col3:
        st.metric("Status", "Processed" if "extracted_data" in selected_doc else "Pending")
    with col4:
        # Check if data is masked
        extracted_data_temp = selected_doc.get("extracted_data", {})
        is_masked = extracted_data_temp.get("_data_masking", {}).get("masked", False)
        if is_masked:
            st.metric("Privacy", "🔒 Protected")
        else:
            st.metric("Privacy", "⚠️ Unmasked")
    
    # Show masking notice if data is masked
    if extracted_data_temp.get("_data_masking", {}).get("masked", False):
        masking_info = extracted_data_temp.get("_data_masking", {})
        st.success(f"🔒 **Privacy Protected**: Sensitive data masked at '{masking_info.get('mask_level', 'standard')}' level")
        with st.expander("ℹ️ What data is masked?"):
            masked_fields = masking_info.get("masked_fields", [])
            if masked_fields:
                st.write(f"**{len(masked_fields)} fields masked:**")
                st.write(", ".join(masked_fields[:10]))
                if len(masked_fields) > 10:
                    st.write(f"... and {len(masked_fields) - 10} more")
            st.caption(masking_info.get("note", ""))
    
    st.markdown("---")
    
    # Get extracted data from the document
    extracted_data = selected_doc.get("extracted_data", {})
    
    if not extracted_data:
        st.warning("⚠️ No extracted data available for this document. Processing may still be in progress.")
        return
    
    # Check if AI-powered extraction was used
    is_ai_powered = extracted_data.get("extraction_method") == "gemini_ai_powered"
    
    if is_ai_powered:
        st.success("🤖 **AI-Powered Analysis** - Enhanced extraction using Google Gemini")
        
        # Display AI Analysis Summary
        if "ai_analysis" in extracted_data:
            ai_analysis = extracted_data["ai_analysis"]
            st.markdown("### 🧠 AI Document Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Type:** {extracted_data.get('document_type', 'Unknown')}")
            with col2:
                st.info(f"**Category:** {extracted_data.get('document_category', 'Unknown')}")
            with col3:
                st.info(f"**Audience:** {ai_analysis.get('target_audience', 'General')}")
            
            if "document_summary" in ai_analysis:
                st.markdown("#### 📝 Document Summary")
                st.write(ai_analysis["document_summary"])
            
            if "key_topics" in ai_analysis and ai_analysis["key_topics"]:
                st.markdown("#### 🏷️ Key Topics")
                topics = ai_analysis["key_topics"]
                st.write(", ".join(topics) if isinstance(topics, list) else topics)
            
            st.markdown("---")
        
        # Display Web References
        if "web_references" in extracted_data and extracted_data["web_references"]:
            with st.expander("🌐 Web References & Additional Context"):
                st.write(extracted_data.get("reference_note", "Related information found online:"))
                for idx, ref in enumerate(extracted_data["web_references"], 1):
                    st.markdown(f"{idx}. [{ref.get('url', 'Link')}]({ref.get('url', '#')})")
                    if "relevance" in ref:
                        st.caption(ref["relevance"])
    
    # Display extracted data
    st.subheader("💰 Extracted Information")
    
    # View mode toggle
    st.markdown("---")
    view_mode = st.radio(
        "Data View Mode",
        ["🔒 Protected View (Masked)", "📄 Full View (Unmasked)"],
        index=0,
        horizontal=True,
        help="Toggle between privacy-protected and full data view"
    )
    
    # Switch data based on view mode
    if view_mode == "📄 Full View (Unmasked)" and "extracted_data_unmasked" in selected_doc:
        st.warning("⚠️ **Full View Active**: Showing unmasked data with sensitive information. Use for personal analysis only.")
        display_data = selected_doc["extracted_data_unmasked"]
    else:
        display_data = extracted_data
    
    # Calculate additional metrics (use display_data which respects view mode)
    principal = display_data.get("principal_amount", 0)
    rate = display_data.get("interest_rate", 0)
    tenure = display_data.get("tenure_months", 0)
    monthly_emi = display_data.get("monthly_emi", 0)
    
    total_amount = monthly_emi * tenure if monthly_emi and tenure else 0
    total_interest = total_amount - principal if total_amount > principal else 0
    
    # Display in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Basic Details")
        st.write(f"**Loan Type:** {display_data.get('loan_type', 'N/A')}")
        st.write(f"**Bank Name:** {display_data.get('bank_name', 'N/A')}")
        st.write(f"**Principal Amount:** ${principal:,.2f}")
        st.write(f"**Interest Rate:** {rate}%")
        st.write(f"**Tenure:** {tenure} months ({tenure//12} years)")
    
    with col2:
        st.markdown("#### 💵 Payment Details")
        st.write(f"**Monthly EMI:** ${monthly_emi:,.2f}")
        st.write(f"**Total Interest:** ${total_interest:,.2f}")
        st.write(f"**Total Amount:** ${total_amount:,.2f}")
        st.write(f"**Processing Fee:** ${display_data.get('processing_fee', 0):,.2f}")
    
    st.markdown("---")
    
    # Additional details in tabs
    if is_ai_powered:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🔴 Critical Info", 
            "🟡 Important Info", 
            "🟢 Useful Info",
            "📄 Fees & Charges", 
            "📅 Payment Schedule", 
            "🔍 Complete Data"
        ])
        
        # Critical Information Tab
        with tab1:
            st.markdown("#### 🔴 Critical Information (Must Know)")
            critical_info = extracted_data.get("critical_information", {})
            if critical_info:
                st.json(critical_info)
            else:
                st.info("No critical information categorized")
        
        # Important Information Tab
        with tab2:
            st.markdown("#### 🟡 Important Information (Should Know)")
            important_info = extracted_data.get("important_information", {})
            if important_info:
                st.json(important_info)
            else:
                st.info("No important information categorized")
        
        # Useful Information Tab
        with tab3:
            st.markdown("#### 🟢 Useful Information (Nice to Know)")
            useful_info = extracted_data.get("useful_information", {})
            if useful_info:
                st.json(useful_info)
            else:
                st.info("No useful information categorized")
    else:
        tab1, tab2, tab3 = st.tabs(["📄 Fees & Charges", "📅 Payment Schedule", "🔍 Raw Data"])
        tab4 = tab1  # Dummy assignment for compatibility
        tab5 = tab2
        tab6 = tab3
    
    with tab4:
        st.markdown("#### Fees and Charges")
        
        # Create fees dataframe
        fees_data = {
            "Fee Type": ["Processing Fee", "Late Payment Penalty", "Prepayment Penalty"],
            "Amount/Rate": [
                f"${extracted_data.get('processing_fee', 0):,.2f}",
                extracted_data.get('late_payment_penalty', 'N/A'),
                extracted_data.get('prepayment_penalty', 'N/A')
            ]
        }
        fees_df = pd.DataFrame(fees_data)
        st.dataframe(fees_df, use_container_width=True, hide_index=True)
        
    with tab5:
        st.markdown("#### Payment Schedule (Sample)")
        
        # Generate sample payment schedule
        schedule_data = []
        remaining_balance = principal
        for month in range(1, min(13, tenure + 1)):  # Show first 12 months
            interest_payment = remaining_balance * (rate / 100 / 12)
            principal_payment = monthly_emi - interest_payment
            remaining_balance -= principal_payment
            
            schedule_data.append({
                "Month": month,
                "EMI": f"${monthly_emi:,.2f}",
                "Principal": f"${principal_payment:,.2f}",
                "Interest": f"${interest_payment:,.2f}",
                "Balance": f"${max(0, remaining_balance):,.2f}"
            })
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        
        if tenure > 12:
            st.info(f"Showing first 12 months of {tenure} month tenure")
        
    with tab6:
        st.markdown("#### Complete Extracted Data")
        if is_ai_powered and "complete_extraction" in extracted_data:
            st.json(extracted_data["complete_extraction"])
        else:
            st.json(extracted_data)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col2:
        # Download masked JSON (safe to share)
        json_data_masked = json.dumps(extracted_data, indent=2)
        st.download_button(
            label="🔒 Safe JSON",
            data=json_data_masked,
            file_name=f"{selected_doc['name']}_masked.json",
            mime="application/json",
            use_container_width=True,
            help="Masked data - safe to share"
        )
    
    with col3:
        # Download unmasked JSON (full details)
        if "extracted_data_unmasked" in selected_doc:
            json_data_full = json.dumps(selected_doc["extracted_data_unmasked"], indent=2)
            st.download_button(
                label="📄 Full JSON",
                data=json_data_full,
                file_name=f"{selected_doc['name']}_full.json",
                mime="application/json",
                use_container_width=True,
                help="Full unmasked data - personal use only"
            )
        else:
            st.button("📄 Full JSON", disabled=True, use_container_width=True)
    
    with col4:
        # Download original file
        if "content" in selected_doc:
            st.download_button(
                label="📑 Original",
                data=selected_doc["content"],
                file_name=selected_doc["name"],
                mime=selected_doc.get("type", "application/pdf"),
                use_container_width=True,
                help="Original uploaded document"
            )
        else:
            st.button("📑 Original", disabled=True, use_container_width=True)
    
    with col5:
        if st.button("📊 Compare", use_container_width=True):
            st.session_state.current_view = "compare"
            st.rerun()
    
    # Confidence score (if available)
    st.markdown("---")
    st.subheader("🎯 Extraction Confidence")
    confidence = extracted_data.get("extraction_confidence", 0.95)
    
    # Color code based on confidence
    if confidence >= 0.9:
        st.success(f"**High Confidence:** {confidence * 100:.1f}%")
    elif confidence >= 0.8:
        st.warning(f"**Medium Confidence:** {confidence * 100:.1f}%")
    else:
        st.error(f"**Low Confidence:** {confidence * 100:.1f}%")
    
    st.progress(confidence)
    
    if confidence < 0.8:
        st.warning("⚠️ Low confidence score. Please review the extracted data carefully and verify with the original document.")
    
    # Add visual summary
    st.markdown("---")
    st.subheader("📈 Loan Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    with summary_col1:
        st.metric("Total Cost", f"${total_amount:,.2f}", f"+${total_interest:,.2f} interest")
    with summary_col2:
        st.metric("Monthly Payment", f"${monthly_emi:,.2f}", f"{tenure} months")
    with summary_col3:
        effective_rate = (total_interest / principal) * 100 if principal > 0 else 0
        st.metric("Effective Rate", f"{effective_rate:.1f}%", f"{rate}% APR")
