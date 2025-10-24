import { webSearchTool, Agent, Runner, withTrace } from "@openai/agents";
import { z } from "zod";

// Tool definitions
const webSearchPreview = webSearchTool({
  userLocation: {
    type: "approximate",
    country: undefined,
    region: undefined,
    city: undefined,
    timezone: undefined
  },
  searchContextSize: "high"
});

// Output schema for the research agent
const ResearchAgentSchema = z.object({
  Title: z.string(),
  Date: z.string(),
  Headline: z.string(),
  "What Changed": z.string(),
  "Exec To-do": z.string(),
  "Legislation Highlights": z.string()
});

// Create the research agent
const researchAgent = new Agent({
  name: "AI Legislation Research Agent",
  instructions: `Search the latest changes in legislation affecting artificial intelligence (AI) and chatbots across the United States in the past month, then draft a concise, C-suite-friendly regulatory newsletter in this exact format:

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

Formatting rules Parse the output in to JSON with the JSON Structure below
– Use Markdown headings, bullets, and dividers exactly as shown.
– Keep the tone executive-brief level (factual, direct, but engaging).
– Include live URLs for each cited source.
– Do not include commentary or speculation.
– The total output should fit comfortably on one page when rendered in Notion or email.`,
  model: "gpt-5",
  tools: [webSearchPreview],
  outputType: ResearchAgentSchema,
  modelSettings: {
    reasoning: {
      effort: "low",
      summary: "auto"
    },
    store: true
  }
});

/**
 * Run the research agent workflow
 * @param {Object} params - Workflow parameters
 * @param {string} params.input_as_text - The input text/query for the agent
 * @param {string} [params.workflowId] - Optional workflow ID for tracing
 * @returns {Promise<Object>} - Agent result with output_text and output_parsed
 */
export const runResearchAgentWorkflow = async ({ input_as_text, workflowId }) => {
  return await withTrace("AI Legislation Agent", async () => {
    const conversationHistory = [
      {
        role: "user",
        content: [
          {
            type: "input_text",
            text: input_as_text
          }
        ]
      }
    ];

    const runner = new Runner({
      traceMetadata: {
        __trace_source__: "agent-builder",
        workflow_id: workflowId || "wf_68fb4285b7848190a7d1feb126fe069e056baab3ea0bf879"
      }
    });

    const agentResultTemp = await runner.run(researchAgent, conversationHistory);
    
    conversationHistory.push(...agentResultTemp.newItems.map((item) => item.rawItem));

    if (!agentResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    return {
      output_text: JSON.stringify(agentResultTemp.finalOutput),
      output_parsed: agentResultTemp.finalOutput,
      conversationHistory: conversationHistory
    };
  });
};

export { researchAgent, ResearchAgentSchema };

