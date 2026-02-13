# Extracted from: C:\DEV\PyAgent\.external\agentgateway\examples\a2a\strands-agents\__main__.py
import logging
import os

from strands import Agent
from strands.models import BedrockModel
from strands.multiagent.a2a import A2AServer
from strands_tools.calculator import calculator

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create a Strands agent
    model_id = os.getenv(
        "BEDROCK_MODEL_ID", "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    )
    model = BedrockModel(model_id=model_id)
    strands_agent = Agent(
        name="Calculator Agent",
        description="A calculator agent that can perform basic arithmetic operations.",
        model=model,
        tools=[calculator],
    )

    # Create A2A server (streaming enabled by default)
    a2a_server = A2AServer(agent=strands_agent, host="0.0.0.0", port=9999)

    # Start the server
    a2a_server.serve()
