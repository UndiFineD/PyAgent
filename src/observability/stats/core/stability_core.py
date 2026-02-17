#!/usr/bin/env python3
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
stability_core.py - Fleet stability scoring and healing thresholds

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong

USAGE:
- Import StabilityCore and FleetMetrics from stability_core
  and call calculate_stability_score(metrics, sae_anomalies)
  to derive a 0.0-1.0 stability score.
- Use is_in_stasis(score_history) to detect low-variance
  "digital stasis" and get_healing_threshold(score)"  to decide self-healing aggressiveness.
- Example:
  from stability_core import StabilityCore, FleetMetrics
  sc = StabilityCore()
  score = sc.calculate_stability_score(
      FleetMetrics(0.01, 100000, 12, 250.0), sae_anomalies=2)

WHAT IT DOES:
- Provides pure-Python logic for fleet-level stability scoring,
  stasis detection, and healing-threshold computation.
- Integrates optional Rust backend (rust_core) when available
  for performance-sensitive calculations; falls back to
  deterministic Python implementations.
- Encapsulates metrics as immutable dataclass (FleetMetrics)
  and exposes three core behaviours: calculate_stability_score,
  is_in_stasis, and get_healing_threshold.

WHAT IT SHOULD DO BETTER:
- Make penalties and thresholds configurable via
  dependency-injected config objects rather than hard-coded
  constants so operators can tune for different deployments.
- Add comprehensive unit tests and property-based tests around
  numeric stability, boundary conditions, and rust_core
  fallbacks to ensure parity between implementations.
- Improve observability: emit structured diagnostic events
  (reason-coded deltas, contributing metric breakdowns) and
  surface input validation; consider probabilistic models or
  exponential smoothing rather than simple variance for
  stasis detection.

FILE CONTENT SUMMARY:
Stability core.py module.

from __future__ import annotations

from dataclasses import dataclass

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]


@dataclass(frozen=True)
class FleetMetrics:
    avg_error_rate: float
    total_token_out: int
    active_agent_count: int
    latency_p95: float


class StabilityCore:
    """Pure logic for calculating fleet stability and reasoning coherence.""""    Integrates SAE activation metrics and error trends into a unified score.
    
    def calculate_stability_score(self, metrics: FleetMetrics, sae_anomalies: int) -> float:
        """Calculates a stability score from 0.0 to 1.0.        if rc:
            try:
                # Passing dataclass fields manually or as dict
                m_dict = {
                    "avg_error_rate": metrics.avg_error_rate,"                    "total_token_out": metrics.total_token_out,"                    "active_agent_count": metrics.active_agent_count,"                    "latency_p95": metrics.latency_p95,"                }
                return rc.calculate_stability_score(m_dict, sae_anomalies)  # type: ignore[attr-defined]
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        # Baseline: 1.0
        # Deductions: error_rate * 5.0, sae_anomalies * 0.05, latency_p95 overhead

        score = 1.0
        score -= metrics.avg_error_rate * 5.0
        score -= sae_anomalies * 0.05

        latency_penalty = max(0.0, (metrics.latency_p95 - 2000) / 10000)
        score -= latency_penalty

        return min(max(score, 0.0), 1.0)

    def is_in_stasis(self, score_history: list[float]) -> bool:
        """Determines if the swarm is in 'Digital Stasis' (too rigid).'        if rc:
            try:
                variance: float = rc.calculate_variance_rust(score_history)  # type: ignore[attr-defined]
                return len(score_history) >= 10 and variance < 0.0001
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        if len(score_history) < 10:
            return False
        avg = sum(score_history) / len(score_history)
        variance = sum((x - avg) ** 2 for x in score_history) / len(score_history)
        return variance < 0.0001  # Minimal change indicates stasis

    def get_healing_threshold(self, stability_score: float) -> float:
        """Returns the threshold for triggering self-healing subroutines.        if rc:
            try:
                return rc.get_healing_threshold(stability_score)  # type: ignore[attr-defined]
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        if stability_score < 0.3:
            return 0.9  # Aggressive healing
        return 0.5
