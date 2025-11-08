/**
 * Top Navigation Bar Component
 */

'use client';

import React from 'react';
import { Settings, User, Bell, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';

interface NavbarProps {
  onProfileClick?: () => void;
  onSettingsClick?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onProfileClick, onSettingsClick }) => {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed top-0 left-0 right-0 z-50 bg-dark-200/95 backdrop-blur-lg border-b border-slate-dark-300"
    >
      <div className="flex items-center justify-between h-16 px-6">
        {/* Logo and Title */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-accent-teal to-accent-emerald rounded-xl flex items-center justify-center shadow-glow-teal">
            <svg
              className="w-6 h-6 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-display font-bold text-white tracking-tight">
              Loan Document Intelligence
            </h1>
            <p className="text-xs text-gray-400">AI-Powered Document Analysis</p>
          </div>
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-2">
          {/* Notifications */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative p-2 rounded-lg hover:bg-slate-dark-200 transition-colors"
            aria-label="Notifications"
          >
            <Bell className="w-5 h-5 text-gray-300" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-accent-teal rounded-full"></span>
          </motion.button>

          {/* Settings */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onSettingsClick}
            className="p-2 rounded-lg hover:bg-slate-dark-200 transition-colors"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5 text-gray-300" />
          </motion.button>

          {/* Profile Dropdown */}
          <div className="relative ml-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onProfileClick}
              className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-slate-dark-200 hover:bg-slate-dark-100 transition-colors"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-accent-teal to-accent-emerald rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <span className="text-sm font-medium text-white hidden sm:block">Admin</span>
            </motion.button>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
