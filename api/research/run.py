"""
Full research workflow endpoint
POST /api/research/run
"""

import json
import sys
import os

# Add parent directory to path to import lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.research_agent import run_research_agent


def handler(request):
    """Vercel serverless function handler"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-API-Key, Authorization'
            },
            'body': ''
        }
    
    try:
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
        
        # Parse request body
        body = request.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        data = json.loads(body) if body else {}
        
        # Get input_as_text from body
        input_as_text = data.get('input_as_text')
        
        if not input_as_text:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'input_as_text is required'
                })
            }
        
        # Check for OpenAI API key
        if not os.getenv('OPENAI_API_KEY'):
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'OPENAI_API_KEY environment variable is not set'
                })
            }
        
        # Run the agent and get JSON output directly
        workflow_id = data.get('workflowId')
        result = run_research_agent(input_as_text, workflow_id)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }
