# Quick Start Guide

Get your AI Legislation Research Agent API up and running in 5 minutes.

## 📋 Prerequisites

- Node.js 18+ installed
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Vercel account ([sign up here](https://vercel.com/signup))
- n8n instance (optional, for workflow automation)

## 🚀 Setup (Local Development)

### 1. Clone and Install

```bash
cd research-agents
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Test Locally

```bash
# Start Vercel dev server
npm run dev
```

The API will be available at `http://localhost:3000`

### 4. Test the Agent

In a new terminal:

```bash
# Test using curl
curl -X POST http://localhost:3000/api/research/quick \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate the latest AI legislation brief"}'
```

Or run the test script:

```bash
npm test
```

## ☁️ Deploy to Vercel (3 Steps)

### Option 1: Via Vercel Dashboard

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Add environment variable:
     - Name: `OPENAI_API_KEY`
     - Value: Your OpenAI API key
   - Click "Deploy"

3. **Test Your Deployment**
   ```bash
   curl -X POST https://your-project.vercel.app/api/research/quick \
     -H "Content-Type: application/json" \
     -d '{"query": "Generate the latest AI legislation brief"}'
   ```

### Option 2: Via CLI

```bash
# Login to Vercel
npx vercel login

# Add environment variable
npx vercel env add OPENAI_API_KEY production

# Deploy
npm run deploy
```

## 🔗 Connect to n8n

### 1. Import the Workflow

1. Open n8n
2. Click **Import from File**
3. Select `n8n-research-agent-workflow.json`
4. Update the API URL in the "Call Research Agent API" node to your Vercel URL

### 2. Test in n8n

1. Click "Execute Workflow"
2. Or trigger via webhook:

```bash
curl -X POST https://your-n8n-instance.com/webhook/ai-legislation \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate the latest AI legislation brief"}'
```

### 3. Example: Quick Query Workflow

Create a simple workflow in n8n:

```
[Manual Trigger] → [HTTP Request to API] → [Show Result]
```

**HTTP Request Node Config:**
- Method: POST
- URL: `https://your-vercel-url.vercel.app/api/research/quick`
- Body:
  ```json
  {
    "query": "Generate the latest AI legislation brief"
  }
  ```

## 📍 API Endpoints

### Health Check
```bash
GET /api/health
```

### Quick Research Query
```bash
POST /api/research/quick
Body: { "query": "your query here" }
```

### Full Research Workflow
```bash
POST /api/research/run
Body: { 
  "input_as_text": "Generate the latest AI legislation brief",
  "workflowId": "optional-workflow-id"
}
```

## 📊 Response Format

The research agent returns structured data:

```json
{
  "success": true,
  "data": {
    "output_parsed": {
      "Title": "AI & Chatbot Regulation — US C-Suite Brief",
      "Date": "Coverage: October 1-31, 2025",
      "Headline": "States accelerate AI governance...",
      "What Changed": "• California AB 123...",
      "Exec To-do": "1. Review compliance...",
      "Legislation Highlights": "• CA AB 123..."
    },
    "output_text": "{...JSON string...}"
  },
  "metadata": {
    "timestamp": "2025-10-24T12:00:00.000Z",
    "workflowId": "wf_..."
  }
}
```

## 🧪 Testing Examples

### 1. Basic Query
```bash
curl -X POST http://localhost:3000/api/research/quick \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest AI legislation"}'
```

### 2. With Workflow ID
```bash
curl -X POST http://localhost:3000/api/research/run \
  -H "Content-Type: application/json" \
  -d '{
    "input_as_text": "Generate AI legislation brief",
    "workflowId": "custom-workflow-123"
  }'
```

### 3. Custom Time Range
```bash
curl -X POST http://localhost:3000/api/research/quick \
  -H "Content-Type: application/json" \
  -d '{"query": "AI legislation changes in the past week"}'
```

## 🔧 Troubleshooting

### "OPENAI_API_KEY not found"
**Solution:** Make sure your `.env` file exists and contains your API key

### "Function execution timed out"
**Solution:** 
- Increase timeout in n8n HTTP Request node (set to 60000ms)
- For Vercel, upgrade to Pro plan for 60s timeout limit

### "Module not found"
**Solution:** Run `npm install` to install dependencies

### Agent returns error
**Solution:** Check your OpenAI API key is valid and has credits

## 📚 Next Steps

- ✅ Deploy to Vercel
- ✅ Test the API endpoints
- ✅ Import n8n workflow
- 📖 Read [N8N_INTEGRATION.md](N8N_INTEGRATION.md) for advanced workflows
- 📖 Read [DEPLOYMENT.md](DEPLOYMENT.md) for deployment details
- 🔧 Customize the agent in `lib/researchAgent.js`

## 💡 Tips

1. **Cost Management**: Monitor your OpenAI usage at [platform.openai.com/usage](https://platform.openai.com/usage)
2. **Performance**: The agent uses GPT-5 with web search, queries may take 15-30 seconds
3. **Caching**: Consider caching results for the same query within a time period
4. **Webhooks**: Set up n8n webhooks for automated daily/weekly reports

## 🆘 Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [N8N_INTEGRATION.md](N8N_INTEGRATION.md) for n8n setup
- Open an issue on GitHub
- Check OpenAI Agents SDK docs: [platform.openai.com/docs](https://platform.openai.com/docs)

---

**You're all set! 🎉** Your AI Legislation Research Agent is ready to use.

