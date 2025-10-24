import OpenAI from 'openai';

/**
 * API endpoint to create a new OpenAI Assistant
 * POST /api/agent/create
 * Body: { name, instructions, model, tools }
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
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    const {
      name = 'Research Agent',
      instructions = 'You are a helpful research assistant.',
      model = 'gpt-4-turbo-preview',
      tools = [{ type: 'code_interpreter' }]
    } = req.body;

    const assistant = await openai.beta.assistants.create({
      name,
      instructions,
      model,
      tools,
    });

    res.status(200).json({
      success: true,
      assistant: {
        id: assistant.id,
        name: assistant.name,
        model: assistant.model,
        instructions: assistant.instructions,
        tools: assistant.tools,
      }
    });
  } catch (error) {
    console.error('Error creating assistant:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}

