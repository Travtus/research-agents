import { runResearchAgentWorkflow } from '../../lib/researchAgent.js';

/**
 * API endpoint to run the AI Legislation Research Agent
 * POST /api/research/run
 * Body: { input_as_text, workflowId }
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
    const { input_as_text, workflowId } = req.body;

    if (!input_as_text) {
      return res.status(400).json({
        success: false,
        error: 'input_as_text is required'
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
      workflowId
    });

    res.status(200).json({
      success: true,
      data: {
        output_text: result.output_text,
        output_parsed: result.output_parsed
      },
      metadata: {
        timestamp: new Date().toISOString(),
        workflowId: workflowId || "wf_68fb4285b7848190a7d1feb126fe069e056baab3ea0bf879"
      }
    });
  } catch (error) {
    console.error('Error running research agent:', error);
    
    res.status(500).json({
      success: false,
      error: error.message || 'An error occurred while running the research agent',
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
}

