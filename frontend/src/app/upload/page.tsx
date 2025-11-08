/**
 * Upload Page - Document Upload and Extraction
 * Beautiful drag-and-drop interface with live results
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React from 'react';
import { DocumentUpload } from '@/components/features/DocumentUpload';
import { motion } from 'framer-motion';
import { Upload, FileText, Zap } from 'lucide-react';

export default function UploadPage() {
  return (
    <div className="container py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mx-auto max-w-4xl"
      >
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full gradient-teal">
            <Upload className="h-8 w-8 text-white" />
          </div>
          <h1 className="mb-4 text-4xl font-bold text-slate">Upload Loan Document</h1>
          <p className="text-lg text-slate-light">
            Upload your loan document and get instant AI-powered analysis
          </p>
        </div>

        {/* Features */}
        <div className="mb-8 grid gap-4 sm:grid-cols-3">
          <div className="rounded-lg bg-teal-50 p-4 text-center">
            <Zap className="mx-auto mb-2 h-6 w-6 text-teal" />
            <div className="text-sm font-medium text-slate">Fast Processing</div>
            <div className="text-xs text-slate-lighter">Results in seconds</div>
          </div>
          <div className="rounded-lg bg-blue-50 p-4 text-center">
            <FileText className="mx-auto mb-2 h-6 w-6 text-blue-600" />
            <div className="text-sm font-medium text-slate">Smart Extraction</div>
            <div className="text-xs text-slate-lighter">95%+ accuracy</div>
          </div>
          <div className="rounded-lg bg-green-50 p-4 text-center">
            <Upload className="mx-auto mb-2 h-6 w-6 text-green-600" />
            <div className="text-sm font-medium text-slate">Easy Upload</div>
            <div className="text-xs text-slate-lighter">Drag & drop</div>
          </div>
        </div>

        {/* Upload Component */}
        <DocumentUpload />
      </motion.div>
    </div>
  );
}
