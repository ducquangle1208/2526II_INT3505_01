const client = require('prom-client');

// Create a Registry which registers the metrics
const register = new client.Registry();

// Add a default label which is added to all metrics
register.setDefaultLabels({
  app: 'hw10-products-api'
});

// Enable the collection of default metrics
client.collectDefaultMetrics({ register });

// Custom metric: HTTP request duration
const httpRequestDurationMicroseconds = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});

register.registerMetric(httpRequestDurationMicroseconds);

// Middleware to track request duration
const metricsMiddleware = (req, res, next) => {
  const end = httpRequestDurationMicroseconds.startTimer();
  res.on('finish', () => {
    // We try to get the route from the request, but it might not be set yet for all cases
    const route = req.route ? req.route.path : req.path;
    end({ method: req.method, route: route, code: res.statusCode });
  });
  next();
};

module.exports = {
  register,
  metricsMiddleware
};
