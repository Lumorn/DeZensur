// Jest-Konfiguration verwendet Babel-Jest zum Transformieren von TS/JSX
module.exports = {
  transform: {
    '^.+\\.(t|j)sx?$': 'babel-jest',
  },
  testEnvironment: 'jsdom',
};
