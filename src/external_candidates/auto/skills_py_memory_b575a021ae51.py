# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\krishna3554.py\echo_agent.py\memory_b575a021ae51.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\krishna3554\echo-agent\memory.py

class SimpleMemory:
    def __init__(self):
        self.history = []

    def store(self, item):
        self.history.append(item)

    def recall(self):
        return self.history[-3:]
