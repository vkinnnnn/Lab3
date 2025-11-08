/**
 * TypeScript Type Definitions
 * Following KIRO Global Steering Guidelines
 */

// Language Types
export type LanguageCode = 'en' | 'hi' | 'te' | 'ta' | 'es' | 'zh-cn' | 'fr' | 'de' | 'pt' | 'ru';

export interface Language {
  code: LanguageCode;
  name: string;
  native: string;
}

// Document Types
export interface DocumentMetadata {
  document_id: string;
  document_name: string;
  file_type: string;
  file_size: number;
  page_count: number;
  uploaded_at: string;
}

export interface NormalizedData {
  principal_amount: number;
  interest_rate: number;
  tenure_months: number;
  monthly_payment: number;
  bank_name: string;
  loan_type: string;
  processing_fee?: number;
  other_fees?: number;
}

export interface ExtractionResult {
  document_id: string;
  document_name: string;
  normalized_data: NormalizedData;
  complete_extraction: {
    text_extraction: {
      all_text: string;
    };
  };
  accuracy_metrics: {
    overall_accuracy: number;
    form_field_confidence: number;
  };
  processors_used: string[];
  processed_at: string;
}

// Chatbot Types
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: any;
}

export interface ChatResponse {
  answer: string;
  sources: Array<{ type: string; data: string }>;
  confidence: number;
  context_used: boolean;
  processing_time_ms: number;
}

// Comparison Types
export interface LoanMetrics {
  loan_id: string;
  bank_name: string;
  principal: number;
  interest_rate: number;
  tenure_months: number;
  monthly_payment: number;
  total_cost: number;
  total_interest: number;
  effective_rate: number;
  upfront_costs: number;
  processing_fee: number;
  other_fees: number;
}

export interface FlexibilityScore {
  loan_id: string;
  bank_name: string;
  score: number;
  features: string[];
  details: Record<string, boolean>;
}

export interface ProsCons {
  loan_id: string;
  bank_name: string;
  pros: string[];
  cons: string[];
  summary: string;
}

export interface ComparisonResult {
  loans: Array<{ document_id: string; document_name: string; bank_name: string }>;
  metrics: LoanMetrics[];
  flexibility_scores: FlexibilityScore[];
  pros_cons: ProsCons[];
  best_overall: string;
  best_by_category: Record<string, string>;
  recommendation: string;
  comparison_date: string;
}

// Financial Education Types
export interface FinancialTerm {
  term: string;
  category: string;
  simple_explanation: string;
  detailed_explanation: string;
  example: string;
  why_it_matters: string;
  related_terms: string[];
  translations: Record<string, string>;
}

export interface ScenarioResult {
  scenario_type: string;
  inputs: Record<string, any>;
  outputs: Record<string, any>;
  explanation: string;
  visualization_data?: any;
}

export interface BestPractice {
  title: string;
  category: string;
  description: string;
  importance: 'high' | 'medium' | 'low';
  applicable_to: string[];
  action_items: string[];
}

export interface LearningModule {
  order: number;
  title: string;
  topics: string[];
  estimated_time: string;
}

export interface LearningPath {
  title: string;
  description: string;
  modules: LearningModule[];
  total_time: string;
  certification: string;
}

// UI State Types
export interface Toast {
  id: string;
  title: string;
  description?: string;
  variant?: 'default' | 'destructive' | 'success';
}

export interface UploadProgress {
  fileName: string;
  progress: number;
  status: 'uploading' | 'processing' | 'complete' | 'error';
  error?: string;
}

// API Response Types
export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
