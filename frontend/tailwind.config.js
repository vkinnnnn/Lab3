/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Dark theme color palette
        dark: {
          100: '#1a1d29',
          200: '#151820',
          300: '#0f1117',
          400: '#0a0c10',
          500: '#06070a',
        },
        'slate-dark': {
          100: '#2a2f3f',
          200: '#252a38',
          300: '#1f2331',
          400: '#1a1d29',
          500: '#151820',
        },
        accent: {
          teal: '#14b8a6',
          'teal-dark': '#0d9488',
          emerald: '#10b981',
          'emerald-dark': '#059669',
        },
        foreground: '#ffffff',
        background: '#0a0c10',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'dark-lg': '0 10px 30px -5px rgba(0, 0, 0, 0.5)',
        'dark-xl': '0 20px 40px -10px rgba(0, 0, 0, 0.6)',
        'glow-teal': '0 0 20px rgba(20, 184, 166, 0.3)',
        'glow-emerald': '0 0 20px rgba(16, 185, 129, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
