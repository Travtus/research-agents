# Python Quick Start Guide

Get your AI Legislation Research Agent API (Python) up and running in 5 minutes.

## 📋 Prerequisites

- Python 3.9+ installed
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Vercel account ([sign up here](https://vercel.com/signup))

## 🚀 Setup (Local Development)

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Already created! Just verify your API key is in .env
cat .env
```

Should contain:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Test the Agent Locally

```bash
# Run the test script
python test_agent.py
```

This will:
- Load your OpenAI API key
- Run the research agent
- Print the structured output

**Expected output:**
```
🚀 Testing AI Legislation Research Agent...

📝 Running query: "Generate the latest AI legislation brief for the past month"

✅ Agent execution completed!

📊 Parsed Output:
{
  "Title": "AI & Chatbot Regulation — US C-Suite Brief",
  "Date": "Coverage: October 1-31, 2025",
  ...
}
```

## ☁️ Deploy to Vercel (3 Steps)

### Option 1: Via Vercel Dashboard (Easiest)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Convert to Python with official OpenAI Agents SDK"
   git push origin initial-setup
   ```

2. **Import to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - **Framework Preset**: Other (Vercel auto-detects Python)
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
vercel login

# Add environment variable
vercel env add OPENAI_API_KEY production

# Deploy
vercel --prod
```

## 🔗 Connect to n8n

### 1. Import the Workflow

1. Open n8n
2. Click **Import from File**
3. Select `n8n-research-agent-workflow.json`
4. Update the API URL in the "Call Research Agent API" node to your Vercel URL

### 2. Test in n8n

```bash
curl -X POST https://your-n8n-instance.com/webhook/ai-legislation \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate the latest AI legislation brief"}'
```

## 📍 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/research/quick` | POST | Quick queries |
| `/api/research/run` | POST | Full workflow with metadata |
| `/api` | GET | API information |

## 🧪 Testing Examples

### Health Check
```bash
curl https://your-vercel-url.vercel.app/api/health
```

### Quick Query
```bash
curl -X POST https://your-vercel-url.vercel.app/api/research/quick \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest AI legislation"}'
```

### Python Script
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

## 🔧 Local Development with Vercel Dev

Vercel CLI supports Python:

```bash
# Install Vercel CLI
npm install -g vercel

# Run local development server
vercel dev
```

Then test:
```bash
curl http://localhost:3000/api/health
```

## 📊 What's Different from JavaScript?

✅ **Using official Python SDK** (`openai-agents`)  
✅ **Better documentation** ([openai.github.io/openai-agents-python/](https://openai.github.io/openai-agents-python/))  
✅ **More stable** - Public SDK vs internal tool  
✅ **Community support** - More examples and resources  

## 🎯 Project Structure

```
research-agents/
├── api/                     # Python serverless functions
│   ├── health.py           # Health check
│   ├── index.py            # API info
│   └── research/
│       ├── quick.py        # Quick endpoint
│       └── run.py          # Full workflow
├── lib/
│   └── research_agent.py   # Core agent logic
├── requirements.txt         # Python dependencies
├── test_agent.py           # Test script
├── vercel.json             # Vercel config (Python)
└── .env                    # Environment variables
```

## 🔑 Key Files

### `lib/research_agent.py`
Core research agent using official OpenAI Agents SDK:
```python
from agents import Agent, Runner

research_agent = Agent(
    name="AI Legislation Research Agent",
    instructions="...",
    model="gpt-4o"
)

def run_research_agent(input_text: str) -> dict:
    result = Runner.run_sync(research_agent, input_text)
    return {"output_parsed": result.final_output}
```

### `api/research/quick.py`
Vercel Python serverless function:
```python
from http.server import BaseHTTPRequestHandler
from lib.research_agent import run_research_agent

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle request
        result = run_research_agent(query)
        # Return JSON response
```

## 📚 Official SDK Documentation

- **Python SDK Docs**: [openai.github.io/openai-agents-python/](https://openai.github.io/openai-agents-python/)
- **Quickstart**: [Agents SDK Quickstart](https://openai.github.io/openai-agents-python/quickstart/)
- **Examples**: [Agents SDK Examples](https://openai.github.io/openai-agents-python/examples/)

## 🆘 Troubleshooting

### "No module named 'agents'"
```bash
pip install openai-agents
```

### "OPENAI_API_KEY not found"
```bash
# Check .env file exists
cat .env

# Or set directly
export OPENAI_API_KEY=sk-your-key-here
```

### "Function execution timed out" on Vercel
- Agent takes 15-30 seconds typically
- Upgrade to Vercel Pro (60s timeout)
- Or optimize the agent instructions

## ✅ Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with OpenAI API key
- [ ] Local test successful (`python test_agent.py`)
- [ ] Code pushed to GitHub
- [ ] Deployed to Vercel
- [ ] Environment variable set in Vercel
- [ ] API endpoints tested
- [ ] n8n workflow imported and configured

## 🎊 You're Ready!

Your Python-based AI Research Agent is ready to deploy!

**Quick test command:**
```bash
python test_agent.py
```

Then deploy:
```bash
git push origin initial-setup
# Import to Vercel from GitHub
```

Happy researching! 🚀

