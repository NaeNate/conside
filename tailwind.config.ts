import { Config } from "tailwindcss"

const config: Config = {
  content: ["src/app/**/*.tsx", "src/components/*.tsx"],
  theme: {
    extend: {
      colors: {
        foreground: "#0b0b0b",
        background: "#fcfcfc",
        primary: "#b55585",
      },
    },
  },
}

export default config
