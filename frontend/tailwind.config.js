/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'coca-cola-red': '#F40009',
        'coca-cola-dark': '#1E1E1E',
        'coca-cola-white': '#FFFFFF',
      },
    },
  },
  plugins: [],
}
