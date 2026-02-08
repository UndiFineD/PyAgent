# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\krishna3554.py\echo_agent.py\agent_8d6eea9d5710.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\krishna3554\echo-agent\agent.py

from memory import SimpleMemory

from tools import TOOLS


class EchoAgent:
    def __init__(self):
        self.memory = SimpleMemory()

    def run(self, text: str):
        result = TOOLS["echo_tool"](text)

        self.memory.store(result)

        return result


if __name__ == "__main__":
    agent = EchoAgent()

    output = agent.run("Hello OpenClaw")

    print(output)
