/**
 * Chat Message Bubble Component
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Bot, User, Copy, Check } from 'lucide-react';
import { Message } from '@/lib/api';
import { formatRelativeTime, copyToClipboard } from '@/lib/utils';

interface MessageBubbleProps {
  message: Message;
  index: number;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, index }) => {
  const [copied, setCopied] = React.useState(false);
  const isUser = message.role === 'user';

  const handleCopy = async () => {
    const success = await copyToClipboard(message.content);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center ${
          isUser
            ? 'bg-gradient-to-br from-accent-teal to-accent-emerald shadow-glow-teal'
            : 'bg-slate-dark-200 border border-slate-dark-300'
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-accent-teal" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-2xl ${isUser ? 'flex flex-col items-end' : ''}`}>
        {/* Message Bubble */}
        <motion.div
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          className={`group relative px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-gradient-to-br from-accent-teal/20 to-accent-emerald/20 border border-accent-teal/30 rounded-tr-sm'
              : 'bg-slate-dark-200 border border-slate-dark-300 rounded-tl-sm'
          }`}
        >
          <p className="text-sm text-gray-100 leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>

          {/* Copy Button */}
          {!isUser && (
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={handleCopy}
              className="absolute top-2 right-2 p-1.5 rounded-lg bg-slate-dark-300/50 hover:bg-slate-dark-300 opacity-0 group-hover:opacity-100 transition-opacity"
              aria-label="Copy message"
            >
              {copied ? (
                <Check className="w-4 h-4 text-accent-emerald" />
              ) : (
                <Copy className="w-4 h-4 text-gray-400" />
              )}
            </motion.button>
          )}
        </motion.div>

        {/* Metadata */}
        <div className={`flex items-center space-x-2 mt-1 px-2 ${isUser ? 'justify-end' : ''}`}>
          <span className="text-xs text-gray-500">
            {formatRelativeTime(message.timestamp)}
          </span>
          {message.provider && !isUser && (
            <>
              <span className="text-xs text-gray-600">•</span>
              <span className="text-xs text-accent-teal font-medium">
                {message.provider}
              </span>
            </>
          )}
          {message.tokens && !isUser && (
            <>
              <span className="text-xs text-gray-600">•</span>
              <span className="text-xs text-gray-500">{message.tokens} tokens</span>
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default MessageBubble;
