# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_agents.py\livekit.py\agents.py\utils.py\moving_average_23b70d528794.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\utils\moving_average.py

from __future__ import annotations


class MovingAverage:
    def __init__(self, window_size: int) -> None:
        self._hist: list[float] = [0] * window_size

        self._sum: float = 0

        self._count: int = 0

    def add_sample(self, sample: float) -> None:
        self._count += 1

        index = self._count % len(self._hist)

        if self._count > len(self._hist):
            self._sum -= self._hist[index]

        self._sum += sample

        self._hist[index] = sample

    def get_avg(self) -> float:
        if self._count == 0:
            return 0

        return self._sum / self.size()

    def reset(self) -> None:
        self._count = 0

        self._sum = 0

    def size(self) -> int:
        return min(self._count, len(self._hist))
