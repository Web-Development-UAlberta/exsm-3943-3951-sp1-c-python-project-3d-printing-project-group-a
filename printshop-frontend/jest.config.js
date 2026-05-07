const nextJest = require("next/jest");
const path = require("path");

const createJestConfig = nextJest({
  dir: "./",
});

const customConfig = {
  testEnvironment: "jsdom",

  // IMPORTANT: use absolute path (CI-safe)
  setupFilesAfterEnv: [path.resolve(__dirname, "jest.setup.js")],

  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
  },

  testPathIgnorePatterns: ["<rootDir>/.next/", "<rootDir>/node_modules/"],
};

module.exports = createJestConfig(customConfig);
