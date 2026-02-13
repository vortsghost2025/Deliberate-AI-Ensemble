const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// Load environment variables
const envPath = path.join(__dirname, '.env');
const env = {};
if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
        const [key, value] = line.split('=');
        if (key && value) env[key.trim()] = value.trim();
    });
}

const PORT = 3000;

const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
};

const server = http.createServer((req, res) => {
    // Handle URL shortening API
    if (req.method === 'POST' && req.url === '/api/shorten') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const { url } = JSON.parse(body);
                
                const bitlyData = JSON.stringify({
                    long_url: url,
                    domain: 'bit.ly'
                });
                
                const options = {
                    hostname: 'api-ssl.bitly.com',
                    path: '/v4/shorten',
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${env.BITLY_TOKEN}`,
                        'Content-Type': 'application/json',
                        'Content-Length': bitlyData.length
                    }
                };
                
                const bitlyReq = https.request(options, bitlyRes => {
                    let data = '';
                    bitlyRes.on('data', chunk => data += chunk);
                    bitlyRes.on('end', () => {
                        if (bitlyRes.statusCode === 200 || bitlyRes.statusCode === 201) {
                            const response = JSON.parse(data);
                            res.writeHead(200, { 'Content-Type': 'application/json' });
                            res.end(JSON.stringify({ shortUrl: response.link }));
                        } else {
                            res.writeHead(500, { 'Content-Type': 'application/json' });
                            res.end(JSON.stringify({ error: 'Bitly API error', details: data }));
                        }
                    });
                });
                
                bitlyReq.on('error', error => {
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: error.message }));
                });
                
                bitlyReq.write(bitlyData);
                bitlyReq.end();
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid request' }));
            }
        });
        return;
    }
    
    // Default to index.html
    let filePath = req.url === '/' ? '/index.html' : req.url;
    
    // Remove query parameters for file lookup
    const urlWithoutQuery = filePath.split('?')[0];
    const fullPath = path.join(__dirname, urlWithoutQuery);
    
    // Get file extension
    const ext = path.extname(fullPath);
    const contentType = MIME_TYPES[ext] || 'text/plain';
    
    // Read and serve the file
    fs.readFile(fullPath, (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('<h1>404 - File Not Found</h1>');
            } else {
                res.writeHead(500);
                res.end('Server Error');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(data);
        }
    });
});

server.listen(PORT, () => {
    console.log(`🌱 WE4Free Connection Bridge running at:`);
    console.log(`   http://localhost:${PORT}`);
    console.log(``);
    console.log(`   Press Ctrl+C to stop`);
});
