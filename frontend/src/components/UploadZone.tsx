/**
 * File Upload Component with Drag & Drop
 */

'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, X, Check, AlertCircle, Loader2 } from 'lucide-react';
import { formatFileSize } from '@/lib/utils';

interface UploadZoneProps {
  onFilesSelected: (files: File[]) => void;
  onUpload: (files: File[]) => Promise<void>;
  acceptedFileTypes?: string[];
  maxFileSize?: number;
  multiple?: boolean;
}

interface FileWithStatus {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
}

export const UploadZone: React.FC<UploadZoneProps> = ({
  onFilesSelected,
  onUpload,
  acceptedFileTypes = ['.pdf', '.docx', '.doc', '.txt'],
  maxFileSize = 50 * 1024 * 1024, // 50MB
  multiple = true,
}) => {
  const [files, setFiles] = useState<FileWithStatus[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const newFiles = acceptedFiles.map((file) => ({
        file,
        status: 'pending' as const,
        progress: 0,
      }));
      setFiles((prev) => [...prev, ...newFiles]);
      onFilesSelected(acceptedFiles);
    },
    [onFilesSelected]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxSize: maxFileSize,
    multiple,
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    const pendingFiles = files.filter((f) => f.status === 'pending');
    if (pendingFiles.length === 0) return;

    setIsUploading(true);
    
    try {
      // Process files one by one
      for (let i = 0; i < pendingFiles.length; i++) {
        const fileIndex = files.findIndex((f) => f.file === pendingFiles[i].file);
        
        // Set to uploading state
        setFiles((prev) => {
          const updated = [...prev];
          updated[fileIndex].status = 'uploading';
          updated[fileIndex].progress = 0;
          return updated;
        });

        let progressInterval: NodeJS.Timeout | null = null;
        
        try {
          // Simulate progress while uploading
          progressInterval = setInterval(() => {
            setFiles((prev) => {
              const updated = [...prev];
              if (updated[fileIndex] && updated[fileIndex].progress < 90) {
                updated[fileIndex].progress = Math.min(updated[fileIndex].progress + 10, 90);
              }
              return updated;
            });
          }, 300);

          // Call actual upload
          console.log('Uploading file:', pendingFiles[i].file.name);
          await onUpload([pendingFiles[i].file]);
          console.log('Upload successful for:', pendingFiles[i].file.name);
          
          // Clear interval and set to 100%
          if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
          }
          
          setFiles((prev) => {
            const updated = [...prev];
            if (updated[fileIndex]) {
              updated[fileIndex].progress = 100;
              updated[fileIndex].status = 'success';
            }
            return updated;
          });
        } catch (error) {
          console.error('Upload error for', pendingFiles[i].file.name, ':', error);
          
          // Clear interval if it exists
          if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
          }
          
          setFiles((prev) => {
            const updated = [...prev];
            if (updated[fileIndex]) {
              updated[fileIndex].status = 'error';
              updated[fileIndex].error = error instanceof Error ? error.message : 'Upload failed - An error occurred';
            }
            return updated;
          });
        }
      }
    } catch (outerError) {
      console.error('Outer upload error:', outerError);
    } finally {
      setIsUploading(false);
    }
  };

  const getStatusIcon = (status: FileWithStatus['status']) => {
    switch (status) {
      case 'uploading':
        return <Loader2 className="w-5 h-5 text-accent-teal animate-spin" />;
      case 'success':
        return <Check className="w-5 h-5 text-accent-emerald" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <FileText className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <motion.div
        {...getRootProps()}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`relative border-2 border-dashed rounded-2xl p-12 transition-all cursor-pointer ${
          isDragActive
            ? 'border-accent-teal bg-accent-teal/10'
            : 'border-slate-dark-300 hover:border-accent-teal/50 hover:bg-slate-dark-200/50'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-4">
          <div
            className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-all ${
              isDragActive
                ? 'bg-accent-teal text-white scale-110'
                : 'bg-slate-dark-200 text-accent-teal'
            }`}
          >
            <Upload className="w-8 h-8" />
          </div>
          <div className="text-center">
            <p className="text-lg font-semibold text-white mb-2">
              {isDragActive ? 'Drop files here' : 'Upload Loan Documents'}
            </p>
            <p className="text-sm text-gray-400">
              Drag & drop files or click to browse
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Supported: PDF, DOCX, DOC, TXT (Max {formatFileSize(maxFileSize)})
            </p>
          </div>
        </div>
      </motion.div>

      {/* File List */}
      <AnimatePresence>
        {files.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="space-y-2"
          >
            {files.map((fileWithStatus, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="bg-slate-dark-200 border border-slate-dark-300 rounded-xl p-4"
              >
                <div className="flex items-center space-x-4">
                  {/* Status Icon */}
                  <div className="flex-shrink-0">{getStatusIcon(fileWithStatus.status)}</div>

                  {/* File Info */}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">
                      {fileWithStatus.file.name}
                    </p>
                    <p className="text-xs text-gray-400">
                      {formatFileSize(fileWithStatus.file.size)}
                    </p>
                    {fileWithStatus.error && (
                      <p className="text-xs text-red-500 mt-1">{fileWithStatus.error}</p>
                    )}
                  </div>

                  {/* Progress Bar */}
                  {fileWithStatus.status === 'uploading' && (
                    <div className="flex-shrink-0 w-32">
                      <div className="w-full h-2 bg-slate-dark-300 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${fileWithStatus.progress}%` }}
                          className="h-full bg-gradient-to-r from-accent-teal to-accent-emerald"
                        />
                      </div>
                    </div>
                  )}

                  {/* Remove Button */}
                  {fileWithStatus.status !== 'uploading' && (
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => removeFile(index)}
                      className="flex-shrink-0 p-2 rounded-lg hover:bg-slate-dark-300 transition-colors"
                    >
                      <X className="w-4 h-4 text-gray-400" />
                    </motion.button>
                  )}
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Upload Button */}
      {files.some((f) => f.status === 'pending') && (
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleUpload}
          disabled={isUploading}
          className="w-full px-6 py-3 bg-gradient-to-r from-accent-teal to-accent-emerald text-white font-semibold rounded-xl hover:shadow-glow-teal transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isUploading ? (
            <span className="flex items-center justify-center space-x-2">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Processing...</span>
            </span>
          ) : (
            `Upload ${files.filter((f) => f.status === 'pending').length} File(s)`
          )}
        </motion.button>
      )}
    </div>
  );
};

export default UploadZone;
