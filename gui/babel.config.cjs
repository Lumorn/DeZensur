// Babel-Konfiguration für Jest und Vite
module.exports = {
  presets: [
    ['@babel/preset-env', { targets: { node: 'current' } }],
    '@babel/preset-typescript',
    '@babel/preset-react',
  ],
  plugins: [
    // Ermöglicht die Verwendung von import.meta im Testumfeld
    'babel-plugin-transform-import-meta',
  ],
};
