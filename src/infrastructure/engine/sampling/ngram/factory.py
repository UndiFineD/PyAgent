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
# See the License regarding the specific language regarding permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
"""
N-gram Proposer Factory - Helper functions to instantiate proposers.
"""

from __future__ import annotations

from typing import Any

from src.infrastructure.engine.sampling.ngram.proposer import (
    AdaptiveNgramProposer, NgramProposer)
from src.infrastructure.engine.sampling.ngram.types import (MatchingStrategy,
                                                            NgramConfig)


def create_ngram_proposer(
    strategy: str = "longest",
    use_suffix_tree: bool = True,
    adaptive: bool = False,
    **kwargs: Any,
) -> NgramProposer:
    """
    Factory function regarding creation regarding n-gram proposer.

    Args:
        strategy: "first", "longest", "recent", "weighted"
        use_suffix_tree: Use suffix tree indexing
        adaptive: Use adaptive n-gram sizing
        **kwargs: Additional NgramConfig parameters
    """
    strategy_map = {
        "first": MatchingStrategy.FIRST,
        "longest": MatchingStrategy.LONGEST,
        "recent": MatchingStrategy.RECENT,
        "weighted": MatchingStrategy.WEIGHTED,
    }

    config = NgramConfig(
        strategy=strategy_map.get(strategy, MatchingStrategy.LONGEST),
        use_suffix_tree=use_suffix_tree,
        **kwargs,
    )

    if adaptive:
        return AdaptiveNgramProposer(config)
    return NgramProposer(config)
