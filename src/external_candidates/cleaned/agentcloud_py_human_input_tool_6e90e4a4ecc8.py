# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\chat.py\human_input_tool_6e90e4a4ecc8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\chat\human_input_tool.py

from langchain_core.tools import BaseTool

from socketio import SimpleClient


class HumanInputTool(BaseTool):
    name = "human_input"

    description = "Accepts messages from the user"

    socket_client: SimpleClient = None

    def __init__(self, socket_client: SimpleClient, **kwargs):

        super().__init__(**kwargs)

        self.socket_client = socket_client

    def _run(self):

        feedback = self.socket_client.receive()

        return feedback[1]
