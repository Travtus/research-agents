"""
AI Legislation Research Agent
Using the official OpenAI Agents SDK for Python
"""

from agents import Agent, Runner, WebSearchTool
from pydantic import BaseModel
import json
import os


class LegislationReport(BaseModel):
    """Structured output for legislation research"""
    Title: str
    Date: str
    Headline: str
    What_Changed: str
    Exec_Todo: str
    Legislation_Highlights: str


# Configure web search tool
web_search_tool = WebSearchTool(
    search_context_size="high"
)

# Define the research agent
research_agent = Agent(
    name="AI Legislation Research Agent",
    instructions="""Search the latest changes in legislation affecting artificial intelligence (AI) and chatbots across the United States in the past month, then draft a concise, C-suite-friendly regulatory newsletter in this exact format:

AI & Chatbot Regulation — US C-Suite Brief
Coverage: [Insert date range for the past 30 days]

This month's headline
[1 short paragraph summarizing the most important regulatory development of the month; use plain English and business tone.]

⸻

What changed (why it matters)
•  [Summarize each major legislative or regulatory action: bill name, state, date, purpose, and impact.]
•  [Include short contextual explanation ("why it matters") for each.]
•  [Add 2–3 reputable source links per item: e.g. TechCrunch, Skadden, Reuters, Gov.ca.gov, LegiScan, AP News.]

⸻

Exec To-Dos (now with context)
1.  [Describe top executive actions required, ordered by importance.]
2.  [Each item should include 1 sentence of context: why it matters, what to do, and expected outcome.]
3.  [Limit to 6–7 items. Use clear verbs ("Decide", "Ship", "Start", "Flow", "Adopt").]

⸻

Last 30 days — proposed/passed items (1-liners + links)
•  [Bill identifier + status + concise one-liner on scope.] [Add source URLs at the end in parentheses.]
•  [Repeat for all relevant state or federal items.]

⸻

Formatting rules: Parse the output into JSON with the structure provided.
– Use Markdown headings, bullets, and dividers exactly as shown.
– Keep the tone executive-brief level (factual, direct, but engaging).
– Include live URLs for each cited source.
– Do not include commentary or speculation.
– The total output should fit comfortably on one page when rendered in Notion or email.""",
    model="gpt-4o",  # Using gpt-4o as it's available and powerful
    tools=[web_search_tool],  # Enable web search
)


def run_research_agent(input_text: str, workflow_id: str = None) -> dict:
    """
    Run the research agent workflow
    
    Args:
        input_text: The query/prompt for the agent
        workflow_id: Optional workflow ID for tracing
        
    Returns:
        dict with output_text and output_parsed
    """
    try:
        # Run the agent
        result = Runner.run_sync(research_agent, input_text)
        
        # Get the final output
        final_output = result.final_output
        
        if not final_output:
            raise ValueError("Agent returned no output")
        
        # Try to parse as structured output
        try:
            # If the output is already structured
            if isinstance(final_output, dict):
                output_parsed = final_output
            else:
                # Try to parse as JSON
                output_parsed = json.loads(final_output)
        except (json.JSONDecodeError, TypeError):
            # If not JSON, return as text
            output_parsed = {
                "Title": "AI & Chatbot Regulation — US C-Suite Brief",
                "Date": "N/A",
                "Headline": final_output,
                "What_Changed": "",
                "Exec_Todo": "",
                "Legislation_Highlights": ""
            }
        
        return {
            "output_text": json.dumps(output_parsed, indent=2),
            "output_parsed": output_parsed
        }
        
    except Exception as e:
        raise Exception(f"Error running research agent: {str(e)}")


async def run_research_agent_async(input_text: str, workflow_id: str = None) -> dict:
    """
    Async version of run_research_agent
    
    Args:
        input_text: The query/prompt for the agent
        workflow_id: Optional workflow ID for tracing
        
    Returns:
        dict with output_text and output_parsed
    """
    try:
        # Run the agent asynchronously
        result = await Runner.run(research_agent, input_text)
        
        # Get the final output
        final_output = result.final_output
        
        if not final_output:
            raise ValueError("Agent returned no output")
        
        # Try to parse as structured output
        try:
            if isinstance(final_output, dict):
                output_parsed = final_output
            else:
                output_parsed = json.loads(final_output)
        except (json.JSONDecodeError, TypeError):
            output_parsed = {
                "Title": "AI & Chatbot Regulation — US C-Suite Brief",
                "Date": "N/A",
                "Headline": final_output,
                "What_Changed": "",
                "Exec_Todo": "",
                "Legislation_Highlights": ""
            }
        
        return {
            "output_text": json.dumps(output_parsed, indent=2),
            "output_parsed": output_parsed
        }
        
    except Exception as e:
        raise Exception(f"Error running research agent: {str(e)}")

