"""
Multifamily Regulation Tracker Agent
Using the official OpenAI Agents SDK for Python
"""

from agents import Agent, Runner, WebSearchTool
from pydantic import BaseModel
import json


class MultifamilyReport(BaseModel):
    """Structured output for multifamily regulation research"""
    Title: str
    Date: str
    Headline: str
    What_Changed: str
    Exec_Todo: str
    Regulation_Highlights: str


# Configure web search tool
web_search_tool = WebSearchTool(
    search_context_size="high"
)

# Define the multifamily regulation tracker agent
multifamily_agent = Agent(
    name="Multifamily Regulation Tracker Agent",
    instructions="""Search the latest changes in regulations affecting multifamily housing and property management across the United States in the past month, then draft a concise, C-suite-friendly regulatory newsletter in this exact format:

Multifamily Regulation — US C-Suite Brief
Coverage: [Insert date range for the past 30 days]

This month's headline
[1 short paragraph summarizing the most important regulatory development of the month; use plain English and business tone.]

⸻

What changed (why it matters)
•  [Summarize each major legislative or regulatory action: regulation name, jurisdiction, date, purpose, and impact on multifamily housing/property management.]
•  [Include short contextual explanation ("why it matters") for each.]
•  [Add 2–3 reputable source links per item: e.g. HousingWire, Multifamily Executive, National Apartment Association, state housing agencies, AP News.]

⸻

Exec To-Dos (now with context)
1.  [Describe top executive actions required, ordered by importance.]
2.  [Each item should include 1 sentence of context: why it matters, what to do, and expected outcome.]
3.  [Limit to 6–7 items. Use clear verbs ("Review", "Update", "Comply", "Train", "Monitor").]

⸻

Last 30 days — proposed/passed items (1-liners + links)
•  [Regulation identifier + status + concise one-liner on scope.] [Add source URLs at the end in parentheses.]
•  [Repeat for all relevant local, state or federal items.]

⸻

Formatting rules: Parse the output into JSON with the structure provided.
– Use Markdown headings, bullets, and dividers exactly as shown.
– Keep the tone executive-brief level (factual, direct, but engaging).
– Include live URLs for each cited source.
– Do not include commentary or speculation.
– Focus on regulations affecting: rent control, tenant protections, fair housing, building codes, energy efficiency, property taxes, eviction procedures, and affordable housing requirements.
– The total output should fit comfortably on one page when rendered in Notion or email.""",
    model="gpt-4o",  # Using gpt-4o as it's available and powerful
    tools=[web_search_tool],  # Enable web search
)


def run_multifamily_agent(input_text: str, workflow_id: str = None) -> dict:
    """
    Run the multifamily regulation tracker workflow
    
    Args:
        input_text: The query/prompt for the agent
        workflow_id: Optional workflow ID for tracing (not currently used)
        
    Returns:
        dict: The agent's JSON output
    """
    import asyncio
    
    try:
        # Get or create event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the agent asynchronously
        result = loop.run_until_complete(Runner.run(multifamily_agent, input_text))
        
        # Get the final output
        final_output = result.final_output
        
        if not final_output:
            raise ValueError("Agent returned no output")
        
        # If the output is already a dict, return it
        if isinstance(final_output, dict):
            return final_output
        
        # If it's a string, try to parse as JSON
        if isinstance(final_output, str):
            try:
                return json.loads(final_output)
            except json.JSONDecodeError:
                # If it's not valid JSON, return it wrapped in a simple structure
                return {
                    "response": final_output
                }
        
        # Fallback: return as-is
        return final_output
        
    except Exception as e:
        raise Exception(f"Error running multifamily agent: {str(e)}")


async def run_multifamily_agent_async(input_text: str, workflow_id: str = None) -> dict:
    """
    Async version of run_multifamily_agent
    
    Args:
        input_text: The query/prompt for the agent
        workflow_id: Optional workflow ID for tracing (not currently used)
        
    Returns:
        dict: The agent's JSON output
    """
    try:
        # Run the agent asynchronously
        result = await Runner.run(multifamily_agent, input_text)
        
        # Get the final output
        final_output = result.final_output
        
        if not final_output:
            raise ValueError("Agent returned no output")
        
        # If the output is already a dict, return it
        if isinstance(final_output, dict):
            return final_output
        
        # If it's a string, try to parse as JSON
        if isinstance(final_output, str):
            try:
                return json.loads(final_output)
            except json.JSONDecodeError:
                # If it's not valid JSON, return it wrapped in a simple structure
                return {
                    "response": final_output
                }
        
        # Fallback: return as-is
        return final_output
        
    except Exception as e:
        raise Exception(f"Error running multifamily agent: {str(e)}")

