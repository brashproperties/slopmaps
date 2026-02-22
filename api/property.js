// Vercel API route - deploy to Vercel for instant proxy
// Save as /api/property.js

export default async function handler(req, res) {
  const { url, key } = req.query;
  
  if (!url) {
    return res.status(400).json({ error: 'Missing url parameter' });
  }
  
  const response = await fetch(url, {
    headers: {
      'x-api-key': key || '',
      'Accept': 'application/json'
    }
  });
  
  const data = await response.json();
  res.status(response.status).json(data);
}
