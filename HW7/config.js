const path = require('path');

const config = {
  PORT: process.env.PORT || 8080,
  MONGODB_URI: process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/hw7_products',
  OPENAPI_PATH: path.join(__dirname, 'api', 'openapi.yaml'),
};

module.exports = config;
