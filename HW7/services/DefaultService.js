const mongoose = require('mongoose');
const Service = require('./Service');
const Product = require('../models/Product');

const create_product = async ({ product }) => {
  try {
    const createdProduct = await Product.create(product);
    return Service.successResponse(createdProduct, 201);
  } catch (error) {
    throw Service.rejectResponse(error.message || 'Invalid input', 400);
  }
};

const get_products = async () => {
  try {
    const products = await Product.find().sort({ createdAt: -1 });
    return Service.successResponse(products);
  } catch (error) {
    throw Service.rejectResponse(error.message || 'Unable to fetch products', 500);
  }
};

const update_product = async ({ id, product }) => {
  if (!mongoose.Types.ObjectId.isValid(id)) {
    throw Service.rejectResponse('Invalid product id', 400);
  }

  try {
    const updatedProduct = await Product.findByIdAndUpdate(id, product, {
      new: true,
      runValidators: true,
    });

    if (!updatedProduct) {
      throw Service.rejectResponse('Product not found', 404);
    }

    return Service.successResponse(updatedProduct);
  } catch (error) {
    if (error.code) {
      throw error;
    }
    throw Service.rejectResponse(error.message || 'Unable to update product', 400);
  }
};

const delete_product = async ({ id }) => {
  if (!mongoose.Types.ObjectId.isValid(id)) {
    throw Service.rejectResponse('Invalid product id', 400);
  }

  try {
    const deletedProduct = await Product.findByIdAndDelete(id);

    if (!deletedProduct) {
      throw Service.rejectResponse('Product not found', 404);
    }

    return Service.successResponse({ message: 'Product deleted', id });
  } catch (error) {
    if (error.code) {
      throw error;
    }
    throw Service.rejectResponse(error.message || 'Unable to delete product', 400);
  }
};

module.exports = {
  create_product,
  get_products,
  update_product,
  delete_product,
};
