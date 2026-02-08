# Refactored by Copilot placeholder
# Refactored by Copilot placeholder
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
