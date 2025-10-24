"""
Root endpoint - API information
GET /api or GET /api/index
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.auth import validate_api_key, send_unauthorized_response


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Validate API key
        if not validate_api_key(self):
            send_unauthorized_response(self)
            return
        
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        self.end_headers()
        
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
        
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        self.end_headers()
        return

