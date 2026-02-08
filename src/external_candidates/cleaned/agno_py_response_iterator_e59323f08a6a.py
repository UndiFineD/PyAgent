# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\response_iterator_e59323f08a6a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\response_iterator.py

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

