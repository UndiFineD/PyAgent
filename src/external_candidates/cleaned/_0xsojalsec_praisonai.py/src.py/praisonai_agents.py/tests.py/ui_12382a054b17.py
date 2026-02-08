# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\ui.py
import gradio as gr
from praisonaiagents import MCP, Agent


def search_airbnb(query):
    agent = Agent(
        instructions="You help book apartments on Airbnb.",
        llm="gpt-5-nano",
        tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"),
    )
    result = agent.start(query)
    return f"## Airbnb Search Results\n\n{result}"


demo = gr.Interface(
    fn=search_airbnb,
    inputs=gr.Textbox(placeholder="I want to book an apartment in Paris for 2 nights..."),
    outputs=gr.Markdown(),
    title="Airbnb Booking Assistant",
    description="Enter your booking requirements below:",
)

if __name__ == "__main__":
    demo.launch()
