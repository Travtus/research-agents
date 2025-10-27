"""
Full multifamily regulation tracker workflow endpoint
POST /api/multifamily/run
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.multifamily_agent import run_multifamily_agent


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
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
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Check for OpenAI API key
            if not os.getenv('OPENAI_API_KEY'):
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'OPENAI_API_KEY environment variable is not set'
                }).encode())
                return
            
            # Run the agent with a simple trigger - the agent knows what to do
            workflow_id = data.get('workflowId')
            result = run_multifamily_agent("Generate the report", workflow_id)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        self.end_headers()

