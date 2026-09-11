/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        zomato: ["Nunito", "sans-serif"],
      },
      colors: {
        zomato: {
          red: "#E23744",
          dark: "#1C1C1C",
          muted: "#686B78",
          bg: "#F8F8F8",
        },
      },
      boxShadow: {
        card: "0 2px 8px rgba(0, 0, 0, 0.08)",
      },
    },
  },
  plugins: [],
};
