export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        accent: '#00b894',
        warn: '#ff6b6b',
        success: '#4caf50',
        'top-bar': '#1e1e2f',
        'bottom-bar': '#0f1117',
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
