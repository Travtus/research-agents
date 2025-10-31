# API Authentication Guide

## Overview

All API endpoints are protected with API key authentication. You must include your API key in the request headers to access any endpoint.

## Setting Up Your API Key

### For Vercel Deployment

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add a new variable:
   - **Name**: `API_KEY`
   - **Value**: Your chosen API key (e.g., a random UUID or secure string)
   - **Environment**: Select all (Production, Preview, Development)
4. Click **Save**
5. Redeploy your application

### For Local Development

Add the `API_KEY` to your `.env` file:

```bash
API_KEY=your-secret-api-key-here
OPENAI_API_KEY=your-openai-api-key
```

**Note:** If `API_KEY` is not set, authentication is disabled (useful for local testing).

## Making Authenticated Requests

Include your API key in one of two ways:

### Option 1: X-API-Key Header (Recommended)

```bash
curl -X POST https://your-domain.vercel.app/api/research/quick \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{"query": "Your research query"}'
```

### Option 2: Authorization Bearer Header

```bash
curl -X POST https://your-domain.vercel.app/api/research/quick \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -d '{"query": "Your research query"}'
```

## API Endpoints

All endpoints require authentication:

### 1. Health Check
```bash
GET /api/health
Headers:
  - X-API-Key: your-secret-api-key-here

Response:
{
  "status": "ok",
  "timestamp": "2025-10-24T12:00:00.000Z",
  "service": "research-agents-api",
  "language": "python",
  "openaiConfigured": true
}
```

### 2. API Information
```bash
GET /api
Headers:
  - X-API-Key: your-secret-api-key-here

Response: (Shows all available endpoints and their documentation)
```

### 3. Quick Research
```bash
POST /api/research/quick
Headers:
  - X-API-Key: your-secret-api-key-here
  - Content-Type: application/json

Body:
{
  "query": "Your research query here"
}

Response: (Direct JSON output from the AI agent)
```

### 4. Full Research Workflow
```bash
POST /api/research/run
Headers:
  - X-API-Key: your-secret-api-key-here
  - Content-Type: application/json

Body:
{
  "input_as_text": "Your research query here",
  "workflowId": "optional-workflow-id"
}

Response: (Direct JSON output from the AI agent)
```

## Error Responses

### 401 Unauthorized
Returned when API key is missing or invalid:

```json
{
  "success": false,
  "error": "Unauthorized - Invalid or missing API key",
  "message": "Please provide a valid API key in the X-API-Key header or Authorization: Bearer header"
}
```

### 400 Bad Request
Returned when required parameters are missing:

```json
{
  "success": false,
  "error": "input_as_text is required"
}
```

### 500 Internal Server Error
Returned when there's an error processing the request:

```json
{
  "success": false,
  "error": "Error message here"
}
```

## JavaScript/TypeScript Example

```typescript
const response = await fetch('https://your-domain.vercel.app/api/research/quick', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-secret-api-key-here'
  },
  body: JSON.stringify({
    query: 'Generate the latest AI legislation brief for the past month'
  })
});

const result = await response.json();
console.log(result);
```

## Python Example

```python
import requests

url = 'https://your-domain.vercel.app/api/research/quick'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-secret-api-key-here'
}
data = {
    'query': 'Generate the latest AI legislation brief for the past month'
}

response = requests.post(url, json=data, headers=headers)
result = response.json()
print(result)
```

## Security Best Practices

1. **Never commit your API key to version control**
   - Add `.env` to your `.gitignore`
   - Use environment variables for all sensitive data

2. **Use strong API keys**
   - Generate random, long strings (e.g., UUIDs)
   - Rotate keys periodically

3. **Use HTTPS only**
   - Never send API keys over unencrypted connections

4. **Keep keys secret**
   - Don't share API keys in public channels
   - Use separate keys for different environments

5. **Monitor usage**
   - Check Vercel logs for unauthorized access attempts
   - Rotate keys if you suspect compromise

## Generating a Secure API Key

Use one of these methods to generate a secure API key:

### Using Python
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(api_key)
```

### Using OpenSSL
```bash
openssl rand -base64 32
```

### Using UUID
```bash
uuidgen
```

## Troubleshooting

**Issue:** Getting 401 Unauthorized errors
- **Solution:** Check that your API key is correct and properly formatted in the header

**Issue:** API works locally but not on Vercel
- **Solution:** Make sure you've added the `API_KEY` environment variable in Vercel settings and redeployed

**Issue:** Want to disable authentication for testing
- **Solution:** Remove or don't set the `API_KEY` environment variable (authentication will be bypassed)

