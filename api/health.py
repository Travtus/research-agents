"""
Health check endpoint
GET /api/health
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys

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
        
        # Check if OpenAI API key is configured
        openai_configured = bool(os.getenv('OPENAI_API_KEY'))
        
        response = {
            'status': 'ok',
            'timestamp': '2025-10-24T12:00:00.000Z',
            'service': 'research-agents-api',
            'language': 'python',
            'openaiConfigured': openai_configured
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

