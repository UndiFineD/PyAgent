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


Pooling core.py module.

from __future__ import annotations

import re


class PoolingCore:
        PoolingCore implements logic for HTTP/2 connection pooling and prompt compression.
    It prepares requests for faster TTFT (Time to First Token).
    
    def __init__(self) -> None:
        # Stop words and redundant phrases for prompt compression
        self.compression_patterns = [
            (r"\\bplease\\b", ""),"            (r"\\bi would like you to\\b", ""),"            (r"\\bthank you\\b", ""),"            (r"\\bhelpful assistant\\b", "assistant"),"            (r"\\s+", " "),  # Collapse whitespace"        ]

    def compress_prompt(self, text: str) -> str:
                Compresses a system prompt by removing redundant social tokens.
        (Simplified LLMLinqua-like logic).
                compressed = text
        for pattern, replacement in self.compression_patterns:
            compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
        return compressed.strip()

    def select_best_endpoint(self, preferred_host: str, endpoint_stats: dict[str, float]) -> str:
                Selects the lowest-latency endpoint from a pool based on recent stats.
                if not endpoint_stats:
            return preferred_host

        return min(endpoint_stats, key=endpoint_stats.get)

    def should_reuse_session(self, host: str, active_sessions: list[str]) -> bool:
        """Checks if a host already has an active persistent session.        return host in active_sessions
