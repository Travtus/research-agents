import OpenAI from 'openai';

/**
 * API endpoint to chat with an OpenAI Assistant
 * POST /api/agent/chat
 * Body: { message, threadId, assistantId }
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

    const { message, threadId, assistantId } = req.body;

    if (!message) {
      return res.status(400).json({
        success: false,
        error: 'Message is required'
      });
    }

    const finalAssistantId = assistantId || process.env.ASSISTANT_ID;
    if (!finalAssistantId) {
      return res.status(400).json({
        success: false,
        error: 'Assistant ID is required. Either pass it in the request or set ASSISTANT_ID environment variable.'
      });
    }

    // Create or use existing thread
    let thread;
    if (threadId) {
      thread = { id: threadId };
    } else {
      thread = await openai.beta.threads.create();
    }

    // Add message to thread
    await openai.beta.threads.messages.create(thread.id, {
      role: 'user',
      content: message,
    });

    // Run the assistant
    const run = await openai.beta.threads.runs.create(thread.id, {
      assistant_id: finalAssistantId,
    });

    // Poll for completion
    let runStatus = await openai.beta.threads.runs.retrieve(thread.id, run.id);
    let attempts = 0;
    const maxAttempts = 60; // 30 seconds timeout

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
        error: 'Request timeout',
        threadId: thread.id,
        runId: run.id
      });
    }

    // Get messages
    const messages = await openai.beta.threads.messages.list(thread.id);
    const lastMessage = messages.data[0];

    res.status(200).json({
      success: true,
      response: lastMessage.content[0].text.value,
      threadId: thread.id,
      messageId: lastMessage.id,
      runId: run.id
    });
  } catch (error) {
    console.error('Error in chat:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}

