class Service {
  static successResponse(payload, code = 200) {
    return { payload, code };
  }

  static rejectResponse(message, code = 500) {
    const error = new Error(message);
    error.code = code;
    return error;
  }
}

module.exports = Service;
