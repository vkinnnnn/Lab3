/**
 * Document Card Component
 * Displays individual document with metadata
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, Eye, Trash2, Clock, HardDrive, CheckCircle } from 'lucide-react';
import { formatFileSize, formatRelativeTime } from '@/lib/utils';
import { Document } from '@/lib/api';

interface DocumentCardProps {
  document: Document;
  onView?: (doc: Document) => void;
  onDownload?: (doc: Document) => void;
  onDelete?: (doc: Document) => void;
  index?: number;
}

export const DocumentCard: React.FC<DocumentCardProps> = ({
  document,
  onView,
  onDownload,
  onDelete,
  index = 0,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-accent-emerald';
      case 'processing':
        return 'text-yellow-500';
      case 'failed':
        return 'text-red-500';
      default:
        return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'processing':
        return <Clock className="w-4 h-4 animate-spin" />;
      case 'failed':
        return <Trash2 className="w-4 h-4" />;
      default:
        return <FileText className="w-4 h-4" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-slate-dark-200 border border-slate-dark-300 rounded-xl p-6 hover:border-accent-teal/50 transition-all group"
    >
      <div className="flex items-start justify-between mb-4">
        {/* Document Icon & Info */}
        <div className="flex items-start space-x-4 flex-1">
          <div className="w-12 h-12 bg-gradient-to-br from-accent-teal/20 to-accent-emerald/20 rounded-xl flex items-center justify-center border border-accent-teal/30">
            <FileText className="w-6 h-6 text-accent-teal" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-white mb-1 truncate">{document.filename}</h3>
            <div className="flex items-center space-x-3 text-xs text-gray-400">
              <span className="flex items-center space-x-1">
                <HardDrive className="w-3 h-3" />
                <span>{formatFileSize(document.size)}</span>
              </span>
              <span>•</span>
              <span className="flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>{formatRelativeTime(document.uploaded_at)}</span>
              </span>
            </div>
          </div>
        </div>

        {/* Status Badge */}
        <div className={`flex items-center space-x-1 ${getStatusColor(document.status)}`}>
          {getStatusIcon(document.status)}
          <span className="text-xs font-medium capitalize">{document.status}</span>
        </div>
      </div>

      {/* Extracted Data Preview */}
      {document.extracted_data && (
        <div className="bg-dark-300 rounded-lg p-4 mb-4">
          <p className="text-xs font-semibold text-gray-400 mb-2">Extracted Information</p>
          <div className="space-y-2">
            {Object.entries(document.extracted_data).slice(0, 3).map(([key, value]) => (
              <div key={key} className="flex justify-between text-sm">
                <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="text-white font-medium">{String(value)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center space-x-2">
        {onView && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onView(document)}
            className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-accent-teal hover:bg-accent-teal-dark rounded-lg transition-colors"
          >
            <Eye className="w-4 h-4" />
            <span className="text-sm font-medium">View</span>
          </motion.button>
        )}
        {onDownload && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onDownload(document)}
            className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-slate-dark-300 hover:bg-slate-dark-100 rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            <span className="text-sm font-medium">Download</span>
          </motion.button>
        )}
        {onDelete && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onDelete(document)}
            className="p-2 bg-red-500/10 hover:bg-red-500/20 rounded-lg transition-colors border border-red-500/30"
          >
            <Trash2 className="w-4 h-4 text-red-500" />
          </motion.button>
        )}
      </div>
    </motion.div>
  );
};

export default DocumentCard;
