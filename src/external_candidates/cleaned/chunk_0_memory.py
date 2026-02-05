# Extracted from: C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_memory.py
# Extracted from: C:\DEV\PyAgent\.external\skills\skills\krishna3554\echo-agent\memory.py
# NOTE: extracted with static-only rules; review before use

class SimpleMemory:

    def __init__(self):

        self.history = []



    def store(self, item):

        self.history.append(item)



    def recall(self):

        return self.history[-3:]

