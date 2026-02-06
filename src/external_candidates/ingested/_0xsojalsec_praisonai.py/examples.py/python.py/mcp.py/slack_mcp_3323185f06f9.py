# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\slack-mcp.py
import os

from praisonaiagents import MCP, Agent

# Get Slack credentials from environment
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_team_id = os.getenv("SLACK_TEAM_ID")

# Use a single string command with Slack configuration
slack_agent = Agent(
    instructions="""You are a helpful assistant that can interact with Slack.
    Use the available tools when relevant to manage Slack communications.""",
    llm="gpt-5-nano",
    tools=MCP(
        "npx -y @modelcontextprotocol/server-slack",
        env={"SLACK_BOT_TOKEN": slack_token, "SLACK_TEAM_ID": slack_team_id},
    ),
)

slack_agent.start("Send a message to the general channel")
