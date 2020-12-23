const path = require('path')
const merge = require('webpack-merge')
const common = require('./webpack.config.comm')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = merge(common, {
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.css|\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
          {
            loader: 'sass-resources-loader',
            options: {
              resources: path.resolve(__dirname, './src/styles/index.scss')
            }
          }
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'main.css'
    })
  ]
})
