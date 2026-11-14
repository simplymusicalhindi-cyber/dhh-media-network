/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dhh: {
          dark: '#090B11',
          card: '#121723',
          border: '#1F293D',
          accent: '#8B5CF6',
          gold: '#F59E0B',
          neon: '#10B981',
          crimson: '#EF4444'
        }
      }
    },
  },
  plugins: [],
}
