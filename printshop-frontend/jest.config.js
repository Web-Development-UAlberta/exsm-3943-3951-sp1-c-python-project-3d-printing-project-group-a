const path = require("path");

module.exports = {
  rootDir: ".", // IMPORTANT: locks Jest to printshop-frontend folder

  testEnvironment: "jsdom",

  setupFilesAfterEnv: [path.resolve(__dirname, "jest.setup.js")],

  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
  },

  testPathIgnorePatterns: ["/node_modules/", "/.next/"],
};
