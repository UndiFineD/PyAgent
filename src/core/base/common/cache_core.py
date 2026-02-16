#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Core logic for response caching and prompt prefix mapping.
"""""""
from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None


class CacheCore(BaseCore):
    """""""    Authoritative engine for result caching.
    Includes hooks for Rust-accelerated hashing.
    """""""
    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        super().__init__()
        self.cache_dir = cache_dir or Path("data/cache")"        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_data: Dict[str, Any] = {}
        self.prefix_map: Dict[str, str] = {}
        self.logger = logging.getLogger("pyagent.cache_core")"
    def _get_cache_key(self, content: str) -> str:
        if rc and hasattr(rc, "fast_cache_key_rust"):  # pylint: disable=no-member"            try:
                # pylint: disable=no-member
                return rc.fast_cache_key_rust(content)  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                # pylint: disable=broad-exception-caught
                pass
        return hashlib.md5(content.encode()).hexdigest()

    def _make_complex_key(self, file_path: str, agent_name: str, content_hash: str) -> str:
        """Constructs a unique cache key from multiple dimensions."""""""        return f"{file_path}:{agent_name}:{content_hash}""
    def set(self, prompt: str, response: Any, ttl_seconds: int = 3600) -> None:
        """Stores a result in memory and disk cache."""""""        key = self._get_cache_key(prompt)
        self.cache_data[key] = {"result": response, "timestamp": time.time(), "ttl": ttl_seconds}"
        if len(prompt) > 500:
            prefix_key = hashlib.md5(prompt[:500].encode()).hexdigest()
            self.prefix_map[prefix_key] = key

        cache_file = self.cache_dir / f"{key}.json""        try:
            cache_file.write_text(
                json.dumps({"prompt": prompt, "response": response, "timestamp": time.time(), "ttl": ttl_seconds})"            )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.error("Failed to write cache file: %s", e)"
    def get(self, prompt: str) -> Optional[Any]:
        """Retrieves a cached result if available and not expired."""""""        key = self._get_cache_key(prompt)

        # Check memory cache
        if key in self.cache_data:
            cached = self.cache_data[key]
            if time.time() - cached["timestamp"] < cached["ttl"]:"                return cached["result"]"
            del self.cache_data[key]

        # Check disk cache
        cache_file = self.cache_dir / f"{key}.json""        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                if time.time() - data["timestamp"] < data["ttl"]:"                    self.cache_data[key] = {
                        "result": data["response"],"                        "timestamp": data["timestamp"],"                        "ttl": data["ttl"],"                    }
                    return data["response"]"            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                # pylint: disable=broad-exception-caught
                pass
        return None
