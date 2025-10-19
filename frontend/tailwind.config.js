/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "media",
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular"],
      },
      boxShadow: {
        soft: "0 6px 24px rgba(0,0,0,.25)",
        inner: "inset 0 1px 0 rgba(255,255,255,.06)",
      },
      colors: {
        brand: { DEFAULT: "#7c3aed" },
      },
    },
  },
  plugins: [],
};
