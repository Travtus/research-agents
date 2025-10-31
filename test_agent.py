#!/usr/bin/env python3
"""
Test script for the Research Agent
Run with: python test_agent.py
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add lib to path
sys.path.insert(0, os.path.dirname(__file__))

from lib.research_agent import run_research_agent


def test_agent():
    print('🚀 Testing AI Legislation Research Agent...\n')
    
    if not os.getenv('OPENAI_API_KEY'):
        print('❌ Error: OPENAI_API_KEY not found in environment variables')
        print('Please create a .env file with your OpenAI API key\n')
        sys.exit(1)
    
    try:
        print('📝 Running query: "Generate the latest AI legislation brief for the past month"\n')
        
        result = run_research_agent(
            "Generate the latest AI legislation brief for the past month"
        )
        
        print('✅ Agent execution completed!\n')
        print('📊 Agent JSON Output:\n')
        print(json.dumps(result, indent=2))
        print('\n' + '='*80 + '\n')
        
    except Exception as e:
        print(f'❌ Error running agent: {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    test_agent()

