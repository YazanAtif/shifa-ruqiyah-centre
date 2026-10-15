const proxyToVPS = require('./_proxy');

module.exports = async function handler(req, res) {
  return proxyToVPS('data', req, res);
};
