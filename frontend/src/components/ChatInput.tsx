/**
 * Chat Input Component with Suggestions Dropdown
 */

'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSendMessage: (message: string, provider?: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

const suggestedQueries = [
  {
    category: 'Document Analysis',
    queries: [
      'Summarize the key loan terms',
      'Extract borrower information',
      'Identify all payment schedules',
      'List all fees and charges',
    ],
  },
  {
    category: 'Compliance & Risk',
    queries: [
      'Check for missing required fields',
      'Verify compliance requirements',
      'Identify potential red flags',
      'Analyze prepayment penalties',
    ],
  },
  {
    category: 'Comparison',
    queries: [
      'Compare interest rates across documents',
      'Find similar loan agreements',
      'Compare payment terms',
      'Analyze risk factors',
    ],
  },
];

const llmProviders = [
  { id: 'openai', name: 'OpenAI GPT-4o-mini', color: 'emerald' },
  { id: 'anthropic', name: 'Anthropic Claude 3.5', color: 'orange' },
  { id: 'kimi', name: 'Kimi K2 Turbo', color: 'purple' },
];

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  isLoading = false,
  placeholder = 'Ask anything about your loan documents...',
}) => {
  const [message, setMessage] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [showProviders, setShowProviders] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('openai');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
        setShowProviders(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim(), selectedProvider);
      setMessage('');
      setShowSuggestions(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionClick = (query: string) => {
    setMessage(query);
    setShowSuggestions(false);
    textareaRef.current?.focus();
  };

  const selectedProviderData = llmProviders.find((p) => p.id === selectedProvider);

  return (
    <div className="relative" ref={suggestionsRef}>
      {/* Suggestions Dropdown */}
      <AnimatePresence>
        {showSuggestions && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute bottom-full left-0 right-0 mb-2 bg-dark-200 border border-slate-dark-300 rounded-2xl shadow-dark-xl overflow-hidden"
          >
            <div className="p-4 max-h-96 overflow-y-auto">
              <div className="flex items-center space-x-2 mb-4">
                <Sparkles className="w-4 h-4 text-accent-teal" />
                <span className="text-sm font-semibold text-white">Suggested Queries</span>
              </div>
              <div className="space-y-4">
                {suggestedQueries.map((category) => (
                  <div key={category.category}>
                    <p className="text-xs font-medium text-gray-400 mb-2">{category.category}</p>
                    <div className="space-y-1">
                      {category.queries.map((query) => (
                        <button
                          key={query}
                          onClick={() => handleSuggestionClick(query)}
                          className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-dark-200 transition-colors text-sm text-gray-300 hover:text-white"
                        >
                          {query}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* LLM Provider Selector Dropdown */}
      <AnimatePresence>
        {showProviders && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute bottom-full left-0 mb-2 bg-dark-200 border border-slate-dark-300 rounded-xl shadow-dark-xl overflow-hidden"
          >
            <div className="p-2 space-y-1">
              {llmProviders.map((provider) => (
                <button
                  key={provider.id}
                  onClick={() => {
                    setSelectedProvider(provider.id);
                    setShowProviders(false);
                  }}
                  className={cn(
                    'w-full text-left px-3 py-2 rounded-lg transition-colors text-sm',
                    selectedProvider === provider.id
                      ? 'bg-accent-teal/20 text-accent-teal'
                      : 'hover:bg-slate-dark-200 text-gray-300'
                  )}
                >
                  {provider.name}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input Container */}
      <div className="bg-dark-200 border border-slate-dark-300 rounded-2xl shadow-dark-lg">
        <div className="flex items-end p-4 space-x-3">
          {/* Provider Selector Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowProviders(!showProviders)}
            className="flex-shrink-0 px-3 py-2 bg-slate-dark-200 hover:bg-slate-dark-100 rounded-xl transition-colors flex items-center space-x-2"
          >
            <div className={`w-2 h-2 rounded-full bg-${selectedProviderData?.color}-500`}></div>
            <span className="text-xs text-gray-400">{selectedProviderData?.name.split(' ')[0]}</span>
            <ChevronDown className="w-3 h-3 text-gray-400" />
          </motion.button>

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            onFocus={() => setShowSuggestions(false)}
            placeholder={placeholder}
            disabled={isLoading}
            rows={1}
            className="flex-1 bg-transparent border-none outline-none resize-none text-sm text-white placeholder-gray-500 max-h-32"
          />

          {/* Suggestions Toggle */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowSuggestions(!showSuggestions)}
            className="flex-shrink-0 p-2 rounded-lg hover:bg-slate-dark-200 transition-colors"
            aria-label="Show suggestions"
          >
            <Sparkles className="w-5 h-5 text-accent-teal" />
          </motion.button>

          {/* Send Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSend}
            disabled={!message.trim() || isLoading}
            className={cn(
              'flex-shrink-0 p-2 rounded-xl transition-all',
              message.trim() && !isLoading
                ? 'bg-gradient-to-r from-accent-teal to-accent-emerald hover:shadow-glow-teal'
                : 'bg-slate-dark-300 cursor-not-allowed'
            )}
            aria-label="Send message"
          >
            <Send
              className={cn('w-5 h-5', message.trim() && !isLoading ? 'text-white' : 'text-gray-500')}
            />
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
