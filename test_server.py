#!/usr/bin/env python3
"""
Simple HTTP test server for local API testing
Run: python test_server.py
Then: curl http://localhost:8000/health
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from lib.research_agent import run_research_agent

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'ok',
                'service': 'research-agents-api',
                'openaiConfigured': bool(os.getenv('OPENAI_API_KEY'))
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/research':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            query = data.get('query', 'Generate AI legislation brief')
            
            try:
                result = run_research_agent(query)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    'success': True,
                    'query': query,
                    'parsed': result['output_parsed']
                }
                self.wfile.write(json.dumps(response, indent=2).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {'success': False, 'error': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    print('🚀 Starting test server on http://localhost:8000')
    print('   GET  /health')
    print('   POST /research')
    print('\nTest with:')
    print('   curl http://localhost:8000/health')
    print('   curl -X POST http://localhost:8000/research -H "Content-Type: application/json" -d \'{"query": "Latest AI laws"}\'')
    print('\nPress Ctrl+C to stop\n')
    
    server = HTTPServer(('localhost', 8000), TestHandler)
    server.serve_forever()

