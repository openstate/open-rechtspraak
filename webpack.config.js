const path = require("path");
const webpack = require("webpack");

const debug = (process.env.NODE_ENV !== "production");
const rootAssetPath = path.join(__dirname, "assets");

module.exports = {
  // configuration
  context: rootAssetPath,
  entry: {
    scripts: "./scripts/main.ts",
    styles: "./styles/main.scss",
    scripts_docs: "./docs/scripts/docs.ts",
    styles_docs: "./docs/styles/docs.scss",
  },
  mode: debug,
  output: {
    chunkFilename: "[id].js",
    filename: "[name].js",
    path: path.join(__dirname, "app", "static", "dist"),
    publicPath: "/static/dist/",
  },
  resolve: {
    extensions: [".js", ".ts", ".tsx", ".scss"],
  },
  devtool: debug ? "source-map" : false,
  module: {
    rules: [
      {
        test: /\.(js|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
              '@babel/preset-typescript',
            ],
            plugins: ['@babel/transform-runtime'],
          },
        },
      },
      {
        test: /\.(png|jpg|ico|webp|svg|webmanifest|xml)$/i,
        type: 'asset/resource'
      },
      {
        test: /\.(woff|woff2)$/i,
        type: 'asset/resource'
      },
      {
        test: /.scss/,
        exclude: /node_modules/,
        type: "asset/resource",
        generator: {
          filename: "[name].css",
        },
        use: ["sass-loader"],
      },
    ],
  },
};
