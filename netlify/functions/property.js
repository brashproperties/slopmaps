exports.handler = async function(event, context) {
  const https = require('https');
  
  const url = event.queryStringParameters.url;
  const apiKey = event.headers['x-api-key'];
  
  if (!url) {
    return { statusCode: 400, body: 'Missing url parameter' };
  }
  
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'x-api-key': apiKey || '',
        'Accept': 'application/json'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          statusCode: 200,
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
          },
          body: data
        });
      });
    });
    
    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
};
