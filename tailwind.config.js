/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        light : {
          ...require("daisyui/src/theming/themes")["light"],
          "primary": "#ef4056",
          "primary-content": "#ffffff",
        }
      }
    ],
  },
}

