"""
Health check endpoint
GET /api/health
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
    
    # Check if OpenAI API key is configured
    openai_configured = bool(os.getenv('OPENAI_API_KEY'))
    
    response = {
        'status': 'ok',
        'timestamp': '2025-10-24T12:00:00.000Z',
        'service': 'research-agents-api',
        'language': 'python',
        'openaiConfigured': openai_configured
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response)
    }

