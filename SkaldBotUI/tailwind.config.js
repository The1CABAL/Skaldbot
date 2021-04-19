// tailwind.config.js
const colors = require('tailwindcss/colors');

module.exports = {
    purge: [
        './src/**/*.html',
        './src/**/*.js',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            colors: {
                primary: colors.coolGray['800'],
                primaryLight: colors.coolGray['500'],
                secondary: colors.indigo['800'],
                dark: colors.trueGray['800'],
                hover: colors.indigo['400'],
                hoverLight: colors.indigo['200']
            },
        },
    },
    variants: {},
    plugins: [],
}