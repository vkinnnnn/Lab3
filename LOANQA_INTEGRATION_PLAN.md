# LoanQA Integration Implementation Plan

**Status**: Ready for Implementation  
**Date**: 2025-11-08  
**System**: Lab3 Student Loan Intelligence + LoanQA MLOps

---

## 📋 Executive Summary

This document outlines the implementation plan to complete the integration between Lab3's document extraction system and LoanQA's semantic Q&A capabilities, creating a unified loan intelligence platform.

### Current Status

✅ **Already Implemented:**
- Document extraction pipeline (Google Document AI)
- Normalization and validation layer
- RAG Chatbot service skeleton (template-based)
- Comparison engine (fully functional)
- Database storage layer (basic)
- Frontend with chat interface
- API endpoints structure

⚠️ **Missing for Full Integration:**
- Vector store (ChromaDB/similar) for semantic search
- LLM API integration (OpenAI/Anthropic)
- Document chunking and embedding pipeline
- Hybrid query router (SQL + Vector)
- Enhanced database schema for vector data
- Vector index with metadata enrichment

---

## 🎯 Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER UPLOADS DOCUMENT                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              LAB3 EXTRACTION (Already Built ✅)              │
│  • Google Document AI                                        │
│  • Field extraction (principal, rate, term, fees)           │
│  • Normalization & validation                               │
│  • Output: Structured JSON + Full Text                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌──────────────────┐        ┌──────────────────────┐
│  STRUCTURED      │        │  UNSTRUCTURED        │
│  DATA PATH       │        │  TEXT PATH           │
│  (SQL)           │        │  (VECTOR)            │
│                  │        │                      │
│  ✅ Database     │        │  ⚠️ Need to Build:   │
│     Storage      │        │  • ChromaDB store    │
│                  │        │  • Chunking          │
│  ⚠️ Need Schema: │        │  • Embeddings        │
│  • loan_fields   │        │  • Metadata index    │
│  • Quick filters │        │                      │
└──────────────────┘        └──────────────────────┘
         │                           │
         └─────────────┬─────────────┘
                       ▼
         ┌──────────────────────────┐
         │  ⚠️ HYBRID QUERY ROUTER   │
         │  (Need to Build)         │
         │                          │
         │  Detects query type:     │
         │  • Structured → SQL      │
         │  • Semantic → Vector     │
         │  • Mixed → Both          │
         └─────────────┬────────────┘
                       ▼
         ┌──────────────────────────┐
         │  ⚠️ LLM INTEGRATION       │
         │  (Need to Build)         │
         │                          │
         │  • OpenAI GPT-4          │
         │  • Anthropic Claude      │
         │  • Context from both     │
         │    SQL + Vector          │
         │  • Confidence validation │
         └─────────────┬────────────┘
                       ▼
         ┌──────────────────────────┐
         │   RESPONSE TO USER       │
         │   with:                  │
         │   • Answer               │
         │   • Sources              │
         │   • Confidence           │
         │   • Charts (if needed)   │
         └──────────────────────────┘
```

---

## 📦 Implementation Tasks

### **Phase 1: Foundation (Week 1)**

#### Task 1.1: Add API Keys
**File**: `.env`
```env
# AI/LLM Configuration
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM=gpt-4-turbo

# Vector Store Configuration
CHROMADB_HOST=localhost
CHROMADB_PORT=8001
EMBEDDING_MODEL=text-embedding-3-small
```

#### Task 1.2: Install Dependencies
**File**: `requirements.txt`
```txt
# Add these:
chromadb>=0.4.22
openai>=1.12.0
anthropic>=0.18.0
langchain>=0.1.11
langchain-openai>=0.0.8
sentence-transformers>=2.3.1
tiktoken>=0.6.0
```

#### Task 1.3: Enhanced Database Schema
**File**: `storage/migrations/add_vector_tables.sql`
```sql
-- Document chunks for vector storage
CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    page_number INT,
    section_type VARCHAR(100),
    token_count INT,
    
    -- Metadata from Lab3 extraction
    related_loan_id UUID REFERENCES loans(loan_id),
    extraction_confidence DECIMAL(3, 2),
    
    -- Vector data (stored as binary or external in ChromaDB)
    embedding_model VARCHAR(100),
    embedding_id VARCHAR(255),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);

