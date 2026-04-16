const fs = require('fs');
const http = require('http');
const path = require('path');
const yaml = require('js-yaml');
const express = require('express');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const OpenApiValidator = require('express-openapi-validator');
const controller = require('./controllers/DefaultController');

class ExpressServer {
  constructor(port, openApiPath) {
    this.port = port;
    this.openApiPath = openApiPath;
    this.app = express();
    this.schema = yaml.load(fs.readFileSync(openApiPath, 'utf8'));
    this.setupMiddleware();
    this.setupRoutes();
    this.setupErrorHandler();
  }

  setupMiddleware() {
    this.app.use(cors());
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: false }));
    this.app.get('/openapi', (req, res) => res.sendFile(this.openApiPath));
    this.app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(this.schema));
    this.app.use(
      OpenApiValidator.middleware({
        apiSpec: this.openApiPath,
        validateRequests: true,
        validateResponses: false,
      }),
    );
  }

  setupRoutes() {
    this.app.get('/products', controller.get_products);
    this.app.post('/products', controller.create_product);
    this.app.put('/products/:id', controller.update_product);
    this.app.delete('/products/:id', controller.delete_product);
  }

  setupErrorHandler() {
    this.app.use((err, req, res, next) => {
      if (res.headersSent) {
        next(err);
        return;
      }

      res.status(err.status || 500).json({
        message: err.message || 'Internal Server Error',
        errors: err.errors || [],
      });
    });
  }

  launch() {
    this.server = http.createServer(this.app).listen(this.port);
  }
}

module.exports = ExpressServer;
