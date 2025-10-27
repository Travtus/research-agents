"""
Root endpoint - API information
GET /api or GET /api/index
"""

from http.server import BaseHTTPRequestHandler
import json
import os


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Validate API key
        api_key = self.headers.get('x-api-key') or self.headers.get('X-API-Key')
        if not api_key:
            auth_header = self.headers.get('authorization') or self.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                api_key = auth_header.replace('Bearer ', '')
        
        expected_key = os.getenv('API_KEY')
        if expected_key and api_key != expected_key:
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'Unauthorized - Invalid or missing API key'
            }).encode())
            return
        
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
                'description': 'AI Legislation Research - Quick query endpoint',
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
                'description': 'AI Legislation Research - Full workflow',
                'headers': {
                    'X-API-Key': 'string (required) - Your API key',
                    'Content-Type': 'application/json'
                },
                'body': {
                    'input_as_text': 'string (required)',
                    'workflowId': 'string (optional)'
                }
            },
            'quickMultifamily': {
                'method': 'POST',
                'path': '/api/multifamily/quick',
                'description': 'Multifamily Regulation Tracker - Quick query endpoint',
                'headers': {
                    'X-API-Key': 'string (required) - Your API key',
                    'Content-Type': 'application/json'
                },
                'body': {
                    'query': 'string (required)'
                }
            },
            'fullMultifamily': {
                'method': 'POST',
                'path': '/api/multifamily/run',
                'description': 'Multifamily Regulation Tracker - Full workflow',
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
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        self.end_headers()
