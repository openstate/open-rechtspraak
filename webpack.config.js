const path = require("path");
const webpack = require("webpack");
const CopyPlugin = require("copy-webpack-plugin");

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require("terser-webpack-plugin");

const debug = (process.env.NODE_ENV !== "production");
const rootAssetPath = path.join(__dirname, "assets");

module.exports = {
  // configuration
  context: rootAssetPath,
  entry: {
    scripts: "./scripts/main.js",
    styles: [
      path.join(__dirname, "assets", "styles", "main.scss"),
    ],
  },
  mode: debug,
  output: {
    chunkFilename: "[id].js",
    filename: "[name].js",
    path: path.join(__dirname, "app", "static", "dist"),
    publicPath: "/static/dist/",
  },
  resolve: {
    extensions: [".js", ".jsx", ".css", ".scss"],
  },
  devtool: debug ? "source-map" : false,
  plugins: [
    new webpack.ProvidePlugin({$: "jquery", jQuery: "jquery"}),
    new MiniCssExtractPlugin(),
    new CopyPlugin({
      patterns: [
        {from: "images", to: "images"}
      ]
    })
  ],
  module: {
    rules: [
      {
        test: /.s?css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
      },
      // {
      //   test: /\.js$/, exclude: /node_modules/, loader: "babel-loader", query: { presets: ["@babel/preset-env"], cacheDirectory: true },
      // },
    ],
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
        extractComments: false,
        terserOptions: {output: {comments: false}}
      }),
      new CssMinimizerPlugin(),
    ],
  },
};