-- Chat conversations
CREATE TABLE IF NOT EXISTS chat_conversations (
    conversation_id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id),
    user_id VARCHAR(255),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_at TIMESTAMP,
    message_count INT DEFAULT 0
);

-- Chat messages
CREATE TABLE IF NOT EXISTS chat_messages (
    message_id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES chat_conversations(conversation_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    
    -- Context used
    chunks_used UUID[],
    structured_data_used JSONB,
    
    -- Metadata
    confidence DECIMAL(3, 2),
    processing_time_ms INT,
    llm_model VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced loans table with query optimization
ALTER TABLE loans ADD COLUMN IF NOT EXISTS tsv_search tsvector;

CREATE INDEX IF NOT EXISTS idx_chunks_document ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_loan ON document_chunks(related_loan_id);
CREATE INDEX IF NOT EXISTS idx_chunks_page ON document_chunks(page_number);
CREATE INDEX IF NOT EXISTS idx_chat_conversation ON chat_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_chat_document ON chat_conversations(document_id);

-- Full-text search on loans
CREATE INDEX IF NOT EXISTS idx_loans_tsv ON loans USING GIN(tsv_search);

-- Function to update tsvector
CREATE OR REPLACE FUNCTION loans_tsv_trigger() RETURNS trigger AS $$
BEGIN
    NEW.tsv_search :=
        setweight(to_tsvector('english', COALESCE(NEW.bank_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.loan_type, '')), 'B');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update_loans 
    BEFORE INSERT OR UPDATE ON loans
    FOR EACH ROW EXECUTE FUNCTION loans_tsv_trigger();
```

---

### **Phase 2: Vector Store Implementation (Week 2)**

#### Task 2.1: Vector Store Manager
**File**: `src/services/vector_store.py`
```python
"""
Vector Store Manager for Semantic Search
Integrates ChromaDB with Lab3 extraction metadata
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import openai
from sentence_transformers import SentenceTransformer
import logging
import uuid

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manages vector storage and retrieval for document chunks"""
    
    def __init__(
        self,
        chroma_host: str = "localhost",
        chroma_port: int = 8001,
        embedding_model: str = "text-embedding-3-small",
        use_openai: bool = True
    ):
        """Initialize vector store"""
        self.use_openai = use_openai
        self.embedding_model = embedding_model
        
        # Initialize ChromaDB
        self.client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="loan_documents",
            metadata={"description": "Student loan document chunks with metadata"}
        )
        
        # Initialize embedding model
        if not use_openai:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        logger.info(f"Vector store initialized with {self.collection.count()} chunks")
    
    def add_document_chunks(
        self,
        document_id: str,
        chunks: List[str],
        metadatas: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Add document chunks to vector store
        
        Args:
            document_id: Document identifier
            chunks: List of text chunks
            metadatas: Metadata for each chunk (from Lab3 extraction)
            
        Returns:
            List of chunk IDs
        """
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        
        # Enrich metadata with document_id
        for meta in metadatas:
            meta['document_id'] = document_id
        
        # Generate embeddings
        embeddings = self._generate_embeddings(chunks)
        
        # Add to ChromaDB
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=chunk_ids
        )
        
        logger.info(f"Added {len(chunks)} chunks for document {document_id}")
        return chunk_ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        document_filter: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for relevant chunks
        
        Args:
            query: Search query
            n_results: Number of results to return
            document_filter: Filter by document_id
            metadata_filter: Additional metadata filters
            
        Returns:
            Search results with chunks and metadata
        """
        # Build where filter
        where_filter = {}
        if document_filter:
            where_filter['document_id'] = document_filter
        if metadata_filter:
            where_filter.update(metadata_filter)
        
        # Generate query embedding
        query_embedding = self._generate_embeddings([query])[0]
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        return {
            'chunks': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0],
            'ids': results['ids'][0]
        }
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts"""
        if self.use_openai:
            response = openai.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            return [item.embedding for item in response.data]
        else:
            return self.sentence_model.encode(texts).tolist()
    
    def delete_document(self, document_id: str) -> int:
        """Delete all chunks for a document"""
        results = self.collection.get(
            where={"document_id": document_id}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
            return len(results['ids'])
        return 0
```

#### Task 2.2: Document Chunking Service
**File**: `src/services/chunking.py`
```python
"""
Document Chunking Service
Chunks documents for vector storage while preserving context
"""

from typing import List, Dict, Any, Tuple
import re
import tiktoken


class DocumentChunker:
    """Chunks documents intelligently for vector storage"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        model: str = "gpt-4"
    ):
        """
        Initialize chunker
        
        Args:
            chunk_size: Target chunk size in tokens
            chunk_overlap: Overlap between chunks
            model: Model name for token counting
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.encoding_for_model(model)
    
    def chunk_document(
        self,
        text: str,
        structured_data: Dict[str, Any],
        document_id: str
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Chunk document with metadata
        
        Args:
            text: Full document text
            structured_data: Lab3 extracted data
            document_id: Document identifier
            
        Returns:
            (chunks, metadatas) tuple
        """
        # Split into paragraphs
        paragraphs = self._split_paragraphs(text)
        
        # Create chunks
        chunks = []
        metadatas = []
        
        current_chunk = []
        current_tokens = 0
        chunk_index = 0
        
        for para in paragraphs:
            para_tokens = len(self.encoding.encode(para))
            
            if current_tokens + para_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = "\n\n".join(current_chunk)
                chunks.append(chunk_text)
                
                # Create metadata enriched with Lab3 data
                metadata = self._create_metadata(
                    chunk_text,
                    structured_data,
                    chunk_index
                )
                metadatas.append(metadata)
                
                # Start new chunk with overlap
                current_chunk = current_chunk[-1:] if current_chunk else []
                current_tokens = len(self.encoding.encode("\n\n".join(current_chunk)))
                chunk_index += 1
            
            current_chunk.append(para)
            current_tokens += para_tokens
        
        # Add final chunk
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunks.append(chunk_text)
            metadatas.append(
                self._create_metadata(chunk_text, structured_data, chunk_index)
            )
        
        return chunks, metadatas
    
    @staticmethod
    def _split_paragraphs(text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split on double newlines or large spaces
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    @staticmethod
    def _create_metadata(
        chunk_text: str,
        structured_data: Dict[str, Any],
        chunk_index: int
    ) -> Dict[str, Any]:
        """Create metadata for chunk"""
        # Detect section type
        section_type = "general"
        lower_text = chunk_text.lower()
        
        if any(kw in lower_text for kw in ['payment', 'emi', 'schedule']):
            section_type = "payment_terms"
        elif any(kw in lower_text for kw in ['interest', 'rate', 'apr']):
            section_type = "interest_terms"
        elif any(kw in lower_text for kw in ['fee', 'charge', 'cost']):
            section_type = "fees"
        elif any(kw in lower_text for kw in ['default', 'late', 'penalty']):
            section_type = "penalties"
        
        return {
            'chunk_index': chunk_index,
            'section_type': section_type,
            'bank_name': structured_data.get('bank_name', ''),
            'loan_type': structured_data.get('loan_type', ''),
            'principal': structured_data.get('principal_amount', 0),
            'interest_rate': structured_data.get('interest_rate', 0),
            'extraction_confidence': structured_data.get(
                'accuracy_metrics', {}
            ).get('overall_accuracy', 0),
            'token_count': len(chunk_text.split())
        }
```

---

### **Phase 3: LLM Integration (Week 3)**

#### Task 3.1: LLM Service Manager
**File**: `src/services/llm_service.py`
```python
"""
LLM Service Manager
Unified interface for OpenAI and Anthropic
"""

from typing import List, Dict, Any, Optional
import openai
from anthropic import Anthropic
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM response"""
    content: str
    model: str
    tokens_used: int
    finish_reason: str


class LLMService:
    """Unified LLM service"""
    
    def __init__(
        self,
        openai_key: str,
        anthropic_key: str,
        default_provider: str = "openai"
    ):
        """Initialize LLM clients"""
        self.openai_client = openai.OpenAI(api_key=openai_key)
        self.anthropic_client = Anthropic(api_key=anthropic_key)
        self.default_provider = default_provider
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        provider: Optional[str] = None
    ) -> LLMResponse:
        """
        Send chat completion request
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (or None for default)
            temperature: Response randomness
            max_tokens: Maximum response length
            provider: 'openai' or 'anthropic'
            
        Returns:
            LLMResponse
        """
        provider = provider or self.default_provider
        
        if provider == "openai":
            return self._openai_chat(messages, model, temperature, max_tokens)
        else:
            return self._anthropic_chat(messages, model, temperature, max_tokens)
    
    def _openai_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> LLMResponse:
        """OpenAI chat completion"""
        model = model or "gpt-4-turbo-preview"
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=model,
            tokens_used=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason
        )
    
    def _anthropic_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> LLMResponse:
        """Anthropic chat completion"""
        model = model or "claude-3-sonnet-20240229"
        
        # Convert to Anthropic format (extract system message)
        system_msg = ""
        user_messages = []
        
        for msg in messages:
            if msg['role'] == 'system':
                system_msg = msg['content']
            else:
                user_messages.append(msg)
        
        response = self.anthropic_client.messages.create(
            model=model,
            system=system_msg,
            messages=user_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return LLMResponse(
            content=response.content[0].text,
            model=model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            finish_reason=response.stop_reason
        )
```

#### Task 3.2: Update RAG Chatbot with Real LLM
**File**: `src/api/services/rag_chatbot_service.py` (UPDATE existing)

Add after imports:
```python
from src.services.vector_store import VectorStoreManager
from src.services.llm_service import LLMService
import os
```

Update `__init__` method:
```python
def __init__(self, vector_store=None, use_llm: bool = True):
    """Initialize with real vector store and LLM"""
    self.use_llm = use_llm
    self.memory = ConversationMemory()
    self.calculator = FinancialScenarioCalculator()
    
    # Initialize vector store
    self.vector_store = vector_store or VectorStoreManager(
        chroma_host=os.getenv('CHROMADB_HOST', 'localhost'),
        chroma_port=int(os.getenv('CHROMADB_PORT', '8001'))
    )
    
    # Initialize LLM service
    if use_llm:
        self.llm_service = LLMService(
            openai_key=os.getenv('OPENAI_API_KEY'),
            anthropic_key=os.getenv('ANTHROPIC_API_KEY'),
            default_provider=os.getenv('DEFAULT_LLM', 'openai')
        )
```

Update `_handle_document_question` method:
```python
def _handle_document_question(
    self,
    question: str,
    document_id: str,
    structured_data: Optional[Dict[str, Any]]
) -> ChatResponse:
    """Handle questions with real RAG"""
    
    # Search vector store
    search_results = self.vector_store.search(
        query=question,
        n_results=5,
        document_filter=document_id
    )
    
    # Build context from retrieved chunks
    context_chunks = search_results['chunks']
    context_text = "\n\n---\n\n".join(context_chunks)
    
    # Build prompt with structured data validation
    messages = [
        {
            'role': 'system',
            'content': self.SYSTEM_PROMPT
        },
        {
            'role': 'user',
            'content': f"""Document Context:
{context_text}

Verified Loan Details (Lab3 Extraction):
• Principal: ${structured_data.get('principal_amount', 'N/A'):,.2f}
• Interest Rate: {structured_data.get('interest_rate', 'N/A')}%
• Term: {structured_data.get('tenure_months', 'N/A')} months
• Extraction Confidence: {structured_data.get('accuracy_metrics', {}).get('overall_accuracy', 'N/A')}

User Question: {question}

Please answer based on the document context. Cross-check any numbers with the verified details above."""
        }
    ]
    
    # Get LLM response
    llm_response = self.llm_service.chat(
        messages=messages,
        temperature=0.7,
        max_tokens=1500
    )
    
    # Build sources from search results
    sources = [
        {
            'chunk_id': cid,
            'text_preview': chunk[:100] + '...',
            'confidence': 1.0 - dist,
            'metadata': meta
        }
        for cid, chunk, dist, meta in zip(
            search_results['ids'],
            search_results['chunks'],
            search_results['distances'],
            search_results['metadatas']
        )
    ]
    
    return ChatResponse(
        answer=llm_response.content,
        sources=sources,
        confidence=0.9,  # Could be calculated based on retrieval scores
        context_used=True,
        processing_time_ms=0.0
    )
```

---

### **Phase 4: Hybrid Query Router (Week 4)**

#### Task 4.1: Query Router
**File**: `src/services/query_router.py`
```python
"""
Hybrid Query Router
Routes queries to SQL, Vector, or both based on intent
"""

from typing import Dict, Any, List, Tuple
from enum import Enum
import re


class QueryType(Enum):
    """Query types"""
    STRUCTURED = "structured"  # SQL query
    SEMANTIC = "semantic"      # Vector search
    HYBRID = "hybrid"          # Both
    CALCULATION = "calculation"  # Financial calc


class QueryRouter:
    """Routes user queries to appropriate backend"""
    
    # Keywords for structured queries
    STRUCTURED_KEYWORDS = [
        'compare', 'filter', 'show', 'list', 'find all',
        'under', 'over', 'between', 'highest', 'lowest',
        'which loan', 'how many', 'total'
    ]
    
    # Keywords for semantic queries
    SEMANTIC_KEYWORDS = [
        'what is', 'what are', 'what happens', 'explain',
        'tell me about', 'describe', 'why', 'how does',
        'what if i miss', 'can i', 'prepayment', 'policy'
    ]
    
    # Keywords for calculations
    CALC_KEYWORDS = [
        'calculate', 'extra payment', 'pay more', 'save',
        'if i pay', 'shorter term', 'compare tenure'
    ]
    
    @classmethod
    def route_query(cls, question: str) -> Tuple[QueryType, Dict[str, Any]]:
        """
        Determine query type and extract parameters
        
        Args:
            question: User question
            
        Returns:
            (query_type, parameters) tuple
        """
        question_lower = question.lower()
        
        # Check for calculation
        if any(kw in question_lower for kw in cls.CALC_KEYWORDS):
            return QueryType.CALCULATION, cls._extract_calc_params(question)
        
        # Check for structured query
        is_structured = any(kw in question_lower for kw in cls.STRUCTURED_KEYWORDS)
        has_numbers = bool(re.search(r'\$?\d+[,\d]*', question))
        has_comparison = any(word in question_lower for word in ['compare', 'vs', 'versus'])
        
        if is_structured or (has_numbers and has_comparison):
            params = cls._extract_structured_params(question)
            
            # Check if also needs semantic search
            if any(kw in question_lower for kw in cls.SEMANTIC_KEYWORDS):
                return QueryType.HYBRID, params
            else:
                return QueryType.STRUCTURED, params
        
        # Default to semantic
        return QueryType.SEMANTIC, {}
    
    @staticmethod
    def _extract_structured_params(question: str) -> Dict[str, Any]:
        """Extract parameters from structured query"""
        params = {}
        
        # Extract amount filters
        amount_match = re.search(r'\$?(\d+[,\d]*)', question)
        if amount_match:
            amount = float(amount_match.group(1).replace(',', ''))
            
            if 'under' in question.lower() or 'below' in question.lower():
                params['max_principal'] = amount
            elif 'over' in question.lower() or 'above' in question.lower():
                params['min_principal'] = amount
        
        # Extract loan type
        if 'education' in question.lower():
            params['loan_type'] = 'education'
        elif 'personal' in question.lower():
            params['loan_type'] = 'personal'
        
        # Extract bank name
        bank_match = re.search(r'from ([\w\s]+?)(?:\s+bank)?(?:\s+and|\s+$)', question, re.IGNORECASE)
        if bank_match:
            params['bank_name'] = bank_match.group(1).strip()
        
        return params
    
    @staticmethod
    def _extract_calc_params(question: str) -> Dict[str, Any]:
        """Extract calculation parameters"""
        params = {}
        
        # Extract extra payment amount
        amount_match = re.search(r'\$?(\d+[,\d]*)', question)
        if amount_match:
            params['extra_payment'] = float(amount_match.group(1).replace(',', ''))
        
        return params
```

#### Task 4.2: Unified Query Handler
**File**: `src/api/routes_integration.py` (NEW)
```python
"""
Unified Query API
Combines structured SQL + semantic vector search
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from src.services.query_router import QueryRouter, QueryType
from src.services.vector_store import VectorStoreManager
from src.services.llm_service import LLMService
from src.api.services.rag_chatbot_service import financial_chatbot
from storage.database import DatabaseManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/integration", tags=["Integration"])


class UnifiedQueryRequest(BaseModel):
    """Unified query request"""
    question: str
    document_id: Optional[str] = None
    user_id: Optional[str] = None


class UnifiedQueryResponse(BaseModel):
    """Unified query response"""
    answer: str
    query_type: str
    sources: list
    structured_results: Optional[Dict[str, Any]] = None
    confidence: float
    processing_time_ms: float


@router.post("/query", response_model=UnifiedQueryResponse)
async def unified_query(request: UnifiedQueryRequest):
    """
    Unified query endpoint - automatically routes to appropriate backend
    
    Examples:
    - "Show loans under $10k" → Structured SQL query
    - "What's the prepayment policy?" → Semantic vector search
    - "Compare loans under $15k and show their late fees" → Hybrid (both)
    """
    try:
        # Route query
        query_type, params = QueryRouter.route_query(request.question)
        
        if query_type == QueryType.STRUCTURED:
            return await _handle_structured_query(request, params)
        
        elif query_type == QueryType.SEMANTIC:
            return await _handle_semantic_query(request)
        
        elif query_type == QueryType.HYBRID:
            return await _handle_hybrid_query(request, params)
        
        else:  # CALCULATION
            return await _handle_calculation_query(request, params)
    
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


async def _handle_structured_query(
    request: UnifiedQueryRequest,
    params: Dict[str, Any]
) -> UnifiedQueryResponse:
    """Handle structured SQL query"""
    # Build SQL query
    query = "SELECT * FROM loans WHERE 1=1"
    query_params = []
    
    if 'max_principal' in params:
        query += " AND principal_amount <= %s"
        query_params.append(params['max_principal'])
    
    if 'min_principal' in params:
        query += " AND principal_amount >= %s"
        query_params.append(params['min_principal'])
    
    if 'loan_type' in params:
        query += " AND loan_type = %s"
        query_params.append(params['loan_type'])
    
    # Execute query
    db = DatabaseManager(os.getenv('DATABASE_URL'))
    results = db.execute_query(query, tuple(query_params))
    
    # Format response
    if results:
        answer = f"Found {len(results)} matching loans:\n\n"
        for loan in results[:5]:  # Top 5
            answer += f"• **{loan['bank_name']}**: ${loan['principal_amount']:,.2f} at {loan['interest_rate']}% for {loan['tenure_months']} months\n"
    else:
        answer = "No loans found matching your criteria."
    
    return UnifiedQueryResponse(
        answer=answer,
        query_type="structured",
        sources=[{"type": "database", "count": len(results)}],
        structured_results={"loans": results},
        confidence=0.95,
        processing_time_ms=100
    )


async def _handle_semantic_query(request: UnifiedQueryRequest) -> UnifiedQueryResponse:
    """Handle semantic vector search query"""
    # Use existing RAG chatbot
    response = financial_chatbot.ask(
        question=request.question,
        document_id=request.document_id or "",
        structured_data={},
        use_memory=False
    )
    
    return UnifiedQueryResponse(
        answer=response.answer,
        query_type="semantic",
        sources=response.sources,
        confidence=response.confidence,
        processing_time_ms=response.processing_time_ms
    )


async def _handle_hybrid_query(
    request: UnifiedQueryRequest,
    params: Dict[str, Any]
) -> UnifiedQueryResponse:
    """Handle hybrid query (SQL + Vector)"""
    # Step 1: Get structured data (SQL)
    sql_response = await _handle_structured_query(request, params)
    filtered_loans = sql_response.structured_results['loans']
    
    # Step 2: For each loan, answer semantic question
    semantic_question = request.question
    # Extract semantic part (after 'and')
    if ' and ' in semantic_question.lower():
        semantic_question = semantic_question.split(' and ', 1)[1]
    
    combined_answer = f"Based on your filters, I found {len(filtered_loans)} loans:\n\n"
    
    for loan in filtered_loans[:3]:  # Top 3
        # Get semantic answer for this specific loan
        loan_response = financial_chatbot.ask(
            question=semantic_question,
            document_id=loan['document_id'],
            structured_data=loan['extracted_data'],
            use_memory=False
        )
        
        combined_answer += f"**{loan['bank_name']}** (${loan['principal_amount']:,.2f}):\n"
        combined_answer += f"{loan_response.answer}\n\n"
    
    return UnifiedQueryResponse(
        answer=combined_answer,
        query_type="hybrid",
        sources=[
            {"type": "structured", "count": len(filtered_loans)},
            {"type": "semantic", "provider": "vector_search"}
        ],
        structured_results={"loans": filtered_loans},
        confidence=0.88,
        processing_time_ms=500
    )


async def _handle_calculation_query(
    request: UnifiedQueryRequest,
    params: Dict[str, Any]
) -> UnifiedQueryResponse:
    """Handle financial calculation"""
    response = financial_chatbot.ask(
        question=request.question,
        document_id=request.document_id or "",
        structured_data={},  # Would need to fetch from DB
        use_memory=False
    )
    
    return UnifiedQueryResponse(
        answer=response.answer,
        query_type="calculation",
        sources=response.sources,
        confidence=response.confidence,
        processing_time_ms=response.processing_time_ms
    )
```

---

### **Phase 5: Pipeline Integration (Week 5)**

#### Task 5.1: Update Extraction Pipeline
**File**: `src/services/extraction_pipeline.py` (NEW)
```python
"""
Complete Extraction → Vector Store Pipeline
"""

from src.services.vector_store import VectorStoreManager
from src.services.chunking import DocumentChunker
from storage.storage_service import StorageService
import logging

logger = logging.getLogger(__name__)


class IntegratedExtractionPipeline:
    """Complete pipeline: Extract → Normalize → Store → Index"""
    
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.chunker = DocumentChunker()
        self.storage = StorageService()
    
    async def process_document_complete(
        self,
        document_path: str,
        document_id: str
    ) -> Dict[str, Any]:
        """
        Complete pipeline:
        1. Extract with Google Document AI
        2. Normalize data
        3. Store in PostgreSQL
        4. Chunk and index in vector store
        """
        
        # Step 1: Extract (existing)
        from src.extraction.extraction_service import DataExtractionService
        extractor = DataExtractionService()
        
        with open(document_path, 'rb') as f:
            extracted = extractor.extract_loan_data(f.read())
        
        # Step 2: Normalize (existing)
        from normalization.field_mapper import FieldMapper
        from normalization.schema_validator import SchemaValidator
        
        mapper = FieldMapper()
        normalized = mapper.map_fields(extracted)
        
        validator = SchemaValidator()
        validation = validator.validate(normalized, document_id)
        
        # Step 3: Store structured data
        self.storage.store_extracted_data(
            document_id=document_id,
            extracted_data=validation.validated_data.model_dump()
        )
        
        # Step 4: Chunk and index
        full_text = extracted.get('complete_extraction', {}).get(
            'text_extraction', {}
        ).get('all_text', '')
        
        chunks, metadatas = self.chunker.chunk_document(
            text=full_text,
            structured_data=normalized,
            document_id=document_id
        )
        
        chunk_ids = self.vector_store.add_document_chunks(
            document_id=document_id,
            chunks=chunks,
            metadatas=metadatas
        )
        
        logger.info(f"Pipeline complete: {len(chunk_ids)} chunks indexed")
        
        return {
            'document_id': document_id,
            'structured_data': normalized,
            'chunks_created': len(chunk_ids),
            'validation_status': 'valid' if validation.is_valid else 'invalid',
            'warnings': validation.warnings
        }
```

---

## 📊 Testing Plan

### Test 1: Vector Store
```bash
# Start ChromaDB
docker run -d -p 8001:8000 chromadb/chroma

# Test script
python -m tests.test_vector_store
```

### Test 2: End-to-End
```bash
# Upload document → Extract → Index → Query
python -m tests.test_integration
```

### Test 3: Hybrid Queries
```bash
curl -X POST http://localhost:8000/integration/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show loans under $15k and explain their prepayment terms"
  }'
```

---

## 🚀 Deployment

### Docker Compose Update
Add to `docker-compose.yml`:
```yaml
  chromadb:
    image: chromadb/chroma:latest
    container_name: loan-extractor-chromadb
    ports:
      - "${CHROMADB_PORT:-8001}:8000"
    volumes:
      - chroma_data:/chroma/chroma
    networks:
      - loan-network
    environment:
      - IS_PERSISTENT=TRUE
```

---

## 📈 Success Metrics

✅ **Integration Complete When:**
1. Documents automatically indexed in vector store
2. Hybrid queries work (SQL + semantic)
3. LLM answers validated with structured data
4. <3s response time for semantic queries
5. >85% user query satisfaction
6. Confidence scores >90% for structured fields

---

## 🎯 Next Steps

1. **Week 1**: Set up environment (API keys, ChromaDB, DB migration)
2. **Week 2**: Implement vector store + chunking
3. **Week 3**: Integrate LLM services
4. **Week 4**: Build hybrid query router
5. **Week 5**: Connect pipeline + testing

**Ready to start? Begin with Phase 1, Task 1.1 - Adding API keys!**
