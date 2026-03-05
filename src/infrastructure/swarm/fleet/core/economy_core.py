#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Core logic for Swarm Economy (Phase 179).
Handles bidding and GPU priority allocation logic.
"""

from typing import Any


class EconomyCore:
    """Handles economic logic for swarm resource bidding and priority."""

    @staticmethod
    def calculate_bid_priority(credits: float, importance: float, urgency: float) -> float:
        """
        Calculates a priority score for a bid.
        Priority = (Credits * Importance) / (1.0 + UrgencyLag)
        """
        # importance and urgency are 0.0 to 1.0
        return (credits * importance) * (1.0 + urgency)

    @staticmethod
    def select_winning_bids(bids: list[dict[str, Any]], slots_available: int) -> list[dict[str, Any]]:
        """
        Selects the top N bids based on priority score.
        """
        sorted_bids = sorted(bids, key=lambda x: x.get("priority", 0), reverse=True)
        return sorted_bids[:slots_available]

    @staticmethod
    def calculate_gpu_surcharge(vram_needed_gb: float, current_utilization: float) -> float:
        """
        Calculates a surcharge for high VRAM usage in a congested system.
        """
        base_surcharge = vram_needed_gb * 0.5
        congestion_multiplier = 1.0 + (current_utilization**2)
        return base_surcharge * congestion_multiplier
