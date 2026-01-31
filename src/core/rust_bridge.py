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
from typing import Dict, List, Any, Optional, Callable

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
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error("RustBridge: calculate_metrics failed: %s", e)
            return {}

    @staticmethod
    def calculate_shard_id(key: str, shard_count: int) -> int:
        """Audited sharding logic (MD5-based)."""
        if shard_count <= 0:
            logger.warning("RustBridge: shard_count must be positive, defaulting to 1024")
            shard_count = 1024
        return RustBridge._calculate_shard_id_fallback(key, shard_count) if not RustBridge._can_use_rust('calculate_interaction_shard_md5') else RustBridge._try_rust_call('calculate_interaction_shard_md5', key, shard_count, fallback=lambda: RustBridge._calculate_shard_id_fallback(key, shard_count))

    @staticmethod
    def _calculate_shard_id_fallback(key: str, shard_count: int) -> int:
        import hashlib
        h = hashlib.md5(key.encode()).digest()
        seed = int.from_bytes(h[:8], "big")
        return seed % shard_count

    @staticmethod
    def _can_use_rust(attr: str) -> bool:
        return RUST_AVAILABLE and hasattr(rc, attr)

    @staticmethod
    def _try_rust_call(attr: str, *args: Any, fallback: Optional[Callable[[], Any]] = None, **kwargs: Any) -> Any:
        try:
            return getattr(rc, attr)(*args, **kwargs)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"RustBridge: {attr} failed: {e}")
            if fallback:
                return fallback()
            return None

    @staticmethod
    def bulk_replace(content: str, replacements: Dict[str, str]) -> str:
        """Audited parallel text replacement."""
        if not replacements:
            return content
        return RustBridge._bulk_replace_fallback(content, replacements) if not RustBridge._can_use_rust('bulk_replace_rust') else RustBridge._try_rust_call('bulk_replace_rust', content, replacements, fallback=lambda: RustBridge._bulk_replace_fallback(content, replacements))

    @staticmethod
    def _bulk_replace_fallback(content: str, replacements: Dict[str, str]) -> str:
        result = content
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result

    @staticmethod
    def bulk_replace_files(file_paths: List[str], replacements: Dict[str, str]) -> Dict[str, bool]:
        """Audited parallel file modification."""
        if not file_paths or not replacements:
            return {p: False for p in file_paths} if file_paths else {}
        return RustBridge._bulk_replace_files_fallback(file_paths, replacements) if not RustBridge._can_use_rust('bulk_replace_files_rust') else RustBridge._try_rust_call('bulk_replace_files_rust', file_paths, replacements, fallback=lambda: RustBridge._bulk_replace_files_fallback(file_paths, replacements))

    @staticmethod
    def _bulk_replace_files_fallback(file_paths: List[str], replacements: Dict[str, str]) -> Dict[str, bool]:
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
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                results[path] = False
        return results

    @staticmethod
    def chunk_boundaries_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited chunk boundary calculation."""
        return RustBridge._try_rust_call("chunk_boundaries_rust", *args, **kwargs)

    @staticmethod
    def stream_sync_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited stream synchronization."""
        return RustBridge._try_rust_call("stream_sync_rust", *args, **kwargs)

    @staticmethod
    def uva_copy_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited UVA data copy."""
        return RustBridge._try_rust_call("uva_copy_rust", *args, **kwargs)

    @staticmethod
    def batch_write_indices_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited batch index generation."""
        return RustBridge._try_rust_call("batch_write_indices_rust", *args, **kwargs)

    @staticmethod
    def event_query_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited event query logic."""
        return RustBridge._try_rust_call("event_query_rust", *args, **kwargs)

    @staticmethod
    def image_resize_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited image resizing."""
        return RustBridge._try_rust_call("image_resize_rust", *args, **kwargs)

    @staticmethod
    def normalize_pixels_rust(*args: Any, **kwargs: Any) -> Any:
        """Audited pixel normalization."""
        return RustBridge._try_rust_call("normalize_pixels_rust", *args, **kwargs)

    @staticmethod
    def is_rust_active() -> bool:
        """Check if the Rust acceleration layer is active."""
        return RUST_AVAILABLE
