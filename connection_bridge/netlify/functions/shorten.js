const https = require('https');

exports.handler = async (event) => {
    // Only allow POST requests
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const { url } = JSON.parse(event.body);
        
        // Bitly API token from environment variable
        const BITLY_TOKEN = process.env.BITLY_TOKEN;
        
        if (!BITLY_TOKEN) {
            return {
                statusCode: 500,
                body: JSON.stringify({ error: 'Bitly token not configured' })
            };
        }

        const bitlyData = JSON.stringify({
            long_url: url,
            domain: 'bit.ly'
        });

        // Make request to Bitly API
        const result = await new Promise((resolve, reject) => {
            const options = {
                hostname: 'api-ssl.bitly.com',
                path: '/v4/shorten',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${BITLY_TOKEN}`,
                    'Content-Type': 'application/json',
                    'Content-Length': bitlyData.length
                }
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    if (res.statusCode === 200 || res.statusCode === 201) {
                        resolve(JSON.parse(data));
                    } else {
                        reject(new Error(`Bitly API error: ${data}`));
                    }
                });
            });

            req.on('error', reject);
            req.write(bitlyData);
            req.end();
        });

        return {
            statusCode: 200,
            body: JSON.stringify({ shortUrl: result.link })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
