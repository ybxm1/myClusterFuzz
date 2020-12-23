const FriendlyErrorsWebpackPlugin = require('friendly-errors-webpack-plugin')
const common = require('./webpack.config.comm')
const merge = require('webpack-merge')
const webpack = require('webpack')
const path = require('path')

module.exports = merge(common, {
  mode: 'development',
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.css|\.scss$/,
        use: [
          'vue-style-loader',
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
  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    compress: false,
    hot: true,
    open: true,
    quiet: true, // 不显示devServer信息
    overlay: true, // 编译出现错误时将错误显示在页面中
    proxy: {
      // '/': 'http://192.168.1.177',
      '/': 'http://127.0.0.1:5000',
      changeOrigin: true
    }
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new FriendlyErrorsWebpackPlugin({
      compilationSuccessInfo: {
        messages: ['Application running in http://localhost:8080/']
      },
      clearConsole: true
    })
  ]
})
