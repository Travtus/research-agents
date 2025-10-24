# n8n Integration Guide

Complete guide for integrating your Vercel-hosted Research Agents API with n8n.

## Prerequisites

1. Your API deployed to Vercel (see [DEPLOYMENT.md](DEPLOYMENT.md))
2. n8n instance running ([n8n.io](https://n8n.io) or self-hosted)
3. Your Vercel API URL

## Quick Start: Import Workflow

1. Copy the contents of `n8n-workflow-example.json`
2. In n8n, click **Menu** → **Import from File/URL**
3. Paste the JSON or upload the file
4. Update the API URL in the "Call Research Agent API" node
5. Activate the workflow

## Method 1: Simple HTTP Request

### Basic Query

1. Add **HTTP Request** node
2. Configure:
   - **Method**: POST
   - **URL**: `https://your-vercel-url.vercel.app/api/agent/run`
   - **Body Content Type**: JSON
   - **Specify Body**: Using Fields
   - Add field:
     - **Name**: `query`
     - **Value**: `{{ $json.query }}` or your static text

### Example Workflow: Webhook → Agent → Response

```
[Webhook] → [HTTP Request to Agent] → [Respond to Webhook]
```

**Configuration:**

**Node 1: Webhook**
- Path: `research`
- Method: POST
- Response Mode: Respond to Webhook

**Node 2: HTTP Request**
- Method: POST
- URL: `https://your-vercel-url.vercel.app/api/agent/run`
- Body Type: JSON
- JSON Body:
  ```json
  {
    "query": "{{ $json.body.question }}"
  }
  ```

**Node 3: Respond to Webhook**
- Response: `{{ $json }}`

### Test It

```bash
curl -X POST http://your-n8n-instance.com/webhook/research \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AI?"}'
```

## Method 2: Persistent Conversations

Create workflows that maintain conversation context using thread IDs.

### Workflow: Stateful Chat

```
[Webhook] → [HTTP Request] → [Set Variable] → [Respond]
```

**HTTP Request Configuration:**
```json
{
  "message": "{{ $json.body.message }}",
  "threadId": "{{ $json.body.threadId || '' }}",
  "assistantId": "asst_your_assistant_id"
}
```

The response includes `threadId` which you can store and reuse for follow-up messages.

## Method 3: Multi-Agent Workflow

Create complex workflows with multiple specialized agents.

### Example: Research → Summarize → Fact-Check

```
[Input] → [Research Agent] → [Summarizer Agent] → [Fact-Checker] → [Output]
```

**Node 2: Research Agent**
```json
{
  "query": "Research: {{ $json.topic }}",
  "assistantId": "asst_researcher_id"
}
```

**Node 3: Summarizer**
```json
{
  "query": "Summarize: {{ $node['Research Agent'].json.response }}",
  "assistantId": "asst_summarizer_id"
}
```

**Node 4: Fact-Checker**
```json
{
  "query": "Fact-check: {{ $node['Summarizer'].json.response }}",
  "assistantId": "asst_factchecker_id"
}
```

## Method 4: Scheduled Research

Set up automated research tasks.

### Example: Daily News Summary

```
[Cron] → [Get Topics] → [Loop] → [Agent API] → [Email Results]
```

**Node 1: Cron Trigger**
- Mode: Every Day
- Hour: 9
- Minute: 0

**Node 2: Agent API**
- URL: `https://your-vercel-url.vercel.app/api/agent/run`
- Body:
  ```json
  {
    "query": "Summarize the latest developments in {{ $json.topic }}"
  }
  ```

**Node 5: Email**
- Subject: `Daily Research Summary`
- Body: `{{ $json.response }}`

## Method 5: Database Integration

Store agent responses in a database.

### Example: Log All Queries

```
[Webhook] → [Agent API] → [Postgres/MySQL Node] → [Respond]
```

**Node 3: Postgres Insert**
```sql
INSERT INTO research_logs (query, response, timestamp)
VALUES (
  '{{ $json.query }}',
  '{{ $json.response }}',
  NOW()
)
```

## Advanced Patterns

### Pattern 1: Conditional Agent Selection

Use **IF** node to route to different agents based on query type.

```
[Input] → [IF] → [Technical Agent] or [Creative Agent] → [Merge] → [Output]
```

**IF Condition:**
```
{{ $json.query.includes('technical') }}
```

### Pattern 2: Parallel Research

Use **Split in Batches** to query multiple agents simultaneously.

```
[Topics] → [Split] → [Agent 1, Agent 2, Agent 3] → [Merge] → [Combine]
```

### Pattern 3: Retry Logic

Add **Error Trigger** and retry failed requests.

```
[Agent API] → [Error Trigger] → [Wait] → [Retry Agent API]
```

### Pattern 4: Rate Limiting

Use **Function** node to implement rate limiting.

```javascript
const lastCall = $node["Variables"].json.lastCall || 0;
const now = Date.now();
const minInterval = 1000; // 1 second

if (now - lastCall < minInterval) {
  await new Promise(r => setTimeout(r, minInterval - (now - lastCall)));
}

return { lastCall: Date.now() };
```

## Complete Example Workflows

### 1. Customer Support Bot

```json
{
  "name": "Customer Support with Research Agent",
  "nodes": [
    {
      "name": "Chat Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "support",
        "method": "POST"
      }
    },
    {
      "name": "Extract Question",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "values": {
          "string": [
            {
              "name": "question",
              "value": "={{ $json.body.message }}"
            }
          ]
        }
      }
    },
    {
      "name": "Call Research Agent",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-vercel-url.vercel.app/api/agent/chat",
        "bodyParametersJson": "={{ JSON.stringify({ message: $json.question, threadId: $json.body.threadId }) }}"
      }
    },
    {
      "name": "Log to Database",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "insert",
        "table": "support_logs",
        "columns": "question, answer, thread_id"
      }
    },
    {
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { answer: $json.response, threadId: $json.threadId } }}"
      }
    }
  ]
}
```

### 2. Content Generation Pipeline

```
[Cron/Manual] → [Get Topic] → [Research] → [Outline] → [Write] → [Edit] → [Save to CMS]
```

Each step calls the agent API with specialized prompts.

### 3. Slack Integration

```
[Slack Trigger] → [Agent API] → [Post to Slack]
```

**Slack Trigger:**
- Event: app_mention

**Agent API:**
- URL: Your Vercel API
- Query: `{{ $json.event.text }}`

**Post to Slack:**
- Channel: Same as trigger
- Text: `{{ $json.response }}`

## Testing in n8n

### Test Single Node

1. Select the HTTP Request node
2. Click **Execute Node**
3. View the output

### Test Entire Workflow

1. Click **Execute Workflow** button
2. Or trigger via webhook/cron

### Debug Tips

1. **Enable logging**: Add **Set** nodes to log intermediate values
2. **Use Function nodes**: Add console.log for debugging
3. **Check execution history**: View in n8n's Executions tab

## Error Handling

### Basic Error Handling

Add **Error Trigger** node:
```
[Main Workflow] → [Error Trigger] → [Send Alert] or [Retry]
```

### Timeout Handling

In HTTP Request node settings:
- **Timeout**: 30000 (30 seconds)
- **Retry on Fail**: Yes
- **Max Attempts**: 3

### Custom Error Responses

Use **IF** node to check for errors:
```
{{ $json.success === false }}
```

## Performance Optimization

1. **Batch requests**: Group multiple queries when possible
2. **Cache responses**: Store common queries in database
3. **Use webhooks**: Instead of polling
4. **Async processing**: For long-running tasks
5. **Parallel execution**: Use Split in Batches for independent queries

## Security Best Practices

1. **Validate inputs**: Use **IF** nodes to check data
2. **Rate limiting**: Implement in n8n or at API level
3. **Authentication**: Add API keys to your Vercel endpoints if needed
4. **Sanitize outputs**: Filter sensitive data before sending
5. **Secure webhooks**: Use webhook authentication tokens

## Monitoring

### Track API Calls

Add logging node after each API call:
```javascript
return [{
  timestamp: new Date().toISOString(),
  endpoint: '{{ $json.endpoint }}',
  status: '{{ $json.status }}',
  duration: '{{ $json.duration }}'
}];
```

### Set Up Alerts

Create workflow to monitor failures:
```
[Error Trigger] → [Email/Slack Alert]
```

## Common Issues & Solutions

### Issue: "Connection Timeout"
**Solution**: Increase timeout in HTTP Request node settings to 30000ms (30s)

### Issue: "CORS Error"
**Solution**: CORS is enabled by default. Check your n8n instance isn't blocking the request.

### Issue: "429 Rate Limit"
**Solution**: Add delay between requests or upgrade OpenAI plan

### Issue: "Thread ID Not Found"
**Solution**: Thread IDs expire. Implement logic to create new thread if old one fails

## Next Steps

1. ✅ Import example workflow
2. ✅ Test basic query
3. ✅ Set up persistent conversations
4. 📝 Create your custom workflows
5. 📊 Monitor and optimize
6. 🔒 Implement security measures

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [HTTP Request Node Docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [n8n Workflow Examples](https://n8n.io/workflows)

## Support

Need help? Check:
1. n8n execution logs
2. Vercel function logs
3. OpenAI API status
4. This repository's issues

---

**Pro Tip**: Start with the simple HTTP request workflow and gradually add complexity as you understand the flow!

