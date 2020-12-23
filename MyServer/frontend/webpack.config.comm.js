const path = require('path')
const WebpackBar = require('webpackbar')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  mode: 'development',
  entry: './src/main.js', // 输出到根目录外
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.svg$/,
        loader: 'svg-sprite-loader',
        options: {
          symbolId: 'icon-[name]', // 将id变为icon-logo这种形式
          publicPath: path.resolve(__dirname, './src/icons/svg')
        }
      },
      {
        test: /\.js$/,
        use: 'babel-loader'
      },
      {
        test: /\.(eot|jpe?g|svg|ttf|woff|woff2)$/,
        loader: 'url-loader',
        exclude: path.resolve(__dirname, './src/icons/svg')
      }
    ]
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src') // 定义@为src目录，import xx from '@/icons' 相当于 from 'src/icons'
    },
    extensions: ['.js', '.vue'] // 这样就不需要在import from中写尾缀
  },
  plugins: [
    new CleanWebpackPlugin(),
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({
      template: 'index.html',
      filename: 'index.html',
      favicon: 'favicon.ico',
      inject: true
    }),
    new CopyWebpackPlugin([
      { from: path.join(__dirname, 'src', 'assets'), to: path.join(__dirname, 'dist/static/img'), toType: 'dir' }
    ]),
    new WebpackBar()
  ]
}
