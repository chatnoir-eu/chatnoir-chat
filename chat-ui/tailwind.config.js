module.exports = {
    purge: [
        './src/**/*.html',
        './src/**/*.vue',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            transitionProperty: {
                'width': 'width'
            },
            fontSize: {
                '2xs': '.65rem'
            },
            spacing: {
                '18': '4.5rem',
              }
        },
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: '#000',
            white: '#fff',
            red: {
                DEFAULT: '#CB4625',
                '50': '#F2C2B6',
                '100': '#EEB3A5',
                '200': '#E89682',
                '300': '#E27A60',
                '400': '#DB5D3D',
                '500': '#CB4625',
                '600': '#B53F21',
                '700': '#9F371D',
                '800': '#8A3019',
                '900': '#742815'
            },
            gray: {
                DEFAULT: '#A8A4A3',
                '50': '#FFFFFF',
                '100': '#F8F7F7',
                '200': '#E4E2E2',
                '300': '#D0CECD',
                '400': '#BCB9B8',
                '500': '#A8A4A3',
                '600': '#908A89',
                '700': '#76716F',
                '800': '#5C5857',
                '900': '#423F3E'
            },
        },
        fill: theme => theme('colors'),
        fontFamily: {
            'sans': ['Carlito', 'ui-sans-serif', 'system-ui', 'sans-serif'],
            'serif': ['ui-serif'],
            'mono': ['ui-monospace', 'monospace']
        },
        shadows: {
            red: '0 2px 4px 0 rgba(288, 121, 106, 0.10)'
        },
    },
    variants: {
        extend: {
            textColor: ['active', 'visited'],
            ringOffsetWidth: ['focus-visible'],
            ringWidth: ['focus-visible'],
            ringColor: ['focus-visible'],
            display: ['group-focus', 'group-hover'],
        },
    },
    plugins: [],
}
