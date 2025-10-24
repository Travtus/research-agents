# Research Agents API

An AI Legislation Research Agent using OpenAI's Agents SDK, hosted on Vercel and designed for easy integration with n8n workflows.

## Features

- 🤖 AI Legislation Research Agent with web search capabilities
- 📊 Structured JSON output with Zod schema validation
- 🔍 Automated research on US AI & Chatbot legislation
- ⚡ Serverless deployment on Vercel
- 🔗 Easy integration with n8n workflows
- 🌐 CORS-enabled REST API
- 📝 C-suite friendly regulatory newsletters

## 🚀 Quick Start

**Get started in 5 minutes:** See [QUICKSTART.md](QUICKSTART.md) for a streamlined setup guide.

### 1. Installation

```bash
npm install
```

### 2. Environment Setup

Create a `.env` file:

```bash
cp .env.example .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. Local Development

```bash
# Start development server
npm run dev

# Test the agent (in another terminal)
npm test
```

The API will be available at `http://localhost:3000`

### 4. Deploy to Vercel

#### Option 1: Using Vercel Dashboard (Recommended)

1. Push code to GitHub
2. Import to Vercel at [vercel.com/new](https://vercel.com/new)
3. Add `OPENAI_API_KEY` environment variable
4. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

#### Option 2: Using Vercel CLI

```bash
npx vercel login
npx vercel env add OPENAI_API_KEY production
npm run deploy
```

## API Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running and configured properly.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-24T12:00:00.000Z",
  "service": "research-agents-api",
  "openaiConfigured": true
}
```

### Quick Research Query

**POST** `/api/research/quick`

Simplified endpoint for quick research queries.

**Request Body:**
```json
{
  "query": "Generate the latest AI legislation brief"
}
```

**Response:**
```json
{
  "success": true,
  "query": "Generate the latest AI legislation brief",
  "response": "{...JSON string...}",
  "parsed": {
    "Title": "AI & Chatbot Regulation — US C-Suite Brief",
    "Date": "Coverage: October 1-31, 2025",
    "Headline": "States accelerate AI governance...",
    "What Changed": "• California AB 123...",
    "Exec To-do": "1. Review compliance requirements...",
    "Legislation Highlights": "• CA AB 123: Passed..."
  },
  "timestamp": "2025-10-24T12:00:00.000Z"
}
```

### Full Research Workflow

**POST** `/api/research/run`

Complete research agent workflow with full metadata.

**Request Body:**
```json
{
  "input_as_text": "Generate the latest AI legislation brief for the past month",
  "workflowId": "custom-workflow-123"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "output_text": "{...JSON string...}",
    "output_parsed": {
      "Title": "AI & Chatbot Regulation — US C-Suite Brief",
      "Date": "Coverage: October 1-31, 2025",
      "Headline": "...",
      "What Changed": "...",
      "Exec To-do": "...",
      "Legislation Highlights": "..."
    }
  },
  "metadata": {
    "timestamp": "2025-10-24T12:00:00.000Z",
    "workflowId": "custom-workflow-123"
  }
}
```

### Legacy Endpoints (Assistants API)

The following endpoints are available for backward compatibility but not used by the main research agent:

- **POST** `/api/agent/create` - Create OpenAI Assistant
- **POST** `/api/agent/chat` - Chat with Assistant
- **POST** `/api/agent/run` - Run Assistant workflow

See the API files for details.

## n8n Integration

**Full integration guide:** See [N8N_INTEGRATION.md](N8N_INTEGRATION.md) for complete workflows and examples.

### Quick Setup

1. **Import the workflow:**
   - Open n8n
   - Import `n8n-research-agent-workflow.json`
   - Update the API URL to your Vercel deployment

2. **Configure HTTP Request node:**
   - Method: POST
   - URL: `https://your-vercel-url.vercel.app/api/research/quick`
   - Body: `{ "query": "Generate AI legislation brief" }`
   - Timeout: 60000ms (60 seconds)

3. **Test it:**
   ```bash
   curl -X POST https://your-n8n.com/webhook/ai-legislation \
     -H "Content-Type: application/json" \
     -d '{"query": "Generate the latest AI legislation brief"}'
   ```

### Example n8n Workflow Structure

```
[Webhook/Cron] → [HTTP Request to API] → [Format Data] → [Send to Slack/Email/Database]
```

**Common Use Cases:**
- 📅 Daily/weekly automated legislation reports
- 📧 Email C-suite with latest updates
- 💬 Slack bot for on-demand queries
- 🗄️ Store reports in database/CMS
- 🔄 Multi-agent research pipelines

## Agent Configuration

The research agent is configured in `lib/researchAgent.js`:

- **Model**: GPT-5 with reasoning
- **Tools**: Web search with high context size
- **Output Schema**: Structured JSON with Zod validation
- **Features**: 
  - Searches latest US AI/chatbot legislation
  - Generates C-suite friendly newsletters
  - Includes source links and executive action items

### Customizing the Agent

Edit `lib/researchAgent.js` to modify:
- Instructions/prompts
- Output schema structure
- Search parameters
- Model settings
- Reasoning effort level

### Environment Variables

Set in Vercel or `.env`:

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `WORKFLOW_ID` (optional): Custom workflow ID for tracing
- `NODE_ENV` (optional): Set to `development` for detailed error messages

### Performance Notes

- **Typical execution time**: 15-30 seconds
- **Vercel timeout**: 10s (Hobby), 60s (Pro)
- **Recommendation**: Use Vercel Pro for production
- The agent performs web searches which adds processing time

## Examples

### cURL Examples

**Health Check:**
```bash
curl https://your-vercel-url.vercel.app/api/health
```

**Quick Research Query:**
```bash
curl -X POST https://your-vercel-url.vercel.app/api/research/quick \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate the latest AI legislation brief"}'
```

**Full Workflow with Custom ID:**
```bash
curl -X POST https://your-vercel-url.vercel.app/api/research/run \
  -H "Content-Type: application/json" \
  -d '{
    "input_as_text": "Generate AI legislation brief for the past week",
    "workflowId": "weekly-report-001"
  }'
```

**Custom Time Range:**
```bash
curl -X POST https://your-vercel-url.vercel.app/api/research/quick \
  -H "Content-Type: application/json" \
  -d '{"query": "Search AI legislation changes in California in the past 2 weeks"}'
```

### JavaScript/Node.js Example

```javascript
const response = await fetch('https://your-vercel-url.vercel.app/api/research/quick', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'Generate the latest AI legislation brief'
  })
});

const data = await response.json();
console.log(data.parsed.Title);
console.log(data.parsed.Headline);
```

### Python Example

```python
import requests

response = requests.post(
    'https://your-vercel-url.vercel.app/api/research/quick',
    json={'query': 'Generate the latest AI legislation brief'}
)

data = response.json()
print(data['parsed']['Title'])
print(data['parsed']['Headline'])
```

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**
   - Set in Vercel environment variables
   - Or add to `.env` file for local development
   - Redeploy after adding

2. **"Function execution timed out"**
   - Research agent needs 15-30 seconds typically
   - Upgrade to Vercel Pro (60s timeout)
   - Or use a different hosting platform
   - In n8n: set HTTP Request timeout to 60000ms

3. **"Agent result is undefined"**
   - Check OpenAI API key is valid
   - Ensure you have credits in your OpenAI account
   - Check OpenAI status at status.openai.com

4. **"Module not found @openai/agents"**
   - Run `npm install`
   - Make sure `package.json` has `"type": "module"`

5. **CORS errors**
   - CORS is enabled by default
   - Check browser/n8n console for specific errors
   - Verify the API URL is correct

## License

ISC

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

