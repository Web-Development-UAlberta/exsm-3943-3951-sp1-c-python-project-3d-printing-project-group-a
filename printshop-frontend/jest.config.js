const nextJest = require("next/jest");
const path = require("path");

const createJestConfig = nextJest({
  dir: "./",
});

const customJestConfig = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: [path.join(__dirname, "jest.setup.js")],
};

module.exports = createJestConfig(customJestConfig);
