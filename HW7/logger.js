const formatArg = (arg) => {
  if (arg instanceof Error) {
    return arg.stack || arg.message;
  }
  return arg;
};

module.exports = {
  info: (...args) => console.log('[INFO]', ...args.map(formatArg)),
  error: (...args) => console.error('[ERROR]', ...args.map(formatArg)),
};
