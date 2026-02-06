# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\tools\firecrawl_tools.py
from agno.agent import Agent
from agno.tools.firecrawl import FirecrawlTools

agent = Agent(
    tools=[FirecrawlTools(scrape=False, crawl=True)],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Summarize this https://finance.yahoo.com/")
