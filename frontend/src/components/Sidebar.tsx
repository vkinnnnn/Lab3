/**
 * Sidebar Navigation Component
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Upload,
  MessageSquare,
  History,
  Database,
  Settings,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  collapsed?: boolean;
  onToggleCollapse?: () => void;
}

const menuItems = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: LayoutDashboard,
    description: 'Overview & Analytics',
  },
  {
    id: 'upload',
    label: 'Upload Documents',
    icon: Upload,
    description: 'Process New Files',
  },
  {
    id: 'chat',
    label: 'Chat Assistant',
    icon: MessageSquare,
    description: 'AI Q&A Interface',
  },
  {
    id: 'history',
    label: 'History',
    icon: History,
    description: 'Past Sessions',
  },
  {
    id: 'documents',
    label: 'Documents',
    icon: Database,
    description: 'Manage Files',
  },
];

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  collapsed = false,
  onToggleCollapse,
}) => {
  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className={cn(
        'fixed left-0 top-16 bottom-0 z-40 bg-dark-200 border-r border-slate-dark-300 transition-all duration-300',
        collapsed ? 'w-20' : 'w-64'
      )}
    >
      <div className="flex flex-col h-full">
        {/* Collapse Toggle */}
        <div className="flex justify-end p-4">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onToggleCollapse}
            className="p-2 rounded-lg hover:bg-slate-dark-200 transition-colors"
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? (
              <ChevronRight className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronLeft className="w-5 h-5 text-gray-400" />
            )}
          </motion.button>
        </div>

        {/* Menu Items */}
        <nav className="flex-1 px-3 py-4 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <motion.button
                key={item.id}
                whileHover={{ x: 4 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onTabChange(item.id)}
                className={cn(
                  'w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200',
                  isActive
                    ? 'bg-gradient-to-r from-accent-teal/20 to-accent-emerald/20 border border-accent-teal/30 shadow-glow-teal'
                    : 'hover:bg-slate-dark-200'
                )}
              >
                <Icon
                  className={cn(
                    'w-5 h-5 flex-shrink-0',
                    isActive ? 'text-accent-teal' : 'text-gray-400'
                  )}
                />
                {!collapsed && (
                  <div className="flex-1 text-left">
                    <p
                      className={cn(
                        'text-sm font-medium',
                        isActive ? 'text-white' : 'text-gray-300'
                      )}
                    >
                      {item.label}
                    </p>
                    <p className="text-xs text-gray-500">{item.description}</p>
                  </div>
                )}
              </motion.button>
            );
          })}
        </nav>

        {/* Bottom Section */}
        {!collapsed && (
          <div className="p-4 border-t border-slate-dark-300">
            <div className="bg-gradient-to-br from-slate-dark-200 to-slate-dark-300 rounded-xl p-4">
              <p className="text-xs font-semibold text-accent-teal mb-2">System Status</p>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">LLM Providers</span>
                  <span className="text-xs font-medium text-accent-emerald">3 Active</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">Vector Store</span>
                  <span className="text-xs font-medium text-accent-emerald">Connected</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </motion.aside>
  );
};

export default Sidebar;
