const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: './assets/scripts/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'core', 'static')
    },
    module: {
        rules: [
        {
            test: /\.css$/,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'postcss-loader', // Use PostCSS for Tailwind
            ],
        },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
        filename: 'bundle.css', // Output CSS file
        }),
    ],
}