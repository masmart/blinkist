/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}",
  "./templates/views/user/**/*.{html,js}"
],
  theme: {
    extend: {
      screens: {
        m: '768px',
        l: '976px',
        xl: '1440px',
      },
      colors: {
        'primary': '#6DDC89',
        'primary-highlight': '#58B770',
        'primary-light': '#EAFDF1',
        'secondary': '#113149',
        'menu': '#F2F6F4',
        'card': '#BCC8CD',
        'promotion': '#FDF3DA',
        'link': '#2367E9',
        'link-light': '#DAE9FD',
        'link-dark': '#113778',
        'error':'#F197A1',
        'border': '#6F787D',
        'green': {
          DEFAULT: '#6DDC89',
          8:'#EAFDF1',
        },
        'blue': {
          DEFAULT: '#2367E9',
          1: '#113778',
          2: '#1D53B7',
        },
        'raspberry': '#EC5462',
        'pale-mint-grey': '#F2F6F4',
        'light-grey': '#BCC8CD',
        'mid-grey': '#6F787D',
        'dark-grey': '#3C4649',
        'midnight': '#113149',
        'background': {
          'yellow': '#FDF3DA',
          'blue': '#DAE9FD',
        },
        'light-pale-mint-grey': '#F8FAF9',
      },
      fontSize: {
        sm: '0.8rem',
        base: '1rem',
        xl: '1.25rem',
        'caption': '0.8rem',
        'p0': '1.1rem',
        'h2': '1.6rem',
        'h5': '0.9rem',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
