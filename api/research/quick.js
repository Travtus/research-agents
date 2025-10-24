import { runResearchAgentWorkflow } from '../../lib/researchAgent.js';

/**
 * API endpoint for quick research queries (simplified interface)
 * POST /api/research/quick
 * Body: { query } or { input_as_text }
 */
export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ 
      success: false,
      error: 'Method not allowed' 
    });
  }

  try {
    // Accept both 'query' and 'input_as_text' for flexibility
    const input_as_text = req.body.input_as_text || req.body.query;

    if (!input_as_text) {
      return res.status(400).json({
        success: false,
        error: 'Either "input_as_text" or "query" is required in request body'
      });
    }

    // Check for OpenAI API key
    if (!process.env.OPENAI_API_KEY) {
      return res.status(500).json({
        success: false,
        error: 'OPENAI_API_KEY environment variable is not set'
      });
    }

    // Run the research agent workflow
    const result = await runResearchAgentWorkflow({
      input_as_text,
      workflowId: req.body.workflowId
    });

    // Return simplified response for quick queries
    res.status(200).json({
      success: true,
      query: input_as_text,
      response: result.output_text,
      parsed: result.output_parsed,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error in quick research query:', error);
    
    res.status(500).json({
      success: false,
      error: error.message || 'An error occurred while processing your query',
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
}

