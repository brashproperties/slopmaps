const https = require('https');

exports.handler = async function(event, context) {
  const { url, apiKey } = JSON.parse(event.body);
  
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'x-api-key': apiKey,
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
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
};
