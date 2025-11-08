/**
 * ChatGPT-Style Chat Interface
 * Modern conversational AI with document upload
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Paperclip,
  Send,
  Sparkles,
  FileText,
  BarChart3,
  TrendingDown,
  Loader2,
  Check,
  Plus,
  Home,
} from 'lucide-react';
import Link from 'next/link';
import Confetti from 'react-confetti';
import { api, getErrorMessage } from '@/lib/api';
import { toast } from '@/components/ui/toaster';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  hasChart?: boolean;
  chartData?: any;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [showConfetti, setShowConfetti] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [documentId, setDocumentId] = useState<string>('');
  const [extractedData, setExtractedData] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Welcome message on load
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: '1',
          role: 'assistant',
          content: `👋 Welcome to LoanIQ! I'm your AI financial advisor.

I can help you:
• Analyze student loan documents
• Compare multiple loan offers
• Explain complex financial terms
• Calculate payment scenarios
• Provide personalized recommendations

Upload a loan document to get started, or ask me any question about student loans!`,
          timestamp: new Date(),
        },
      ]);
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Suggested prompts
  const suggestedPrompts = [
    '📄 Analyze my loan document',
    '📊 Compare loan offers',
    '💰 Calculate my monthly payment',
    '❓ Explain prepayment penalty',
  ];

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadedFile(file);

    // Add user message
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: `📎 Uploaded: ${file.name}`,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);

    // Start analysis
    setIsAnalyzing(true);
    setAnalysisProgress(0);

    // Progress simulation
    const progressInterval = setInterval(() => {
      setAnalysisProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 15;
      });
    }, 300);

    try {
      // Real API call to backend
      const response = await api.uploadDocument(file);
      const data = response.data;

      clearInterval(progressInterval);
      setAnalysisProgress(100);
      setDocumentId(data.document_id || Date.now().toString());
      setExtractedData(data.structured_data);

      // Success!
      setTimeout(() => {
        setIsAnalyzing(false);
        setShowConfetti(true);
        setTimeout(() => setShowConfetti(false), 3000);

        // Format the extracted data
        const structuredData = data.structured_data || {};
        const principal = structuredData.principal_amount || 'N/A';
        const rate = structuredData.interest_rate || 'N/A';
        const tenure = structuredData.tenure_months || 'N/A';
        const monthly = structuredData.monthly_payment || 'N/A';

        const aiMsg: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: `✅ Analysis Complete!

I've analyzed your loan document. Here's what I found:

**Loan Details:**
• Principal Amount: $${principal.toLocaleString()}
• Interest Rate: ${rate}% APR
• Tenure: ${tenure} months
• Monthly Payment: $${monthly.toLocaleString()}

**Key Insights:**
${structuredData.prepayment_allowed ? '✓ No prepayment penalty' : '⚠ Prepayment penalty may apply'}
${structuredData.processing_fee ? `⚠ Processing fee: $${structuredData.processing_fee}` : '✓ No processing fee'}

Would you like me to:
1. Compare with other loan offers
2. Show you payment scenarios
3. Explain any terms in detail`,
          timestamp: new Date(),
          hasChart: true,
        };

        setMessages((prev) => [...prev, aiMsg]);
      }, 500);
    } catch (error) {
      clearInterval(progressInterval);
      setIsAnalyzing(false);
      
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ Error analyzing document: ${getErrorMessage(error)}

Please try:
• Uploading a different file
• Ensuring the file is a valid PDF or image
• Checking your internet connection`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
      
      toast({
        title: 'Upload Error',
        description: getErrorMessage(error),
        variant: 'destructive',
      });
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    const question = input;
    setInput('');
    setIsTyping(true);

    try {
      // Real API call to chatbot
      const response = await api.askChatbot(
        question,
        documentId,
        extractedData,
        true
      );

      setIsTyping(false);

      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.answer || 'I apologize, but I could not process your question.',
        timestamp: new Date(),
        hasChart: question.toLowerCase().includes('compare'),
        chartData: question.toLowerCase().includes('compare')
          ? { type: 'comparison' }
          : undefined,
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      setIsTyping(false);
      
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I'm having trouble connecting to the server. ${getErrorMessage(error)}

Please check:
• Backend server is running (http://localhost:8000)
• Your internet connection
• Try uploading a document first`,
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMsg]);
    }
  };

  const handleSuggestedPrompt = (prompt: string) => {
    setInput(prompt.substring(2).trim());
  };

  return (
    <div className="flex h-screen flex-col bg-white">
      {showConfetti && <Confetti recycle={false} numberOfPieces={500} />}

      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex h-14 max-w-4xl items-center justify-between px-4">
          <Link href="/" className="flex items-center space-x-2 text-gray-900 hover:text-gray-700">
            <Home className="h-5 w-5" />
          </Link>
          <div className="flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-purple-600" />
            <span className="font-semibold">LoanIQ Chat</span>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setMessages([]);
              setUploadedFile(null);
              window.location.reload();
            }}
          >
            <Plus className="mr-2 h-4 w-4" />
            New Chat
          </Button>
        </div>
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-3xl px-4 py-8">
          <AnimatePresence>
            {messages.map((message, idx) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                transition={{ 
                  duration: 0.3, 
                  ease: [0.4, 0, 0.2, 1]
                }}
                className={`mb-6 flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-6 py-4 ${
                    message.role === 'user'
                      ? 'rounded-tr-sm bg-black text-white'
                      : 'rounded-tl-sm bg-gray-100 text-gray-900'
                  }`}
                >
                  {message.role === 'assistant' && (
                    <div className="mb-2 flex items-center text-xs text-gray-500">
                      <Sparkles className="mr-1 h-3 w-3" />
                      AI Assistant
                    </div>
                  )}
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                  </div>
                  
                  {/* Chart Display */}
                  {message.hasChart && message.chartData && (
                    <div className="mt-4 rounded-xl border border-gray-200 bg-white p-4">
                      <div className="mb-2 text-xs font-medium text-gray-600">
                        Comparison Chart
                      </div>
                      <div className="h-48 w-full rounded-lg bg-gradient-to-br from-purple-50 to-pink-50 flex items-center justify-center">
                        <BarChart3 className="h-16 w-16 text-purple-600" />
                      </div>
                      <div className="mt-2 text-xs text-gray-500">
                        <TrendingDown className="mr-1 inline h-3 w-3" />
                        You could save $138 with Option A
                      </div>
                    </div>
                  )}

                  <div className="mt-2 text-xs opacity-60">
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
              className="mb-6 flex justify-start"
            >
              <div className="rounded-2xl rounded-tl-sm bg-gray-100 px-6 py-4 shimmer">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400 dot-flashing"></div>
                    <div
                      className="h-2 w-2 animate-bounce rounded-full bg-gray-400 dot-flashing"
                      style={{ animationDelay: '0.2s' }}
                    ></div>
                    <div
                      className="h-2 w-2 animate-bounce rounded-full bg-gray-400 dot-flashing"
                      style={{ animationDelay: '0.4s' }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-500">AI is thinking...</span>
                </div>
              </div>
            </motion.div>
          )}

          {/* Analysis Progress */}
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
              className="mb-6"
            >
              <div className="rounded-xl border border-purple-200 bg-purple-50 p-4 animate-pulse-glow">
                <div className="mb-2 flex items-center text-sm font-medium text-purple-900">
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing document...
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-purple-200">
                  <motion.div
                    className="h-full bg-gradient-to-r from-purple-600 to-pink-600 shimmer"
                    initial={{ width: 0 }}
                    animate={{ width: `${analysisProgress}%` }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                  />
                </div>
                <div className="mt-2 text-xs text-purple-700">
                  {analysisProgress < 30 && 'Extracting loan details...'}
                  {analysisProgress >= 30 && analysisProgress < 60 && 'Analyzing terms...'}
                  {analysisProgress >= 60 && analysisProgress < 90 && 'Calculating scenarios...'}
                  {analysisProgress >= 90 && 'Finalizing analysis...'}
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Suggested Prompts (show when no messages) */}
      {messages.length === 1 && !isTyping && (
        <div className="mx-auto max-w-3xl px-4 pb-4">
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {suggestedPrompts.map((prompt, idx) => (
              <motion.button
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + idx * 0.1, duration: 0.3 }}
                onClick={() => handleSuggestedPrompt(prompt)}
                className="rounded-xl border border-gray-200 bg-white px-4 py-3 text-left text-sm hover-lift active-press hover:border-purple-300 hover:bg-purple-50"
              >
                {prompt}
              </motion.button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white">
        <div className="mx-auto max-w-3xl px-4 py-4">
          <div className="flex items-end space-x-2">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".pdf,.png,.jpg,.jpeg,.tiff"
              className="hidden"
            />
            <Button
              variant="outline"
              size="icon"
              onClick={() => fileInputRef.current?.click()}
              disabled={isAnalyzing}
              className="hover-lift active-press"
            >
              <Paperclip className="h-5 w-5" />
            </Button>
            <div className="relative flex-1">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                placeholder="Ask me anything about your loan..."
                disabled={isAnalyzing || isTyping}
                className="h-12 pr-12 text-base"
              />
              <Button
                onClick={handleSend}
                disabled={!input.trim() || isAnalyzing || isTyping}
                size="icon"
                className="absolute right-1 top-1 h-10 w-10 active-press"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
          {uploadedFile && (
            <div className="mt-2 flex items-center text-xs text-gray-500">
              <FileText className="mr-1 h-3 w-3" />
              {uploadedFile.name}
              <Check className="ml-2 h-3 w-3 text-green-600" />
            </div>
          )}
          <div className="mt-2 text-center text-xs text-gray-500">
            LoanIQ can make mistakes. Verify important information.
          </div>
        </div>
      </div>
    </div>
  );
}
