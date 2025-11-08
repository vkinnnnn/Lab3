/**
 * Language Selector Component
 * Allows users to select their preferred language for viewing documents
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Globe, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Language {
  code: string;
  name: string;
  nativeName: string;
  flag: string;
}

interface LanguageSelectorProps {
  selectedLanguage: string;
  onLanguageChange: (languageCode: string) => void;
  className?: string;
}

const languages: Language[] = [
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷' },
  { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', flag: '🇨🇳' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語', flag: '🇯🇵' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', flag: '🇮🇳' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦' },
  { code: 'pt', name: 'Portuguese', nativeName: 'Português', flag: '🇵🇹' },
  { code: 'ru', name: 'Russian', nativeName: 'Русский', flag: '🇷🇺' },
];

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  selectedLanguage,
  onLanguageChange,
  className,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedLang = languages.find((lang) => lang.code === selectedLanguage) || languages[0];

  return (
    <div className={cn('relative', className)} ref={dropdownRef}>
      {/* Selected Language Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 px-4 py-3 bg-slate-dark-200 hover:bg-slate-dark-100 border border-slate-dark-300 rounded-xl transition-colors w-full"
      >
        <Globe className="w-5 h-5 text-accent-teal" />
        <div className="flex-1 text-left">
          <p className="text-sm font-medium text-white">
            {selectedLang.flag} {selectedLang.name}
          </p>
          <p className="text-xs text-gray-400">{selectedLang.nativeName}</p>
        </div>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="text-gray-400"
        >
          ▼
        </motion.div>
      </motion.button>

      {/* Dropdown Menu */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="absolute top-full left-0 right-0 mt-2 bg-dark-200 border border-slate-dark-300 rounded-xl shadow-dark-xl max-h-96 overflow-y-auto z-50"
        >
          <div className="p-2 space-y-1">
            {languages.map((language) => {
              const isSelected = language.code === selectedLanguage;
              return (
                <motion.button
                  key={language.code}
                  whileHover={{ x: 4 }}
                  onClick={() => {
                    onLanguageChange(language.code);
                    setIsOpen(false);
                  }}
                  className={cn(
                    'w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors',
                    isSelected
                      ? 'bg-accent-teal/20 border border-accent-teal/30'
                      : 'hover:bg-slate-dark-200'
                  )}
                >
                  <span className="text-2xl">{language.flag}</span>
                  <div className="flex-1 text-left">
                    <p className={cn('text-sm font-medium', isSelected ? 'text-accent-teal' : 'text-white')}>
                      {language.name}
                    </p>
                    <p className="text-xs text-gray-400">{language.nativeName}</p>
                  </div>
                  {isSelected && <Check className="w-5 h-5 text-accent-teal" />}
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default LanguageSelector;
