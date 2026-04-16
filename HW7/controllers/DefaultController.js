const Controller = require('./Controller');
const service = require('../services/DefaultService');

const create_product = async (request, response) => {
  try {
    const result = await service.create_product({ product: request.body });
    Controller.sendResponse(response, result.payload, result.code);
  } catch (error) {
    Controller.sendError(response, error);
  }
};

const get_products = async (request, response) => {
  try {
    const result = await service.get_products();
    Controller.sendResponse(response, result.payload, result.code);
  } catch (error) {
    Controller.sendError(response, error);
  }
};

const update_product = async (request, response) => {
  try {
    const result = await service.update_product({
      id: request.params.id,
      product: request.body,
    });
    Controller.sendResponse(response, result.payload, result.code);
  } catch (error) {
    Controller.sendError(response, error);
  }
};

const delete_product = async (request, response) => {
  try {
    const result = await service.delete_product({ id: request.params.id });
    Controller.sendResponse(response, result.payload, result.code);
  } catch (error) {
    Controller.sendError(response, error);
  }
};

module.exports = {
  create_product,
  get_products,
  update_product,
  delete_product,
};
