"""
Full research workflow endpoint
POST /api/research/run
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.research_agent import run_research_agent


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Get input_as_text from body
            input_as_text = data.get('input_as_text')
            
            if not input_as_text:
                self.send_error_response(
                    400,
                    'input_as_text is required'
                )
                return
            
            # Check for OpenAI API key
            if not os.getenv('OPENAI_API_KEY'):
                self.send_error_response(
                    500,
                    'OPENAI_API_KEY environment variable is not set'
                )
                return
            
            # Run the agent
            workflow_id = data.get('workflowId', 'wf_68fb4285b7848190a7d1feb126fe069e056baab3ea0bf879')
            result = run_research_agent(input_as_text, workflow_id)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                'success': True,
                'data': {
                    'output_text': result['output_text'],
                    'output_parsed': result['output_parsed']
                },
                'metadata': {
                    'timestamp': '2025-10-24T12:00:00.000Z',
                    'workflowId': workflow_id
                }
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
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

