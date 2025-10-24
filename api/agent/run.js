import OpenAI from 'openai';

/**
 * API endpoint for a complete agent workflow
 * POST /api/agent/run
 * Body: { query, assistantId, systemPrompt }
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
      query,
      assistantId,
      systemPrompt = 'You are a helpful research assistant that provides detailed and accurate information.'
    } = req.body;

    if (!query) {
      return res.status(400).json({
        success: false,
        error: 'Query is required'
      });
    }

    let finalAssistantId = assistantId || process.env.ASSISTANT_ID;

    // If no assistant ID provided, create a temporary one
    if (!finalAssistantId) {
      const assistant = await openai.beta.assistants.create({
        name: 'Temporary Research Agent',
        instructions: systemPrompt,
        model: 'gpt-4-turbo-preview',
        tools: [{ type: 'code_interpreter' }],
      });
      finalAssistantId = assistant.id;
    }

    // Create thread
    const thread = await openai.beta.threads.create();

    // Add message
    await openai.beta.threads.messages.create(thread.id, {
      role: 'user',
      content: query,
    });

    // Run assistant
    const run = await openai.beta.threads.runs.create(thread.id, {
      assistant_id: finalAssistantId,
    });

    // Poll for completion
    let runStatus = await openai.beta.threads.runs.retrieve(thread.id, run.id);
    let attempts = 0;
    const maxAttempts = 60;

    while (runStatus.status !== 'completed' && runStatus.status !== 'failed' && attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 500));
      runStatus = await openai.beta.threads.runs.retrieve(thread.id, run.id);
      attempts++;
    }

    if (runStatus.status === 'failed') {
      return res.status(500).json({
        success: false,
        error: 'Assistant run failed',
        details: runStatus.last_error
      });
    }

    if (attempts >= maxAttempts) {
      return res.status(408).json({
        success: false,
        error: 'Request timeout'
      });
    }

    // Get response
    const messages = await openai.beta.threads.messages.list(thread.id);
    const lastMessage = messages.data[0];

    res.status(200).json({
      success: true,
      query,
      response: lastMessage.content[0].text.value,
      assistantId: finalAssistantId,
      threadId: thread.id,
      messageId: lastMessage.id
    });
  } catch (error) {
    console.error('Error running agent:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}

