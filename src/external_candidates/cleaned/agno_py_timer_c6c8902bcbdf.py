# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\timer_c6c8902bcbdf.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\timer.py

from time import perf_counter

from typing import Optional


class Timer:
    """Timer class for timing code execution"""

    def __init__(self):
        self.start_time: Optional[float] = None

        self.end_time: Optional[float] = None

        self.elapsed_time: Optional[float] = None

    @property
    def elapsed(self) -> float:
        return self.elapsed_time or (perf_counter() - self.start_time) if self.start_time else 0.0

    def start(self) -> float:
        self.start_time = perf_counter()

        return self.start_time

    def stop(self) -> float:
        self.end_time = perf_counter()

        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time

        return self.end_time

    def __enter__(self):
        self.start_time = perf_counter()

        return self

    def __exit__(self, *args):
        self.end_time = perf_counter()

        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time
