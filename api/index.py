"""
Root endpoint - API information
GET /api or GET /api/index
"""

import json
import os


def handler(request):
    """Vercel serverless function handler"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-API-Key, Authorization'
            },
            'body': ''
        }
    
    # Validate API key
    api_key = request.headers.get('x-api-key') or request.headers.get('X-API-Key')
    if not api_key:
        auth_header = request.headers.get('authorization') or request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            api_key = auth_header.replace('Bearer ', '')
    
    expected_key = os.getenv('API_KEY')
    if expected_key and api_key != expected_key:
        return {
            'statusCode': 401,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': 'Unauthorized - Invalid or missing API key'
            })
        }
    
    response = {
        'name': 'Research Agents API',
        'version': '1.0.0',
        'language': 'python',
        'description': 'AI Legislation Research Agent using OpenAI Agents SDK (Python)',
        'sdk': 'openai-agents (official Python SDK)',
        'endpoints': {
            'health': {
                'method': 'GET',
                'path': '/api/health',
                'description': 'Health check endpoint'
            },
            'quickResearch': {
                'method': 'POST',
                'path': '/api/research/quick',
                'description': 'Quick research query endpoint - Returns agent JSON output directly',
                'headers': {
                    'X-API-Key': 'string (required) - Your API key',
                    'Content-Type': 'application/json'
                },
                'body': {
                    'query': 'string (required)'
                }
            },
            'fullResearch': {
                'method': 'POST',
                'path': '/api/research/run',
                'description': 'Full research workflow - Returns agent JSON output directly',
                'headers': {
                    'X-API-Key': 'string (required) - Your API key',
                    'Content-Type': 'application/json'
                },
                'body': {
                    'input_as_text': 'string (required)',
                    'workflowId': 'string (optional)'
                }
            }
        },
        'documentation': 'https://github.com/your-username/research-agents',
        'status': 'operational',
        'timestamp': '2025-10-24T12:00:00.000Z'
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response)
    }
