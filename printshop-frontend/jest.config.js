const nextJest = require("next/jest");
const path = require("path");

const createJestConfig = nextJest({
  dir: "./",
});

const customJestConfig = {
  testEnvironment: "jsdom",
};

const jestConfig = createJestConfig(customJestConfig);

// IMPORTANT: inject setup AFTER next/jest processing
jestConfig.setupFilesAfterEnv = [path.resolve(__dirname, "jest.setup.js")];

module.exports = jestConfig;
