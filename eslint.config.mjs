import { FlatCompat } from "@eslint/eslintrc";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname
});

const eslintConfig = [
  {
    ignores: [
      ".next/**",
      ".npm-cache/**",
      ".pytest_cache/**",
      ".venv/**",
      "next-env.d.ts",
      "node_modules/**",
      "aqualord.egg-info/**"
    ]
  },
  ...compat.extends("next/core-web-vitals", "next/typescript")
];

export default eslintConfig;
