/**
 * Document Upload Component
 * Drag-and-drop interface with live extraction results
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Check, AlertCircle, Loader2, X } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { toast } from '@/components/ui/toaster';
import { api } from '@/lib/api';
import { formatCurrency, formatPercent } from '@/lib/utils';
import type { ExtractionResult } from '@/types';
import Confetti from 'react-confetti';

type UploadStatus = 'idle' | 'uploading' | 'processing' | 'complete' | 'error';

export function DocumentUpload() {
  const [status, setStatus] = useState<UploadStatus>('idle');
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setStatus('uploading');
    setProgress(0);
    setError(null);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      setStatus('processing');
      
      const response = await api.uploadDocument(file);
      
      clearInterval(progressInterval);
      setProgress(100);

      // Extract the result
      const extractedData = response.data;
      setResult(extractedData);
      setStatus('complete');
      
      // Show confetti animation
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);

      toast({
        title: 'Success!',
        description: 'Document extracted successfully',
        variant: 'success',
      });
    } catch (err: any) {
      setStatus('error');
      setError(err.response?.data?.detail || 'Failed to process document');
      toast({
        title: 'Error',
        description: 'Failed to process document. Please try again.',
        variant: 'destructive',
      });
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg', '.tiff'],
    },
    multiple: false,
    disabled: status === 'uploading' || status === 'processing',
  });

  const reset = () => {
    setStatus('idle');
    setProgress(0);
    setResult(null);
    setError(null);
  };

  return (
    <>
      {showConfetti && <Confetti recycle={false} numberOfPieces={200} />}
      
      <div className="space-y-6">
        {/* Upload Area */}
        <AnimatePresence mode="wait">
          {(status === 'idle' || status === 'uploading' || status === 'processing') && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
            >
              <Card>
                <CardContent className="p-0">
                  <div
                    {...getRootProps()}
                    className={`cursor-pointer border-2 border-dashed p-12 text-center transition-all duration-300 ${
                      isDragActive
                        ? 'border-teal bg-teal-50'
                        : 'border-gray-300 hover:border-teal hover:bg-base-dark'
                    } ${
                      status === 'uploading' || status === 'processing'
                        ? 'cursor-not-allowed opacity-50'
                        : ''
                    }`}
                  >
                    <input {...getInputProps()} />
                    
                    <motion.div
                      animate={isDragActive ? { scale: 1.05 } : { scale: 1 }}
                      transition={{ duration: 0.2 }}
                    >
                      {status === 'uploading' || status === 'processing' ? (
                        <Loader2 className="mx-auto h-16 w-16 animate-spin text-teal" />
                      ) : (
                        <Upload className="mx-auto h-16 w-16 text-slate-lighter" />
                      )}
                      
                      <div className="mt-4">
                        {status === 'uploading' && (
                          <p className="text-lg font-medium text-slate">Uploading...</p>
                        )}
                        {status === 'processing' && (
                          <p className="text-lg font-medium text-slate">
                            Processing with AI...
                          </p>
                        )}
                        {status === 'idle' && (
                          <>
                            <p className="text-lg font-medium text-slate">
                              {isDragActive
                                ? 'Drop your file here'
                                : 'Drag & drop your loan document'}
                            </p>
                            <p className="mt-2 text-sm text-slate-lighter">
                              or click to browse • PDF, PNG, JPG, TIFF
                            </p>
                          </>
                        )}
                      </div>
                    </motion.div>

                    {(status === 'uploading' || status === 'processing') && (
                      <div className="mx-auto mt-6 max-w-md">
                        <Progress value={progress} className="h-2" />
                        <p className="mt-2 text-sm text-slate-lighter">
                          {progress}% • Powered by Google Document AI
                        </p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Error State */}
          {status === 'error' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Card className="border-accent-red">
                <CardContent className="p-8 text-center">
                  <AlertCircle className="mx-auto h-16 w-16 text-accent-red" />
                  <h3 className="mt-4 text-lg font-medium text-slate">Upload Failed</h3>
                  <p className="mt-2 text-sm text-slate-lighter">{error}</p>
                  <Button onClick={reset} className="mt-4">
                    Try Again
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Success State with Results */}
          {status === 'complete' && result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Success Message */}
              <Card className="border-green-200 bg-green-50">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                      <Check className="h-6 w-6 text-green-600" />
                    </div>
                    <div className="ml-4">
                      <h3 className="font-semibold text-slate">Extraction Complete!</h3>
                      <p className="text-sm text-slate-lighter">
                        Document processed successfully with{' '}
                        {formatPercent(result.accuracy_metrics.overall_accuracy * 100)} accuracy
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={reset}
                      className="ml-auto"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Extracted Data */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <FileText className="mr-2 h-5 w-5 text-teal" />
                    Extracted Loan Details
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2">
                    <DataField
                      label="Bank Name"
                      value={result.normalized_data.bank_name || 'N/A'}
                      icon="🏦"
                    />
                    <DataField
                      label="Loan Type"
                      value={result.normalized_data.loan_type || 'N/A'}
                      icon="📄"
                    />
                    <DataField
                      label="Principal Amount"
                      value={formatCurrency(result.normalized_data.principal_amount)}
                      icon="💰"
                      highlight
                    />
                    <DataField
                      label="Interest Rate"
                      value={formatPercent(result.normalized_data.interest_rate)}
                      icon="📊"
                      highlight
                    />
                    <DataField
                      label="Tenure"
                      value={`${result.normalized_data.tenure_months} months`}
                      icon="⏰"
                    />
                    <DataField
                      label="Monthly Payment"
                      value={formatCurrency(result.normalized_data.monthly_payment)}
                      icon="💳"
                      highlight
                    />
                  </div>

                  {result.normalized_data.processing_fee && (
                    <div className="mt-4 rounded-lg bg-base-dark p-4">
                      <div className="text-sm text-slate-lighter">
                        Processing Fee:{' '}
                        <span className="font-medium text-slate">
                          {formatCurrency(result.normalized_data.processing_fee)}
                        </span>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Actions */}
              <div className="flex gap-4">
                <Button asChild className="flex-1">
                  <a href="/compare">Compare with Other Loans</a>
                </Button>
                <Button asChild variant="outline" className="flex-1">
                  <a href="/chat">Ask Questions</a>
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
}

// Helper component for data fields
function DataField({
  label,
  value,
  icon,
  highlight = false,
}: {
  label: string;
  value: string;
  icon: string;
  highlight?: boolean;
}) {
  return (
    <div
      className={`rounded-lg p-4 ${
        highlight ? 'bg-teal-50 border border-teal-100' : 'bg-base-dark'
      }`}
    >
      <div className="flex items-center text-sm text-slate-lighter">
        <span className="mr-2">{icon}</span>
        {label}
      </div>
      <div className={`mt-1 text-lg font-semibold ${highlight ? 'text-teal' : 'text-slate'}`}>
        {value}
      </div>
    </div>
  );
}
