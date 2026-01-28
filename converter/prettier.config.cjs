/** @type {import('prettier').Config} */

const config = {
  plugins: [
    require.resolve("@prettier/plugin-xml"),
    require.resolve("prettier-plugin-toml"),
  ],
  bracketSpacing: false,
  printWidth: 88,
  proseWrap: "always",
  semi: true,
  trailingComma: "es5",
  xmlWhitespaceSensitivity: "ignore",
};

module.exports = config;
