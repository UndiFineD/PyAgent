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

"""Parser-safe minimal `KnowledgeCore`.

Provides a conservative, importable fallback of the project's knowledge
management core so dependent modules can import while full logic is
restored incrementally.
"""
from pathlib import Path
from typing import Any, Dict, Optional
import hashlib
import logging

logger = logging.getLogger("pyagent.core")

try:
    from .base_core import BaseCore
except Exception:  # pragma: no cover - fallback
    class BaseCore:  # type: ignore[no-redef]
        def __init__(self, *_, **__):
            self.repo_root = Path.cwd()

try:
    import rust_core as rc  # pylint: disable=no-name-in-module
except Exception:
    rc = None


class KnowledgeCore(BaseCore):
    """Lightweight knowledge sharding helper.

    This minimal implementation exposes `get_shard_id` and `index_entity`
    with deterministic behavior but does not perform persistent storage.
    """

    def __init__(self, shard_count: int = 1024, base_path: Optional[Path] = None) -> None:
        super().__init__()
        self.shard_count = int(shard_count)
        self.base_path = Path(base_path) if base_path else Path(self.repo_root) / "data" / "knowledge"

    def get_shard_id(self, entity_key: str) -> int:
        """Return a shard index for `entity_key`.

        Uses rust-accelerated function when available; otherwise MD5 modulus.
        """
        if rc and hasattr(rc, "get_adler32_shard"):  # pragma: no cover - optional
            try:
                return rc.get_adler32_shard(entity_key, self.shard_count)  # type: ignore[attr-defined]
            except Exception:
                logger.debug("rust shard failed, falling back to md5")
        hash_val = int(hashlib.md5(entity_key.encode()).hexdigest(), 16)
        return hash_val % self.shard_count

    def index_entity(self, entity: Dict[str, Any]) -> bool:
        """Compute shard for entity and return True on success.

        This conservative stub does not persist data; it merely provides a
        stable interface for higher-level components and tests.
        """
        key = entity.get("id") or entity.get("name") or "unknown"
        _ = self.get_shard_id(str(key))
        return True
