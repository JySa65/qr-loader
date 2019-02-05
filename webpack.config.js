const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const miniCssExtractPlugin = new MiniCssExtractPlugin({
	filename: 'main.css',
})
module.exports = {
	mode: "development",
	entry: './src/index.js',
	output: {
		filename: 'main.js',
		path: path.resolve(__dirname, 'static')
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				loader: "babel-loader"
			},
			{
				test: /\.(css|scss)$/,
				use: [
					'style-loader',
					MiniCssExtractPlugin.loader,
					'css-loader',
					'sass-loader'
				]
			}
		]
	},
	plugins: 
		[miniCssExtractPlugin]
};
