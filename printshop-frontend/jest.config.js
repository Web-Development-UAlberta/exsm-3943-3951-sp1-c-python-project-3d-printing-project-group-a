const nextJest = require("next/jest");
const path = require("path");

const createJestConfig = nextJest({
  dir: "./",
});

const customJestConfig = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: [path.resolve(__dirname, "jest.setup.js")],
};

module.exports = createJestConfig(customJestConfig);
