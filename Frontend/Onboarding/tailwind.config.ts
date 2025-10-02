// tailwind.config.ts
import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      fontFamily: {
        grotesk: ['Space Grotesk', 'Noto Sans', 'sans-serif'],
      },
    },
  },
} satisfies Config;
