const config = require('./config');
const logger = require('./logger');
const ExpressServer = require('./expressServer');
const connectDB = require('./config/db');

const launchServer = async () => {
  try {
    await connectDB();
    const server = new ExpressServer(config.PORT, config.OPENAPI_PATH);
    server.launch();
    logger.info(`Server running on port ${config.PORT}`);
  } catch (error) {
    logger.error('Startup failed:', error);
    process.exit(1);
  }
};

launchServer();
