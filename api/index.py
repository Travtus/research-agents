"""
Root endpoint - API information
GET /api or GET /api/index
"""

from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
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
                    'description': 'Quick research query endpoint',
                    'body': {
                        'query': 'string (required)'
                    }
                },
                'fullResearch': {
                    'method': 'POST',
                    'path': '/api/research/run',
                    'description': 'Full research workflow with metadata',
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
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

