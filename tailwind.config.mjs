/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: '#EF7D00',
        caramel: {
          text: '#1F150F',
          surface: '#FCF6F0',
          glass: 'rgba(255, 255, 255, 0.65)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans SC', 'sans-serif'],
      },
      boxShadow: {
        glass: '0 24px 80px rgba(239, 125, 0, 0.16)',
      },
    },
  },
  plugins: [],
};
