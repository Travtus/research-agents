# Deployment Guide

## Deploying to Vercel

### Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. An [OpenAI API key](https://platform.openai.com/api-keys)
3. [Vercel CLI](https://vercel.com/cli) (optional, for CLI deployment)

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Environment Variables**
   - In the "Configure Project" section, expand "Environment Variables"
   - Add the following:
     - **Name**: `OPENAI_API_KEY`
     - **Value**: Your OpenAI API key (starts with `sk-`)
     - **Environments**: Production, Preview, Development (select all)
   
   - (Optional) Add your assistant ID:
     - **Name**: `ASSISTANT_ID`
     - **Value**: Your assistant ID (starts with `asst_`)
     - **Environments**: Production, Preview, Development (select all)

4. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete (usually 1-2 minutes)
   - Your API will be live at: `https://your-project-name.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy: Yes
   - Which scope: Select your account
   - Link to existing project: No
   - Project name: (press Enter for default or specify)
   - Directory: `./` (press Enter)
   - Want to override settings: No

4. **Add Environment Variables**
   ```bash
   vercel env add OPENAI_API_KEY production
   # Paste your OpenAI API key when prompted
   
   vercel env add OPENAI_API_KEY preview
   # Paste your OpenAI API key when prompted
   
   vercel env add OPENAI_API_KEY development
   # Paste your OpenAI API key when prompted
   ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

### Method 3: One-Click Deploy

You can create a "Deploy to Vercel" button by adding this to your GitHub README:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/YOUR_REPO&env=OPENAI_API_KEY&envDescription=OpenAI%20API%20Key%20required%20for%20agent%20functionality)
```

## Verify Deployment

1. **Test Health Endpoint**
   ```bash
   curl https://your-project-name.vercel.app/api/health
   ```
   
   Expected response:
   ```json
   {
     "status": "ok",
     "timestamp": "2025-10-24T12:00:00.000Z",
     "service": "research-agents-api",
     "openaiConfigured": true
   }
   ```

2. **Test Agent Endpoint**
   ```bash
   curl -X POST https://your-project-name.vercel.app/api/agent/run \
     -H "Content-Type: application/json" \
     -d '{"query": "What is 2+2?"}'
   ```

## Getting Your Vercel URL

After deployment, your API URL will be:
- Production: `https://your-project-name.vercel.app`
- Preview deployments: `https://your-project-name-git-branch.vercel.app`

You can also:
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on your project
3. Copy the domain from the "Domains" section

## Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update your DNS settings as instructed by Vercel

## Monitoring and Logs

### View Logs
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click "Deployments"
4. Click on a deployment
5. View "Runtime Logs"

### View Function Metrics
1. In your project dashboard
2. Click "Analytics"
3. View request counts, errors, and performance metrics

## Updating Your Deployment

### Automatic Deployments (GitHub Integration)
- Every push to `main` branch triggers a production deployment
- Pull requests create preview deployments
- No manual action required

### Manual CLI Deployment
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Environment Variables Management

### Add a New Variable
```bash
vercel env add VARIABLE_NAME production
```

### Remove a Variable
```bash
vercel env rm VARIABLE_NAME production
```

### List All Variables
```bash
vercel env ls
```

### Pull Environment Variables Locally
```bash
vercel env pull .env.local
```

## Troubleshooting

### "Function execution timed out"
- **Cause**: Function took longer than Vercel's timeout limit (10s hobby, 60s pro)
- **Solution**: 
  - Upgrade to Vercel Pro for 60s timeout
  - Optimize your agent prompts
  - Implement async processing

### "OpenAI API Key not configured"
- **Cause**: Environment variable not set or not deployed
- **Solution**:
  ```bash
  vercel env add OPENAI_API_KEY production
  vercel --prod  # Redeploy
  ```

### Changes Not Reflected
- **Solution**: Make sure to redeploy after changing environment variables
  ```bash
  vercel --prod
  ```

### Build Fails
- Check the build logs in Vercel Dashboard
- Ensure `package.json` dependencies are correct
- Try building locally: `npm install`

## Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore` for a reason
2. **Use Vercel's environment variables** - They're encrypted at rest
3. **Rotate API keys regularly** - Update them in Vercel environment variables
4. **Enable rate limiting** - Consider using Vercel's Edge Config for rate limiting
5. **Monitor usage** - Check OpenAI and Vercel usage dashboards regularly

## Cost Considerations

### Vercel Costs
- **Hobby Plan** (Free):
  - 100GB bandwidth
  - 100 hours serverless function execution
  - 10 second function timeout
  
- **Pro Plan** ($20/month):
  - 1TB bandwidth
  - 1000 hours serverless function execution
  - 60 second function timeout

### OpenAI Costs
- Charged per token used
- GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
- Monitor usage at [platform.openai.com](https://platform.openai.com/usage)

## Next Steps

1. ✅ Deploy your API to Vercel
2. ✅ Get your production URL
3. ✅ Test the endpoints
4. 📝 Set up n8n integration (see main README.md)
5. 📊 Monitor usage and performance
6. 🔒 Set up custom domain (optional)

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Vercel Discord](https://vercel.com/discord)

