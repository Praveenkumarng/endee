/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                neon: {
                    pink: '#f093fb',
                    purple: '#9333ea',
                    blue: '#4facfe',
                    cyan: '#00f2fe',
                    green: '#00f260',
                    yellow: '#ffd200',
                    orange: '#ff6a00',
                    red: '#eb3349',
                },
                primary: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: '#7dd3fc',
                    400: '#38bdf8',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                },
            },
            fontFamily: {
                sans: ['Poppins', 'Montserrat', 'system-ui', 'sans-serif'],
                display: ['Montserrat', 'Poppins', 'sans-serif'],
            },
            animation: {
                'gradient-shift': 'gradient-shift 15s ease infinite',
                'shimmer': 'shimmer 3s infinite',
                'float': 'float 20s ease-in-out infinite',
                'rotate': 'rotate 4s linear infinite',
                'rainbow-flow': 'rainbow-flow 5s linear infinite',
                'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
                'bounce-slow': 'bounce 3s infinite',
            },
            keyframes: {
                'gradient-shift': {
                    '0%, 100%': { backgroundPosition: '0% 50%' },
                    '50%': { backgroundPosition: '100% 50%' },
                },
                shimmer: {
                    '0%': { transform: 'translateX(-100%) skewX(-15deg)' },
                    '100%': { transform: 'translateX(200%) skewX(-15deg)' },
                },
                float: {
                    '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
                    '33%': { transform: 'translate(30px, -30px) scale(1.1)' },
                    '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
                },
                rotate: {
                    '0%': { transform: 'rotate(0deg)' },
                    '100%': { transform: 'rotate(360deg)' },
                },
                'rainbow-flow': {
                    '0%': { backgroundPosition: '0% 50%' },
                    '50%': { backgroundPosition: '100% 50%' },
                    '100%': { backgroundPosition: '0% 50%' },
                },
                'pulse-glow': {
                    '0%, 100%': {
                        boxShadow: '0 0 20px rgba(147, 51, 234, 0.5), 0 0 40px rgba(79, 172, 254, 0.3)'
                    },
                    '50%': {
                        boxShadow: '0 0 40px rgba(147, 51, 234, 0.8), 0 0 80px rgba(79, 172, 254, 0.6)'
                    },
                },
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
                'gradient-rainbow': 'linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)',
            },
            boxShadow: {
                'neon': '0 0 30px rgba(147, 51, 234, 0.6), 0 0 60px rgba(79, 172, 254, 0.4)',
                'neon-strong': '0 0 40px rgba(147, 51, 234, 0.9), 0 0 80px rgba(79, 172, 254, 0.6)',
                'glow-pink': '0 0 30px rgba(240, 147, 251, 0.6)',
                'glow-blue': '0 0 30px rgba(79, 172, 254, 0.6)',
                'glow-green': '0 0 30px rgba(0, 242, 96, 0.6)',
            },
        },
    },
    plugins: [],
}
