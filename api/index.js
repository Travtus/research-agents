/**
 * Root endpoint - API information
 * GET /api or GET /api/index
 */
export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  res.status(200).json({
    name: 'Research Agents API',
    version: '1.0.0',
    description: 'AI Legislation Research Agent using OpenAI Agents SDK',
    endpoints: {
      health: {
        method: 'GET',
        path: '/api/health',
        description: 'Health check endpoint'
      },
      quickResearch: {
        method: 'POST',
        path: '/api/research/quick',
        description: 'Quick research query endpoint',
        body: {
          query: 'string (required)'
        }
      },
      fullResearch: {
        method: 'POST',
        path: '/api/research/run',
        description: 'Full research workflow with metadata',
        body: {
          input_as_text: 'string (required)',
          workflowId: 'string (optional)'
        }
      }
    },
    documentation: 'https://github.com/your-username/research-agents',
    status: 'operational',
    timestamp: new Date().toISOString()
  });
}

