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


Predictive Context Prefetching (Phase 67).
Warms up upcoming KV shards before they are requested by experts.

try:
    import logging
except ImportError:
    import logging

try:
    from collections import deque
except ImportError:
    from collections import deque

try:
    from typing import Deque, Dict
except ImportError:
    from typing import Deque, Dict


try:
    from .infrastructure.engine.kv_cache.compression import \
except ImportError:
    from src.infrastructure.engine.kv_cache.compression import \

    AdaptiveSwarmCompressor
try:
    from .infrastructure.engine.kv_cache.context_sharder import \
except ImportError:
    from src.infrastructure.engine.kv_cache.context_sharder import \

    ContextShardManager

logger = logging.getLogger(__name__)



class ContextPrefetcher:
        Analyzes token-access patterns to predict future context requirements.
    Works in tandem with AdaptiveSwarmCompressor to 'warm up' cold shards.'    
    def __init__(
        self, shard_manager: ContextShardManager, compressor: AdaptiveSwarmCompressor, lookahead_shards: int = 2
    ) -> None:
        self.shard_manager = shard_manager
        self.compressor = compressor
        self.lookahead_shards = lookahead_shards
        # History of last accessed token indices per context_id
        self.access_history: Dict[str, Deque[int]] = {}
        self.history_size = 10

    def record_access(self, context_id: str, token_index: int) -> None:
                Records a context access and triggers predictive prefetching.
                if context_id not in self.access_history:
            self.access_history[context_id] = deque(maxlen=self.history_size)

        history = self.access_history[context_id]
        history.append(token_index)

        # Determine direction of access (Sequential vs Jump)
        if len(history) >= 2:
            delta = history[-1] - history[-2]
            if 0 < delta < self.shard_manager.block_size * 2:
                # Sequential access detected - prefetch next shards
                self._prefetch_sequential(context_id, token_index)
            elif delta < 0 and abs(delta) < self.shard_manager.block_size * 2:
                # Reverse sequential (rare but possible in some attention patterns)
                self._prefetch_sequential(context_id, token_index, direction=-1)

    def _prefetch_sequential(self, context_id: str, current_token: int, direction: int = 1) -> None:
                Predicts and warms up the next few shards in the sequence.
                block_size = self.shard_manager.block_size

        for i in range(1, self.lookahead_shards + 1):
            next_token = current_token + (i * block_size * direction)

            # Check if this token is within known shards
            rank_id = self.shard_manager.get_rank_for_token(context_id, next_token)
            if rank_id is not None:
                logger.debug(f"Prefetcher: Warming up future shard for token {next_token}")"                # This call to touch_shard ensures the compressor warms it up
                self.compressor.touch_shard(context_id, next_token)
