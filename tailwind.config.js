/** @type {import('tailwindcss').Config} */
module.exports = {

  content: [
    "./**/templates/**/*.html",
    "./**/templates/**/**/*.html",
    "./**/static/**/js/*.js",
    "./**/static/**/js/**/*.js"
  ],
  theme: {
    container: {
      center: true,
      screens: {
        'sm': '100%',
        'md': '726px',
        'lg': '982px',
        'xl': '1200px',
        '2xl': '1200px',
      },
    },
    extend: {
      colors: {
        'brand-light-gray': '#FFFFFF',
        'brand-light-blue': '#0573F0',
        'brand-dark-blue': '#0769DA',
        'brand-dark-gray': '#F7FBFC',
        'brand-dark-text': "#27323f",
        'brand-light-border': '#dce3e5',
        'brand-price': '#48515B',
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif']
      },
      container: {
        'desktop': '1200px'
      },
      backgroundImage: {
        'banner1': "url('/assets/img/banner/banner1.jpg)",
      }
    },
  },
  plugins: [],
}

