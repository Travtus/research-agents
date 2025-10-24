"""
Health check endpoint
GET /api/health
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
        
        # Check if OpenAI API key is configured
        openai_configured = bool(os.getenv('OPENAI_API_KEY'))
        
        response = {
            'status': 'ok',
            'timestamp': '2025-10-24T12:00:00.000Z',
            'service': 'research-agents-api',
            'language': 'python',
            'openaiConfigured': openai_configured
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

