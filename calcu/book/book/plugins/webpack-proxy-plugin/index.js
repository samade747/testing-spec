// book/plugins/webpack-proxy-plugin/index.js
module.exports = function (context, options) {
  return {
    name: "custom-webpack-proxy-plugin",
    configureWebpack(config, isServer, utils) {
      return {
        mergeStrategy: {
          "devServer.proxy": "replace"
        },
        devServer: {
          proxy: {
            "/api": {
              target: "http://localhost:8000",
              secure: false,
              changeOrigin: true,
              logLevel: "debug",
            },
          },
        },
      };
    },
  };
};