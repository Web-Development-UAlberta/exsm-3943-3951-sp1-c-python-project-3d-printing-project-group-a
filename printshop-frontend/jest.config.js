const nextJest = require("next/jest");

const createJestConfig = nextJest({
  dir: "./",
});

const config = {
  testEnvironment: "jsdom",
  //setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  setupFilesAfterEnv: ["/home/runner/work/exsm-3943-3951-sp1-c-python-project-3d-printing-project-group-a/printshop-frontend/jest.setup.js"],
  transform: {
    "^.+\\.(js|jsx|ts|tsx)$": ["babel-jest", { presets: ["next/babel"] }],
  },
};

module.exports = createJestConfig(config);
