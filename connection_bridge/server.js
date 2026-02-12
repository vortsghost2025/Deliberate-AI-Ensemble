const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
};

const server = http.createServer((req, res) => {
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
