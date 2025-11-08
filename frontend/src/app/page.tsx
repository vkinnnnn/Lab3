/**
 * Main Application Page
 * Loan Document Intelligence System
 */

'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Navbar } from '@/components/Navbar';
import { Sidebar } from '@/components/Sidebar';
import { MessageBubble } from '@/components/MessageBubble';
import { ChatInput } from '@/components/ChatInput';
import { UploadZone } from '@/components/UploadZone';
import { LanguageSelector } from '@/components/LanguageSelector';
import { DocumentCard } from '@/components/DocumentCard';
import { chatAPI, documentAPI, Message, Document, handleAPIError } from '@/lib/api';
import { generateId } from '@/lib/utils';
import {
  BarChart3,
  FileText,
  MessageSquare,
  TrendingUp,
  Clock,
  Loader2,
  AlertCircle,
  X,
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState('chat');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    totalDocuments: 0,
    totalChats: 0,
    tokensUsed: 0,
    processingTime: 0,
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      // Load chat sessions and stats
      const sessions = await chatAPI.getSessions();
      setStats((prev) => ({ ...prev, totalChats: sessions.length }));
      
      // Load documents
      const documents = await documentAPI.getAll();
      setStats((prev) => ({ ...prev, totalDocuments: documents.length }));
    } catch (err) {
      console.error('Failed to load initial data:', err);
    }
  };

  // Handle sending messages
  const handleSendMessage = async (content: string, provider: string = 'openai') => {
    if (!content.trim()) return;

    setError(null);
    setIsLoading(true);

    // Add user message immediately
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Send to backend
      const response = await chatAPI.sendMessage(content, provider);
      
      // Add assistant response
      setMessages((prev) => [...prev, response]);
      
      // Update stats
      setStats((prev) => ({
        ...prev,
        tokensUsed: prev.tokensUsed + (response.tokens || 0),
      }));
    } catch (err) {
      const errorMessage = handleAPIError(err);
      setError(errorMessage);
      
      // Add error message
      const errorMsg: Message = {
        id: generateId(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle file uploads
  const handleFileUpload = async (files: File[]) => {
    console.log('handleFileUpload called with', files.length, 'files');
    setError(null);
    
    if (!files || files.length === 0) {
      console.error('No files provided to upload');
      alert('❌ No files selected');
      return;
    }
    
    try {
      let successCount = 0;
      let failCount = 0;
      
      // Process files sequentially for better error handling
      for (const file of files) {
        try {
          console.log(`Starting upload for: ${file.name}`);
          
          const result = await documentAPI.upload(file, (progressEvent) => {
            if (progressEvent.total) {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              console.log(`Upload progress for ${file.name}: ${percentCompleted}%`);
            }
          });
          
          console.log('Upload successful:', result);
          successCount++;
          
        } catch (uploadError: any) {
          console.error(`Failed to upload ${file.name}:`, uploadError);
          console.error('Error details:', {
            message: uploadError.message,
            code: uploadError.code,
            response: uploadError.response?.data
          });
          failCount++;
        }
      }
      
      // Try to reload documents
      try {
        const documents = await documentAPI.getAll();
        setStats((prev) => ({ ...prev, totalDocuments: documents.length }));
      } catch (err) {
        console.warn('Could not reload documents:', err);
        // Update count manually based on successful uploads
        setStats((prev) => ({ ...prev, totalDocuments: prev.totalDocuments + successCount }));
      }
      
      // Show appropriate message
      if (successCount > 0 && failCount === 0) {
        alert(`✅ Successfully uploaded ${successCount} document(s)!`);
      } else if (successCount > 0 && failCount > 0) {
        alert(`⚠️ Uploaded ${successCount} document(s), ${failCount} failed`);
      } else {
        throw new Error(`All uploads failed (${failCount} files)`);
      }
      
    } catch (err: any) {
      console.error('Upload error:', err);
      const errorMessage = handleAPIError(err);
      setError(errorMessage);
      alert(`❌ Upload failed: ${errorMessage}\n\nPlease check:\n1. Backend is running (http://localhost:8000)\n2. File size is under 50MB\n3. File type is supported (PDF, DOCX, DOC, TXT)\n\nCheck browser console (F12) for details.`);
    }
  };

  // Render content based on active tab
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardView stats={stats} onNavigate={setActiveTab} />;
      case 'upload':
        return (
          <div className="max-w-4xl mx-auto">
            <UploadZone
              onFilesSelected={(files) => console.log('Files selected:', files)}
              onUpload={handleFileUpload}
            />
          </div>
        );
      case 'chat':
        return <ChatView messages={messages} isLoading={isLoading} error={error} />;
      case 'history':
        return <HistoryView />;
      case 'documents':
        return <DocumentsView />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-dark-300">
      {/* Navbar */}
      <Navbar />

      {/* Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Content */}
      <main
        className={`pt-16 transition-all duration-300 ${
          sidebarCollapsed ? 'ml-20' : 'ml-64'
        }`}
      >
        <div className="h-[calc(100vh-4rem)] flex flex-col">
          {/* Content Area */}
          <div className="flex-1 overflow-y-auto scrollbar-thin p-6">
            {renderContent()}
          </div>

          {/* Chat Input (only visible on chat tab) */}
          {activeTab === 'chat' && (
            <div className="border-t border-slate-dark-300 bg-dark-200/95 backdrop-blur-lg p-6">
              <div className="max-w-4xl mx-auto">
                <ChatInput
                  onSendMessage={handleSendMessage}
                  isLoading={isLoading}
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

// Dashboard View Component
const DashboardView: React.FC<{ stats: any; onNavigate: (tab: string) => void }> = ({ stats, onNavigate }) => {
  const statCards = [
    {
      icon: FileText,
      label: 'Total Documents',
      value: stats.totalDocuments,
      color: 'teal',
      trend: '+12%',
    },
    {
      icon: MessageSquare,
      label: 'Chat Sessions',
      value: stats.totalChats,
      color: 'emerald',
      trend: '+8%',
    },
    {
      icon: BarChart3,
      label: 'Tokens Used',
      value: stats.tokensUsed.toLocaleString(),
      color: 'purple',
      trend: '+24%',
    },
    {
      icon: Clock,
      label: 'Avg Processing',
      value: `${stats.processingTime}s`,
      color: 'orange',
      trend: '-15%',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-display font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">Overview of your loan document intelligence system</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-dark-200 border border-slate-dark-300 rounded-2xl p-6 hover:border-accent-teal/50 transition-all"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 bg-${stat.color}-500/10 rounded-xl`}>
                  <Icon className={`w-6 h-6 text-${stat.color}-500`} />
                </div>
                <span className="flex items-center text-xs font-medium text-accent-emerald">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  {stat.trend}
                </span>
              </div>
              <div className="mt-2">
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <p className="text-sm text-gray-400 mt-1">{stat.label}</p>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Welcome Card */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="bg-gradient-to-br from-accent-teal/20 to-accent-emerald/20 border border-accent-teal/30 rounded-2xl p-8"
      >
        <h2 className="text-2xl font-bold text-white mb-2">Welcome to Loan Intelligence</h2>
        <p className="text-gray-300 mb-6">
          Start by uploading loan documents or chat with our AI assistant about your existing documents.
        </p>
        <div className="flex space-x-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onNavigate('upload')}
            className="px-6 py-3 bg-accent-teal hover:bg-accent-teal-dark rounded-xl text-white font-semibold transition-colors"
          >
            Upload Documents
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onNavigate('chat')}
            className="px-6 py-3 bg-slate-dark-200 hover:bg-slate-dark-100 rounded-xl text-white font-semibold transition-colors"
          >
            Start Chatting
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
};

// Chat View Component
const ChatView: React.FC<{ messages: Message[]; isLoading: boolean; error: string | null }> = ({
  messages,
  isLoading,
  error,
}) => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      {messages.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center py-12"
        >
          <div className="w-16 h-16 bg-gradient-to-br from-accent-teal to-accent-emerald rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-glow-teal">
            <MessageSquare className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Start a Conversation</h2>
          <p className="text-gray-400">
            Ask anything about your loan documents. Try the suggestions below!
          </p>
        </motion.div>
      )}

      {/* Messages */}
      <div className="space-y-6">
        {messages.map((message, index) => (
          <MessageBubble key={message.id} message={message} index={index} />
        ))}
        
        {/* Loading Indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center space-x-3"
          >
            <div className="w-10 h-10 bg-slate-dark-200 rounded-xl flex items-center justify-center">
              <Loader2 className="w-5 h-5 text-accent-teal animate-spin" />
            </div>
            <div className="bg-slate-dark-200 rounded-2xl px-4 py-3">
              <p className="text-sm text-gray-400">Thinking...</p>
            </div>
          </motion.div>
        )}

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-start space-x-3 p-4 bg-red-500/10 border border-red-500/30 rounded-xl"
          >
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-300">{error}</p>
          </motion.div>
        )}
      </div>
    </div>
  );
};

// History View Component
const HistoryView: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-white mb-6">Chat History</h2>
      <div className="space-y-4">
        <p className="text-gray-400">Your previous chat sessions will appear here.</p>
      </div>
    </div>
  );
};

// Documents View Component
const DocumentsView: React.FC = () => {
  const [documents, setDocuments] = React.useState<Document[]>([]);
  const [selectedLanguage, setSelectedLanguage] = React.useState('en');
  const [isLoading, setIsLoading] = React.useState(true);
  const [showLanguagePrompt, setShowLanguagePrompt] = React.useState(true);

  // Load documents
  React.useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setIsLoading(true);
    try {
      const docs = await documentAPI.getAll();
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Filter documents by language
  const filteredDocuments = documents.filter((doc) => {
    if (selectedLanguage === 'all') return true;
    const docLanguage = doc.extracted_data?.language || 'en';
    return docLanguage === selectedLanguage;
  });

  const handleViewDocument = (doc: Document) => {
    alert(`Viewing document: ${doc.filename}\n\nDocument ID: ${doc.id}\nStatus: ${doc.status}`);
  };

  const handleDownloadDocument = (doc: Document) => {
    alert(`Downloading: ${doc.filename}\n\nIn production, this would download the file.`);
  };

  const handleDeleteDocument = async (doc: Document) => {
    if (confirm(`Are you sure you want to delete "${doc.filename}"?`)) {
      try {
        await documentAPI.delete(doc.id);
        setDocuments(documents.filter((d) => d.id !== doc.id));
        alert('Document deleted successfully!');
      } catch (err) {
        alert('Failed to delete document');
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Documents Library</h2>
          <p className="text-gray-400">
            {filteredDocuments.length} document(s) in {selectedLanguage === 'en' ? 'English' : selectedLanguage}
          </p>
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={loadDocuments}
          className="px-4 py-2 bg-accent-teal hover:bg-accent-teal-dark rounded-lg transition-colors text-white font-medium"
        >
          Refresh
        </motion.button>
      </div>

      {/* Language Selection Prompt */}
      <AnimatePresence>
        {showLanguagePrompt && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-gradient-to-br from-accent-teal/20 to-accent-emerald/20 border border-accent-teal/30 rounded-2xl p-6"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-xl font-bold text-white mb-2">
                  Select Your Preferred Language
                </h3>
                <p className="text-gray-300 mb-4">
                  Choose the language in which you want to view your documents. We support 10+ languages!
                </p>
                <div className="max-w-md">
                  <LanguageSelector
                    selectedLanguage={selectedLanguage}
                    onLanguageChange={(lang) => {
                      setSelectedLanguage(lang);
                      setShowLanguagePrompt(false);
                    }}
                  />
                </div>
              </div>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setShowLanguagePrompt(false)}
                className="text-gray-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Language Filter */}
      {!showLanguagePrompt && (
        <div className="bg-dark-200 border border-slate-dark-300 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-400">Viewing documents in:</p>
            <div className="flex items-center space-x-4">
              <LanguageSelector
                selectedLanguage={selectedLanguage}
                onLanguageChange={setSelectedLanguage}
                className="w-64"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                onClick={() => setSelectedLanguage('all')}
                className="text-sm text-accent-teal hover:text-accent-teal-dark"
              >
                Show All
              </motion.button>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 text-accent-teal animate-spin" />
          <span className="ml-3 text-gray-400">Loading documents...</span>
        </div>
      )}

      {/* Documents Grid */}
      {!isLoading && filteredDocuments.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocuments.map((doc, index) => (
            <DocumentCard
              key={doc.id}
              document={doc}
              index={index}
              onView={handleViewDocument}
              onDownload={handleDownloadDocument}
              onDelete={handleDeleteDocument}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && filteredDocuments.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-20"
        >
          <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">
            No documents found
          </h3>
          <p className="text-gray-400 mb-6">
            {selectedLanguage === 'all'
              ? 'Upload your first document to get started'
              : `No documents available in ${selectedLanguage === 'en' ? 'English' : selectedLanguage}`}
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setSelectedLanguage('all')}
            className="px-6 py-3 bg-accent-teal hover:bg-accent-teal-dark rounded-xl text-white font-semibold"
          >
            Show All Languages
          </motion.button>
        </motion.div>
      )}
    </div>
  );
};
