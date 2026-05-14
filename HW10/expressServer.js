const fs = require('fs');
const http = require('http');
const path = require('path');
const yaml = require('js-yaml');
const express = require('express');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const OpenApiValidator = require('express-openapi-validator');
const rateLimit = require('express-rate-limit');
const controller = require('./controllers/DefaultController');
const { register, metricsMiddleware } = require('./metrics');
const logger = require('./logger');

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
    // 1. Prometheus Metrics (should be early)
    this.app.use(metricsMiddleware);

    this.app.use(cors());
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: false }));

    // 2. Request Logging (Winston)
    this.app.use((req, res, next) => {
      logger.info(`${req.method} ${req.url}`);
      next();
    });

    // 3. Rate Limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // Limit each IP to 100 requests per `window` (here, per 15 minutes)
      standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
      legacyHeaders: false, // Disable the `X-RateLimit-*` headers
      message: 'Too many requests from this IP, please try again after 15 minutes',
    });
    this.app.use('/products', limiter);

    this.app.get('/openapi', (req, res) => res.sendFile(this.openApiPath));
    this.app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(this.schema));

    // Expose metrics endpoint
    this.app.get('/metrics', async (req, res) => {
      res.setHeader('Content-Type', register.contentType);
      res.end(await register.metrics());
    });

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

      logger.error('API Error:', err);

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
