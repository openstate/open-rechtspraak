module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['./scripts'],
  setupFilesAfterEnv: ['./__tests__/setupTests.ts'],
};
