const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 6010;
const MCP_API_URL = process.env.MCP_API_URL || 'https://api.githubcopilot.com/';
const GITHUB_MCP_PAT = process.env.GITHUB_MCP_PAT;

// Print the actual API URL for debugging
console.log(`Using MCP API URL: ${MCP_API_URL}`);

if (!GITHUB_MCP_PAT) {
  console.warn('WARNING: GITHUB_MCP_PAT environment variable is not set');
}

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '10mb' }));
app.use(bodyParser.text({ limit: '10mb' }));

// Debug middleware - log all requests
app.use((req, res, next) => {
  console.log(`[DEBUG] ${req.method} ${req.url}`);
  next();
});

// Health endpoint
app.get('/health', (req, res) => {
  console.log('[HEALTH] Health check endpoint accessed');
  res.status(200).send('MCP proxy is healthy');
});

// Root endpoint
app.get('/', (req, res) => {
  console.log('[ROOT] Root endpoint accessed');
  res.send('GitHub MCP Proxy Server');
});

// SSE endpoint for streaming completions
app.get('/sse', (req, res) => {
  console.log('[SSE] Client connected to SSE endpoint');
  
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send a heartbeat every 30 seconds
  const intervalId = setInterval(() => {
    res.write('event: heartbeat\ndata: {}\n\n');
  }, 30000);

  // Clean up when client disconnects
  req.on('close', () => {
    console.log('[SSE] Client disconnected from SSE endpoint');
    clearInterval(intervalId);
  });
});

// Proxy endpoint for GitHub Copilot MCP API completions
app.post('/completions', async (req, res) => {
  try {
    console.log('[COMPLETIONS] Received completion request');
    const url = `${MCP_API_URL}completions`; // Removed v1/ from path
    
    console.log(`[COMPLETIONS] Sending request to: ${url}`);
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GITHUB_MCP_PAT}`,
        'User-Agent': 'GitHub-Copilot-MCP-Proxy/1.0'
      },
      body: JSON.stringify(req.body)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[COMPLETIONS] Error from GitHub API (${response.status}):`, errorText);
      return res.status(response.status).send(errorText);
    }
    
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('[COMPLETIONS] Error forwarding request:', error);
    res.status(500).json({ error: 'Failed to forward request to GitHub Copilot API' });
  }
});

// Chat completions endpoint
app.post('/chat/completions', async (req, res) => {
  try {
    console.log('[CHAT] Received chat completion request');
    const url = `${MCP_API_URL}chat/completions`; // Removed v1/ from path
    
    console.log(`[CHAT] Sending request to: ${url}`);
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GITHUB_MCP_PAT}`,
        'User-Agent': 'GitHub-Copilot-MCP-Proxy/1.0'
      },
      body: JSON.stringify(req.body)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[CHAT] Error from GitHub API (${response.status}):`, errorText);
      return res.status(response.status).send(errorText);
    }
    
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('[CHAT] Error forwarding request:', error);
    res.status(500).json({ error: 'Failed to forward request to GitHub Copilot API' });
  }
});

// Catch all other routes
app.use((req, res) => {
  console.log(`[ERROR] Unhandled route: ${req.method} ${req.path}`);
  res.status(404).send('Not Found');
});

// Add route debugging function
const logAllRoutes = () => {
  const routes = [];
  app._router.stack.forEach(middleware => {
    if (middleware.route) {
      // Route middleware
      routes.push({
        path: middleware.route.path,
        methods: Object.keys(middleware.route.methods).join(', ')
      });
    }
  });
  console.log('Registered routes:', routes);
};

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`MCP proxy server running on port ${PORT}`);
  console.log(`Health endpoint: http://localhost:${PORT}/health`);
  console.log(`API endpoints: /completions, /chat/completions`);
  
  // Log all registered routes
  logAllRoutes();
  
  // Test internal routes with IPv4 address
  console.log('Testing internal routes...');
  fetch(`http://127.0.0.1:${PORT}/health`)
    .then(response => response.text())
    .then(text => console.log('Internal health check response:', text))
    .catch(err => console.error('Internal health check failed:', err));
});