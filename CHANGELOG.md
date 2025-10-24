# Changelog

## 2025-10-24 - API Key Authentication & Simplified Output

### Added
- **API Key Authentication**: All endpoints now require API key authentication via `X-API-Key` or `Authorization: Bearer` header
- **Authentication Library**: Created `lib/auth.py` with `validate_api_key()` and `send_unauthorized_response()` functions
- **API Authentication Documentation**: Created `API_AUTH.md` with complete guide on using API keys

### Changed
- **Simplified Agent Output**: `run_research_agent()` now returns the agent's JSON output directly instead of wrapping it in `output_text` and `output_parsed`
- **Endpoint Responses**: All research endpoints (`/api/research/quick` and `/api/research/run`) now return the agent's JSON output directly
- **CORS Headers**: Updated all endpoints to include `X-API-Key` and `Authorization` in allowed headers
- **Test Script**: Updated `test_agent.py` to work with new simplified output format
- **API Documentation**: Updated `/api` endpoint to show required authentication headers

### Security
- **Environment Variable**: New `API_KEY` environment variable controls authentication (authentication is disabled if not set)
- **Unauthorized Responses**: Proper 401 responses with helpful error messages for missing/invalid API keys

### Files Modified
- `lib/research_agent.py` - Simplified to return agent JSON directly
- `lib/auth.py` - New authentication utility (created)
- `api/health.py` - Added API key validation
- `api/index.py` - Added API key validation and updated docs
- `api/research/quick.py` - Added API key validation and simplified response
- `api/research/run.py` - Added API key validation and simplified response
- `test_agent.py` - Updated for new output format
- `vercel.json` - Removed secret references (using dashboard env vars)

### Migration Notes

**For Vercel Users:**
1. Add `API_KEY` environment variable in Vercel dashboard
2. Add `OPENAI_API_KEY` environment variable if not already set
3. Redeploy the application

**For API Consumers:**
1. Update all API calls to include `X-API-Key` header
2. Update response parsing - responses are now direct JSON from agent (no wrapper)

**Example Before:**
```json
{
  "success": true,
  "query": "...",
  "response": "...",
  "parsed": {...}
}
```

**Example After:**
```json
{
  "title": "...",
  "date_range": "...",
  "headline": "...",
  ...
}
```

