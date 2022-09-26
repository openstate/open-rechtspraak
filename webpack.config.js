const path = require("path");
const webpack = require("webpack");

const CopyPlugin = require("copy-webpack-plugin");

const debug = (process.env.NODE_ENV !== "production");
const rootAssetPath = path.join(__dirname, "assets");

module.exports = {
  // configuration
  context: rootAssetPath,
  entry: {
    scripts: "./scripts/onload.ts",
    scripts: "./scripts/main.ts",
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
    extensions: [".ts", ".tsx", ".scss"],
  },
  devtool: debug ? "source-map" : false,
  plugins: [
    new CopyPlugin({
      patterns: [
        {from: "images", to: "images"}
      ]
    })
  ],
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(png|jpg|ico|webp|svg|webmanifest|xml)$/i,
        type: 'asset/resource'
      },
      {
        test: /.scss/,
        exclude: /node_modules/,
        type: "asset/resource",
        generator: {
          filename: "styles.css",
        },
        use: ["sass-loader"],
      },
    ],
  },
};
