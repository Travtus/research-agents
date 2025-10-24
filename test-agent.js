#!/usr/bin/env node

/**
 * Test script for the Research Agent
 * Run with: node test-agent.js
 */

import { runResearchAgentWorkflow } from './lib/researchAgent.js';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

async function testAgent() {
  console.log('🚀 Testing AI Legislation Research Agent...\n');

  if (!process.env.OPENAI_API_KEY) {
    console.error('❌ Error: OPENAI_API_KEY not found in environment variables');
    console.error('Please create a .env file with your OpenAI API key\n');
    process.exit(1);
  }

  try {
    console.log('📝 Running query: "Generate the latest AI legislation brief for the past month"\n');
    
    const result = await runResearchAgentWorkflow({
      input_as_text: "Generate the latest AI legislation brief for the past month"
    });

    console.log('✅ Agent execution completed!\n');
    console.log('📊 Parsed Output:\n');
    console.log(JSON.stringify(result.output_parsed, null, 2));
    console.log('\n📄 Text Output:\n');
    console.log(result.output_text);

  } catch (error) {
    console.error('❌ Error running agent:', error.message);
    if (error.stack) {
      console.error('\nStack trace:', error.stack);
    }
    process.exit(1);
  }
}

// Run the test
testAgent();

