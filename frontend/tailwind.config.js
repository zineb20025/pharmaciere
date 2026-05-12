/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}'
  ],
  theme: {
    extend: {
      colors: {
        pharma: {
          purple: '#6366F1',
          blueLight: '#93C5FD'
        }
      },
      boxShadow: {
        soft: '0 10px 30px rgba(99, 102, 241, 0.12)'
      }
    }
  },
  plugins: []
}

