/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // 加入 src 資料夾底下所有 js/ts 檔案
  ],
  theme: {
    extend: {},
  },
  plugins: [
  require('@tailwindcss/forms'),
  require('@tailwindcss/typography'),
  require('daisyui'),
  ],
}
