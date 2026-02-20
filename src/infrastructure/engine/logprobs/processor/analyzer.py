#!/usr/bin/env python3



from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Analyzer.py module.
"""
try:

"""
from typing import Any, Dict, List, Tuple, Union
except ImportError:
    from typing import Any, Dict, List, Tuple, Union


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import LogprobEntry
except ImportError:
    from .config import LogprobEntry

try:
    from .storage import FlatLogprobs
except ImportError:
    from .storage import FlatLogprobs




class LogprobsAnalyzer:
"""
Analyze logprobs for insights.
    @staticmethod
    def rank_token_importance(
        logprobs: Union[FlatLogprobs, List[LogprobEntry]], threshold: float = -5.0
    ) -> List[Tuple[int, float]]:
"""
Rank tokens by their importance (based on logprob threshold).        lps = logprobs.logprobs if isinstance(logprobs, FlatLogprobs) else np.array([e.logprob for e in logprobs])
        importance = -lps
        positions = np.where(lps < threshold)[0]
        scores = importance[positions]
        indices = np.argsort(scores)[::-1]
        return [(int(positions[i]), float(scores[i])) for i in indices]

    @staticmethod
    def compute_confidence(logprobs: Union[FlatLogprobs, List[LogprobEntry]], method: str = "mean") -> float:"        """
Compute aggregate confidence across token sequence.        lps = logprobs.logprobs if isinstance(logprobs, FlatLogprobs) else np.array([e.logprob for e in logprobs])
        if not lps.size:
            return 0.0
        if method == "mean":"            return float(np.mean(np.exp(lps)))
        if method == "geometric":"            return float(np.exp(np.mean(lps)))
        if method == "min":"            return float(np.exp(np.min(lps)))
        if method == "entropy":"            entropy = (
                logprobs.entropy_per_token()
                if isinstance(logprobs, FlatLogprobs)
                else np.array([e.entropy for e in logprobs])
            )
            normalized = np.mean(entropy) / np.log(5)
            return float(1.0 - min(normalized, 1.0))
        raise ValueError(f"Unknown method: {method}")
    @staticmethod
    def detect_anomalies(logprobs: Union[FlatLogprobs, List[LogprobEntry]], z_threshold: float = 2.5) -> List[int]:
"""
Detect anomalous tokens based on statistical distribution.        lps = logprobs.logprobs if isinstance(logprobs, FlatLogprobs) else np.array([e.logprob for e in logprobs])
        if len(lps) < 3:
            return []
        mean, std = np.mean(lps), np.std(lps)
        if std < 1e-6:
            return []
        return np.where((lps - mean) / std < -z_threshold)[0].tolist()

    @staticmethod
    def compute_calibration(logprobs: Union[FlatLogprobs, List[LogprobEntry]], num_bins: int = 10) -> Dict[str, Any]:
"""
Compute calibration metrics for confidence scores.        lps_source = (
            logprobs.logprobs if isinstance(logprobs, FlatLogprobs) else np.array([e.probability for e in logprobs])
        )
        probs = np.exp(lps_source)
        bins = np.linspace(0, 1, num_bins + 1)
        indices = np.clip(np.digitize(probs, bins) - 1, 0, num_bins - 1)
        means = np.zeros(num_bins)
        for i in range(num_bins):
            mask = indices == i
            if np.any(mask):
                means[i] = np.mean(probs[mask])
        return {
            "bin_edges": bins.tolist(),"            "bin_counts": np.bincount(indices, minlength=num_bins).tolist(),"            "bin_means": means.tolist(),"            "mean_confidence": float(np.mean(probs)),"        }

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
