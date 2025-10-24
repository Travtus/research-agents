"""
Quick research query endpoint
POST /api/research/quick
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.research_agent import run_research_agent
from lib.auth import validate_api_key, send_unauthorized_response


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Validate API key first
        if not validate_api_key(self):
            send_unauthorized_response(self)
            return
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Get query from body
            query = data.get('query') or data.get('input_as_text')
            
            if not query:
                self.send_error_response(
                    400,
                    'Either "query" or "input_as_text" is required in request body'
                )
                return
            
            # Check for OpenAI API key
            if not os.getenv('OPENAI_API_KEY'):
                self.send_error_response(
                    500,
                    'OPENAI_API_KEY environment variable is not set'
                )
                return
            
            # Run the agent and get JSON output directly
            result = run_research_agent(query, data.get('workflowId'))
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
            self.end_headers()
            
            # Return the agent's JSON output directly
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        self.end_headers()
        return
    
    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'success': False,
            'error': message
        }
        
        self.wfile.write(json.dumps(response).encode())

