const path = require("path");

module.exports = {
  testEnvironment: "jsdom",

  setupFilesAfterEnv: [path.join(__dirname, "jest.setup.js")],

  moduleNameMapper: {
    "^@/(.*)$": path.join(__dirname, "$1"),
  },

  testPathIgnorePatterns: ["/node_modules/", "/.next/"],
};
