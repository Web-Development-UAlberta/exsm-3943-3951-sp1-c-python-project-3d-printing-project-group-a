const nextJest = require("next/jest");
const path = require('path');

const createJestConfig = nextJest({
  dir: "./",
});

const config = {
  setupFilesAfterEnv: [path.join(__dirname, 'jest.setup.js')],
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.(js|jsx|ts|tsx)$": ["babel-jest", { presets: ["next/babel"] }],
  },
};

module.exports = createJestConfig(config);