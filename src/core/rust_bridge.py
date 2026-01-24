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
Safe FFI Bridge for Rust Acceleration (rust_core.pyd).
Provides centralized hub for all Rust FFI calls with graceful fallbacks.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any

try:
    import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False

logger = logging.getLogger(__name__)


def get_bridge() -> RustBridge:
    """Singleton-like accessor for the Rust bridge."""
    return RustBridge()


class RustBridge:
    """
    Centralized hub for all Rust FFI calls.
    Provides memory-safe wrappers, boundary checks, and graceful fallbacks.
    """

    @staticmethod
    def calculate_metrics(content: str) -> Dict[str, float]:
        """Audited metrics calculation."""
        if not content or not isinstance(content, str):
            return {}

        if not RUST_AVAILABLE or not hasattr(rc, "calculate_metrics_rust"):
            return {}
        try:
            return rc.calculate_metrics_rust(content)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("RustBridge: calculate_metrics failed: %s", e)
            return {}

    @staticmethod
    def calculate_shard_id(key: str, shard_count: int) -> int:
        """Audited sharding logic (MD5-based)."""
        if shard_count <= 0:
            logger.warning("RustBridge: shard_count must be positive, defaulting to 1024")
            shard_count = 1024

        if not RUST_AVAILABLE or not hasattr(rc, "calculate_interaction_shard_md5"):
            # Minimal fallback implementation if Rust is missing
            import hashlib
            h = hashlib.md5(key.encode()).digest()
            seed = int.from_bytes(h[:8], "big")
            return seed % shard_count
        try:
            return rc.calculate_interaction_shard_md5(key, shard_count)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"RustBridge: calculate_shard_id failed: {e}")
            import hashlib
            h = hashlib.md5(key.encode()).digest()
            seed = int.from_bytes(h[:8], "big")
            return seed % shard_count

    @staticmethod
    def bulk_replace(content: str, replacements: Dict[str, str]) -> str:
        """Audited parallel text replacement."""
        if not replacements:
            return content

        if not RUST_AVAILABLE or not hasattr(rc, "bulk_replace_rust"):
            # Fallback
            result = content
            for old, new in replacements.items():
                result = result.replace(old, new)
            return result
        try:
            return rc.bulk_replace_rust(content, replacements)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"RustBridge: bulk_replace failed: {e}")
            return content

    @staticmethod
    def bulk_replace_files(file_paths: List[str], replacements: Dict[str, str]) -> Dict[str, bool]:
        """Audited parallel file modification."""
        if not file_paths or not replacements:
            return {p: False for p in file_paths} if file_paths else {}

        if not RUST_AVAILABLE or not hasattr(rc, "bulk_replace_files_rust"):
            results = {}
            for path in file_paths:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                    changed = False
                    for old, new in replacements.items():
                        if old in text:
                            text = text.replace(old, new)
                            changed = True
                    if changed:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(text)
                    results[path] = changed
                except Exception:  # pylint: disable=broad-exception-caught
                    results[path] = False
            return results
        try:
            return rc.bulk_replace_files_rust(file_paths, replacements)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"RustBridge: bulk_replace_files failed: {e}")
            return {p: False for p in file_paths}

    @staticmethod
    def chunk_boundaries_rust(*args, **kwargs) -> Any:
        """Audited chunk boundary calculation."""
        if not RUST_AVAILABLE or not hasattr(rc, "chunk_boundaries_rust"):
            return None
        return rc.chunk_boundaries_rust(*args, **kwargs)  # type: ignore

    @staticmethod
    def stream_sync_rust(*args, **kwargs) -> Any:
        """Audited stream synchronization."""
        if not RUST_AVAILABLE or not hasattr(rc, "stream_sync_rust"):
            return None
        return rc.stream_sync_rust(*args, **kwargs)  # type: ignore

    @staticmethod
    def uva_copy_rust(*args, **kwargs) -> Any:
        """Audited UVA data copy."""
        if not RUST_AVAILABLE or not hasattr(rc, "uva_copy_rust"):
            return None
        return rc.uva_copy_rust(*args, **kwargs)  # type: ignore

    @staticmethod
    def batch_write_indices_rust(*args, **kwargs) -> Any:
        """Audited batch index generation."""
        if not RUST_AVAILABLE or not hasattr(rc, "batch_write_indices_rust"):
            return None
        return rc.batch_write_indices_rust(*args, **kwargs)  # type: ignore

    @staticmethod
    def event_query_rust(*args, **kwargs) -> Any:
        """Audited event query logic."""
        if not RUST_AVAILABLE or not hasattr(rc, "event_query_rust"):
            return None
        return rc.event_query_rust(*args, **kwargs)  # type: ignore

    @staticmethod
    def is_rust_active() -> bool:
        """Check if the Rust acceleration layer is active."""
        return RUST_AVAILABLE
