# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_response_iterator_16d3ebdfb0e4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_response_iterator.py

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\response_iterator.py

# NOTE: extracted with static-only rules; review before use


class ResponseIterator:
    def __init__(self):
        self.items = []

        self.index = 0

    def add(self, item):
        self.items.append(item)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration

        item = self.items[self.index]

        self.index += 1

        return item
