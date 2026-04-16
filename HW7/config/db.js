const mongoose = require('mongoose');
const config = require('../config');

const connectDB = async () => {
  try {
    await mongoose.connect(config.MONGODB_URI, {
      serverSelectionTimeoutMS: 5000,
    });
    console.log(`MongoDB connected: ${config.MONGODB_URI}`);
  } catch (error) {
    throw new Error(`MongoDB connection failed for ${config.MONGODB_URI}: ${error.message}`);
  }
};

module.exports = connectDB;
