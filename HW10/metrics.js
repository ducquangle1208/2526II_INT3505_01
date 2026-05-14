const client = require('prom-client');

const register = new client.Registry();

register.setDefaultLabels({
  app: 'hw10-products-api'
});

client.collectDefaultMetrics({ register });

const httpRequestDurationMicroseconds = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});

register.registerMetric(httpRequestDurationMicroseconds);

const metricsMiddleware = (req, res, next) => {
  const end = httpRequestDurationMicroseconds.startTimer();
  res.on('finish', () => {
    const route = req.route ? req.route.path : req.path;
    end({ method: req.method, route: route, code: res.statusCode });
  });
  next();
};

module.exports = {
  register,
  metricsMiddleware
};
