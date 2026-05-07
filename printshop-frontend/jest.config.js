const nextJest = require("next/jest");

const createJestConfig = nextJest({
  dir: "./printshop-frontend",
});

const customJestConfig = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
};

module.exports = createJestConfig(customJestConfig);
