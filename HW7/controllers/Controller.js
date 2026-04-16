class Controller {
  static sendResponse(response, payload, code = 200) {
    response.status(code).json(payload);
  }

  static sendError(response, error) {
    response.status(error.code || 500).json({
      message: error.message || 'Internal Server Error',
    });
  }
}

module.exports = Controller;
