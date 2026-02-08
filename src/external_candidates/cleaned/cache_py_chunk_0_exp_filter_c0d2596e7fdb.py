# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_exp_filter_c0d2596e7fdb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_exp_filter.py

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\utils\exp_filter.py

# NOTE: extracted with static-only rules; review before use


class ExpFilter:
    def __init__(self, alpha: float, max_val: float = -1.0) -> None:
        self._alpha = alpha

        self._filtered = -1.0

        self._max_val = max_val

    def reset(self, alpha: float = -1.0) -> None:
        if alpha != -1.0:
            self._alpha = alpha

        self._filtered = -1.0

    def apply(self, exp: float, sample: float) -> float:
        if self._filtered == -1.0:
            self._filtered = sample

        else:
            a = self._alpha**exp

            self._filtered = a * self._filtered + (1 - a) * sample

        if self._max_val != -1.0 and self._filtered > self._max_val:
            self._filtered = self._max_val

        return self._filtered

    def filtered(self) -> float:
        return self._filtered

    def update_base(self, alpha: float) -> None:
        self._alpha = alpha
