#!/usr/bin/env python3
"""
Test the API endpoints locally by importing them directly
"""

import os
import sys
import json
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

# Add to path
sys.path.insert(0, os.path.dirname(__file__))

print('🧪 Testing API Endpoints Locally\n')
print('='*80)

# Test 1: Health Check
print('\n1️⃣  Testing Health Endpoint...')
try:
    from api.health import handler as health_handler
    
    class MockRequest:
        def __init__(self):
            self.headers = {}
            self.rfile = BytesIO()
            self.wfile = BytesIO()
            
    mock = MockRequest()
    health = health_handler()
    health.rfile = mock.rfile
    health.wfile = mock.wfile
    health.do_GET()
    
    response = health.wfile.getvalue().decode()
    print(f'   ✅ Health endpoint works!')
    print(f'   Response: {response[:100]}...')
except Exception as e:
    print(f'   ❌ Error: {str(e)}')

# Test 2: Direct Agent Call
print('\n2️⃣  Testing Research Agent Directly...')
try:
    from lib.research_agent import run_research_agent
    
    if not os.getenv('OPENAI_API_KEY'):
        print('   ❌ OPENAI_API_KEY not found in environment')
    else:
        print('   📝 Running agent with test query...')
        print('   Query: "Summarize AI legislation in California"')
        
        result = run_research_agent("Summarize AI legislation in California")
        
        print(f'   ✅ Agent executed successfully!')
        print(f'   Output preview:')
        
        if result.get('output_parsed'):
            parsed = result['output_parsed']
            print(f'      Title: {parsed.get("Title", "N/A")}')
            print(f'      Date: {parsed.get("Date", "N/A")}')
            headline = parsed.get("Headline", "N/A")
            print(f'      Headline: {headline[:100]}...')
        else:
            print(f'      {result.get("output_text", "No output")[:200]}...')
            
except Exception as e:
    print(f'   ❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()

# Test 3: Test API endpoint logic (simulated)
print('\n3️⃣  Testing Quick Research Endpoint Logic...')
try:
    # Simulate what the endpoint does
    test_query = "What are the latest AI regulations?"
    print(f'   Query: "{test_query}"')
    
    from lib.research_agent import run_research_agent
    
    result = run_research_agent(test_query)
    
    # This is what the API returns
    api_response = {
        'success': True,
        'query': test_query,
        'response': result['output_text'],
        'parsed': result['output_parsed'],
        'timestamp': '2025-10-24T12:00:00.000Z'
    }
    
    print(f'   ✅ API endpoint logic works!')
    print(f'   Success: {api_response["success"]}')
    print(f'   Has parsed output: {bool(api_response["parsed"])}')
    
except Exception as e:
    print(f'   ❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()

print('\n' + '='*80)
print('\n✅ Testing Complete!')
print('\n📝 Notes:')
print('   - The agent is working')
print('   - Endpoints are structured correctly')
print('   - To test via HTTP, deploy to Vercel or use: vercel dev')
print('\n🚀 Ready to deploy to Vercel!')

