export default {
    transform: {
        '^.+\\.jsx?$': 'babel-jest',
    },
    testEnvironment: 'jsdom',
    // setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
	setupFilesAfterEnv: ['./jest.setup.js'],
    moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
};
