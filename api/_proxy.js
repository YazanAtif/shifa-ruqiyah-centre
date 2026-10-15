module.exports = async function proxyToVPS(endpoint, req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  const VPS_API_BASE = process.env.VPS_API_BASE || 'http://13.140.43.8:3005';

  try {
    let url = `${VPS_API_BASE}/api/${endpoint}`;
    const queryIdx = (req.url || '').indexOf('?');
    if (queryIdx !== -1) {
      url += req.url.slice(queryIdx);
    } else if (req.query && Object.keys(req.query).length > 0) {
      const q = new URLSearchParams(req.query).toString();
      url += `?${q}`;
    }

    const options = {
      method: req.method,
      headers: { 'Content-Type': 'application/json' }
    };

    if (req.method !== 'GET' && req.method !== 'HEAD' && req.body) {
      options.body = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
    }

    const upstream = await fetch(url, options);
    const data = await upstream.json();
    return res.status(upstream.status).json(data);
  } catch (err) {
    console.error(`Upstream error for /api/${endpoint}:`, err);
    return res.status(502).json({ error: 'Database service unreachable', details: err.message });
  }
};
