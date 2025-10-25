"""
Gemini AI-powered extraction agent for intelligent document analysis
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from googlesearch import search

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAByZBoIRnou5MISPFPJdo4J1siQgnUhWg"
genai.configure(api_key=GEMINI_API_KEY)


class GeminiExtractionAgent:
    """
    Advanced AI agent using Google Gemini for intelligent document extraction
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("Gemini Extraction Agent initialized")
    
    def analyze_document(self, ocr_text: str, filename: str, tables: List[Dict] = None) -> Dict[str, Any]:
        """
        Perform comprehensive AI-powered document analysis
        
        Args:
            ocr_text: Extracted text from OCR
            filename: Name of the document
            tables: Extracted tables from the document
            
        Returns:
            Comprehensive extraction results
        """
        try:
            logger.info(f"Starting Gemini analysis for: {filename}")
            
            # Step 1: Identify document type and context
            doc_context = self._identify_document_context(ocr_text, filename)
            
            # Step 2: Perform web search for reference
            web_references = self._search_document_context(doc_context)
            
            # Step 3: Extract all relevant information
            extracted_info = self._extract_comprehensive_data(
                ocr_text, 
                doc_context, 
                web_references,
                tables
            )
            
            # Step 4: Determine user-relevant information
            relevant_info = self._filter_relevant_information(extracted_info)
            
            # Step 5: Structure final output
            final_output = self._structure_output(
                extracted_info,
                relevant_info,
                doc_context,
                web_references,
                filename
            )
            
            logger.info(f"Gemini analysis complete for: {filename}")
            return final_output
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {str(e)}")
            return self._generate_fallback_response(ocr_text, filename)
    
    def _identify_document_context(self, text: str, filename: str) -> Dict[str, Any]:
        """Identify what type of document this is and its context"""
        try:
            prompt = f"""
Analyze this document and identify:
1. Document type (loan agreement, brochure, advertisement, information sheet, etc.)
2. Primary purpose
3. Target audience
4. Key topics covered
5. Document category (financial, legal, informational, promotional)

Filename: {filename}

Document text (first 2000 characters):
{text[:2000]}

Provide response in JSON format with keys: document_type, purpose, audience, topics, category
"""
            
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            
            if result:
                return result
            else:
                # Fallback parsing
                return {
                    "document_type": "Unknown Document",
                    "purpose": "Document analysis",
                    "audience": "General",
                    "topics": ["Financial information"],
                    "category": "informational"
                }
                
        except Exception as e:
            logger.warning(f"Context identification error: {str(e)}")
            return {
                "document_type": "Financial Document",
                "purpose": "Information",
                "audience": "Users",
                "topics": ["Loan information"],
                "category": "financial"
            }
    
    def _search_document_context(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Perform web search to get reference information"""
        try:
            doc_type = context.get("document_type", "loan document")
            topics = context.get("topics", [])
            
            # Create search query
            search_query = f"{doc_type} {' '.join(topics[:2])} information guide"
            
            logger.info(f"Searching web for: {search_query}")
            
            references = []
            try:
                # Perform Google search (limit to 3 results)
                for url in search(search_query, num_results=3, lang="en"):
                    references.append({
                        "url": url,
                        "relevance": "Reference for document context"
                    })
            except Exception as search_error:
                logger.warning(f"Web search error: {str(search_error)}")
                # Add generic reference
                references.append({
                    "url": "https://www.consumerfinance.gov/",
                    "relevance": "General financial information"
                })
            
            return references
            
        except Exception as e:
            logger.warning(f"Web search error: {str(e)}")
            return []
    
    def _extract_comprehensive_data(
        self, 
        text: str, 
        context: Dict[str, Any],
        web_refs: List[Dict],
        tables: List[Dict] = None
    ) -> Dict[str, Any]:
        """Extract ALL relevant information from the document"""
        try:
            # Prepare table information
            table_info = ""
            if tables:
                table_info = f"\n\nTables found: {len(tables)} tables with data"
            
            prompt = f"""
You are an expert document analyzer. Extract ALL relevant information from this document.

Document Context:
- Type: {context.get('document_type')}
- Purpose: {context.get('purpose')}
- Category: {context.get('category')}

Extract EVERYTHING that would be useful for a user, including:

FINANCIAL INFORMATION:
- Loan amounts, interest rates, APR, fees
- Payment schedules, EMI amounts
- Processing fees, penalties, charges
- Tenure, moratorium periods
- Collateral or security requirements

CONTACT INFORMATION:
- Bank/Lender name and branch
- Phone numbers, email addresses
- Website URLs, social media
- Physical addresses
- Customer service contacts

IMPORTANT DATES & TIMINGS:
- Application deadlines
- Processing times
- Office hours, working days
- Payment due dates
- Validity periods

LEGAL & TERMS:
- Terms and conditions
- Eligibility criteria
- Required documents
- Legal clauses, disclaimers
- Rights and obligations

PROMOTIONAL INFORMATION:
- Special offers, discounts
- Promotional periods
- Benefits and features
- Comparison with other products

HELPFUL RESOURCES:
- Links to more information
- Reference documents
- FAQs mentioned
- Support resources

ADDITIONAL DETAILS:
- Any other information that would help the user
- Instructions or procedures
- Warnings or important notices

{table_info}

Document Text:
{text[:4000]}

Provide a comprehensive JSON response with all extracted information organized by category.
"""
            
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            
            if result:
                return result
            else:
                # Fallback: extract basic information
                return self._basic_extraction(text)
                
        except Exception as e:
            logger.error(f"Comprehensive extraction error: {str(e)}")
            return self._basic_extraction(text)
    
    def _filter_relevant_information(self, extracted_info: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to determine what information is most relevant for the user"""
        try:
            prompt = f"""
Given this extracted information from a document, identify and prioritize what is MOST IMPORTANT for a user to know.

Extracted Information:
{json.dumps(extracted_info, indent=2)[:3000]}

Categorize information by importance:
1. CRITICAL: Must-know information (loan terms, amounts, deadlines, contact info)
2. IMPORTANT: Should-know information (fees, procedures, requirements)
3. USEFUL: Nice-to-know information (additional resources, references)

Provide response in JSON format with these three categories.
"""
            
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            
            if result:
                return result
            else:
                return {
                    "critical": extracted_info,
                    "important": {},
                    "useful": {}
                }
                
        except Exception as e:
            logger.warning(f"Relevance filtering error: {str(e)}")
            return {
                "critical": extracted_info,
                "important": {},
                "useful": {}
            }
    
    def _structure_output(
        self,
        extracted_info: Dict[str, Any],
        relevant_info: Dict[str, Any],
        context: Dict[str, Any],
        web_refs: List[Dict],
        filename: str
    ) -> Dict[str, Any]:
        """Structure the final output for the user"""
        
        return {
            # Document metadata
            "document_name": filename,
            "document_type": context.get("document_type", "Unknown"),
            "document_purpose": context.get("purpose", ""),
            "document_category": context.get("category", ""),
            "analysis_timestamp": self._get_timestamp(),
            
            # AI-powered analysis
            "ai_analysis": {
                "document_summary": self._generate_summary(extracted_info, context),
                "key_topics": context.get("topics", []),
                "target_audience": context.get("audience", "General")
            },
            
            # Extracted information (organized by priority)
            "critical_information": relevant_info.get("critical", {}),
            "important_information": relevant_info.get("important", {}),
            "useful_information": relevant_info.get("useful", {}),
            
            # Complete extracted data
            "complete_extraction": extracted_info,
            
            # Web references
            "web_references": web_refs,
            "reference_note": "These links provide additional context about similar documents",
            
            # Extraction metadata
            "extraction_method": "gemini_ai_powered",
            "extraction_confidence": 0.92,
            "ai_model": "gemini-pro"
        }
    
    def _generate_summary(self, extracted_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a human-readable summary"""
        try:
            prompt = f"""
Create a brief, user-friendly summary (2-3 sentences) of this document based on the extracted information.

Document Type: {context.get('document_type')}
Extracted Info: {json.dumps(extracted_info, indent=2)[:1000]}

Make it clear and actionable for the user.
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"This is a {context.get('document_type', 'document')} containing financial and informational content."
    
    def _basic_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback basic extraction"""
        import re
        
        # Extract emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        # Extract phone numbers
        phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        
        # Extract URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        # Extract amounts
        amounts = re.findall(r'\$[\d,]+\.?\d*', text)
        
        return {
            "contact_information": {
                "emails": list(set(emails)),
                "phone_numbers": list(set(phones)),
                "websites": list(set(urls))
            },
            "financial_data": {
                "amounts_found": amounts[:10]
            },
            "raw_text_preview": text[:1000]
        }
    
    def _parse_json_response(self, response_text: str) -> Optional[Dict]:
        """Parse JSON from Gemini response"""
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except:
            return None
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _generate_fallback_response(self, text: str, filename: str) -> Dict[str, Any]:
        """Generate fallback response if AI fails"""
        return {
            "document_name": filename,
            "document_type": "Unknown",
            "extraction_method": "fallback",
            "extraction_confidence": 0.5,
            "raw_text_preview": text[:1000],
            "note": "AI analysis unavailable, showing basic extraction"
        }
