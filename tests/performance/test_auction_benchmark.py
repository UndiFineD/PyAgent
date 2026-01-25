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
Test Auction Benchmark module.
"""

import timeit
import random
from src.logic.agents.swarm.core.auction_core import AuctionCore


def benchmark_auction():
    core = AuctionCore()

    # Setup data

    bids_small = [
        {"agent_id": f"a{i}", "amount": random.random() * 100} for i in range(10)
    ]
    bids_medium = [
        {"agent_id": f"a{i}", "amount": random.random() * 100} for i in range(100)
    ]
    bids_large = [
        {"agent_id": f"a{i}", "amount": random.random() * 100} for i in range(1000)
    ]

    # Pre-copy to avoid benchmark measuring copy time if possible,
    # but VCG sorts in place or returns new list? Python sort is usually fine.
    # The function sorts `bids` which are dicts in a list. `sorted` returns a new list.

    t_small = timeit.timeit(
        lambda: AuctionCore.calculate_vcg_auction(bids_small, 3), number=10000
    )

    t_medium = timeit.timeit(
        lambda: AuctionCore.calculate_vcg_auction(bids_medium, 10), number=1000
    )
    t_large = timeit.timeit(
        lambda: AuctionCore.calculate_vcg_auction(bids_large, 50), number=100
    )

    print(f"Auction (Small 10): {t_small / 10000 * 1e6:.2f} us")
    print(f"Auction (Medium 100): {t_medium / 1000 * 1e6:.2f} us")

    print(f"Auction (Large 1000): {t_large / 100 * 1e6:.2f} us")

    t_quota = timeit.timeit(
        lambda: AuctionCore.enforce_vram_quota(10.0, 100.0, 0.2), number=100000
    )
    print(f"VRAM Quota Check: {t_quota / 100000 * 1e6:.2f} us")


if __name__ == "__main__":
    benchmark_auction()