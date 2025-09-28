/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        // Malaysian SPM Education Color Palette
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        // Malaysian flag colors
        malaysia: {
          red: '#0033A0',      // Blue from Malaysian flag
          blue: '#CC0001',     // Red from Malaysian flag
          yellow: '#FFCC00',   // Yellow from Malaysian flag
          white: '#FFFFFF',
        },
        // Education-themed colors
        education: {
          wisdom: '#1e40af',   // Deep blue for wisdom
          growth: '#059669',   // Green for growth
          creativity: '#dc2626', // Red for creativity
          excellence: '#ca8a04', // Gold for excellence
          knowledge: '#7c3aed', // Purple for knowledge
        },
        // Subject-specific colors
        subject: {
          math: '#2563eb',     // Blue for Mathematics
          science: '#16a34a',  // Green for Science
          language: '#dc2626', // Red for Languages
          history: '#ca8a04',  // Gold for History
          arts: '#9333ea',     // Purple for Arts
          commerce: '#059669', // Emerald for Commerce
        },
        accent: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        malay: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.8s ease-out',
        'slide-in': 'slideIn 0.5s ease-out',
        'pulse-slow': 'pulse 3s infinite',
        'bounce-slow': 'bounce 2s infinite',
        'gradient-shift': 'gradientShift 8s ease infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        gradientShift: {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' },
        },
      },
      backgroundImage: {
        'malaysia-gradient': 'linear-gradient(135deg, #0033A0 0%, #CC0001 50%, #FFCC00 100%)',
        'education-gradient': 'linear-gradient(135deg, #1e40af 0%, #059669 25%, #dc2626 50%, #ca8a04 75%, #7c3aed 100%)',
        'spm-gradient': 'linear-gradient(135deg, #6366f1 0%, #22c55e 100%)',
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('@tailwindcss/typography'),
  ],
  daisyui: {
    themes: [
      'light',
      'dark',
      {
        malaysia: {
          primary: '#0033A0',
          secondary: '#CC0001',
          accent: '#FFCC00',
          neutral: '#1F2937',
          info: '#3B82F6',
          success: '#10B981',
          warning: '#F59E0B',
          error: '#EF4444',
          base: '#FFFFFF',
          rounded: 'medium',
          fontFamily: 'Inter, system-ui, sans-serif',
        },
      },
      {
        spm: {
          primary: '#6366f1',
          secondary: '#22c55e',
          accent: '#ca8a04',
          neutral: '#1F2937',
          info: '#3B82F6',
          success: '#10B981',
          warning: '#F59E0B',
          error: '#EF4444',
          base: '#FFFFFF',
          rounded: 'medium',
          fontFamily: 'Inter, system-ui, sans-serif',
        },
      },
    ],
    darkTheme: 'dark',
    base: true,
    styled: true,
    utils: true,
    prefix: "",
    logs: true,
    themeRoot: ":root",
  },
}