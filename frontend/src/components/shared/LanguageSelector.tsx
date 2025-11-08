/**
 * Language Selector Component
 * Dropdown for selecting interface language
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React from 'react';
import { Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useLanguage } from '@/hooks/useLanguage';

const languages = [
  { code: 'en' as const, name: 'English', native: 'English' },
  { code: 'hi' as const, name: 'Hindi', native: 'हिंदी' },
  { code: 'te' as const, name: 'Telugu', native: 'తెలుగు' },
  { code: 'ta' as const, name: 'Tamil', native: 'தமிழ்' },
  { code: 'es' as const, name: 'Spanish', native: 'Español' },
  { code: 'zh-cn' as const, name: 'Chinese', native: '中文' },
  { code: 'fr' as const, name: 'French', native: 'Français' },
  { code: 'de' as const, name: 'German', native: 'Deutsch' },
  { code: 'pt' as const, name: 'Portuguese', native: 'Português' },
  { code: 'ru' as const, name: 'Russian', native: 'Русский' },
];

export function LanguageSelector() {
  const { currentLanguage, setLanguage } = useLanguage();

  const currentLang = languages.find((lang) => lang.code === currentLanguage) || languages[0];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className="space-x-2">
          <Globe className="h-4 w-4" />
          <span className="hidden sm:inline">{currentLang.native}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        {languages.map((lang) => (
          <DropdownMenuItem
            key={lang.code}
            onClick={() => setLanguage(lang.code)}
            className={currentLanguage === lang.code ? 'bg-teal-50 text-teal' : ''}
          >
            <span className="font-medium">{lang.native}</span>
            <span className="ml-auto text-xs text-slate-lighter">{lang.name}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
