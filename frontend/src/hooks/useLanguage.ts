/**
 * useLanguage Hook
 * Manages language state
 * Following KIRO Global Steering Guidelines
 */

'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type LanguageCode = 'en' | 'hi' | 'te' | 'ta' | 'es' | 'zh-cn' | 'fr' | 'de' | 'pt' | 'ru';

interface LanguageStore {
  currentLanguage: LanguageCode;
  setLanguage: (lang: LanguageCode) => void;
}

const useLanguageStore = create<LanguageStore>()(
  persist(
    (set) => ({
      currentLanguage: 'en',
      setLanguage: (lang) => set({ currentLanguage: lang }),
    }),
    {
      name: 'language-storage',
    }
  )
);

export function useLanguage() {
  const { currentLanguage, setLanguage } = useLanguageStore();

  return {
    currentLanguage,
    setLanguage,
  };
}
