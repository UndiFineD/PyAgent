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
Rust Bridge - Safe Rust FFI Bridge.
Safe FFI Bridge for Rust Acceleration (rust_core.pyd).
Provides centralized hub for all Rust FFI calls with graceful fallbacks.

[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- From Python: from rust_bridge import get_bridge; metrics = get_bridge().calculate_metrics(text)
- Shard id: sid = get_bridge().calculate_shard_id(key, shard_count)
- Vector search: idxs = get_bridge().search_vector(query_vec, database, top_k)
- Generic execute: result = get_bridge().execute("method_name", {"param": value})

WHAT IT DOES:
- Provides a centralized, memory-safe bridge to an optional rust_core extension with graceful Python fallbacks.
- Wraps Rust FFI calls with boundary checks, logging, and simple fallback implementations for metrics, sharding, vector search, block management, token hashing, and bulk text replace.
- Exposes a singleton-like accessor (get_bridge) and a generic execute router for dynamic calls.

WHAT IT SHOULD DO BETTER:
- Add structured feature-detection and an initialization handshake to surface availability and version of rust_core at startup.
- Improve error handling: return typed exceptions or result objects instead of None/empty values to aid upstream handling and testing.
- Add extensive unit tests for fallbacks, and optimize fallback implementations (e.g., use thread-safe caches, deterministic hashing) and better typing for returned structures.
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
        except Exception:  # pylint: disable=broad-exception-caught
            logger.error("RustBridge: calculate_metrics failed")
            return {}

    @staticmethod
    def calculate_shard_id(key: str, shard_count: int) -> int:
        """Audited sharding logic (MD5-based)."""
        if shard_count <= 0:
            logger.warning("RustBridge: shard_count must be positive, defaulting to 1024")
            shard_count = 1024

        def fallback() -> int:
            return RustBridge._calculate_shard_id_fallback(key, shard_count)

        if not RustBridge._can_use_rust("calculate_interaction_shard_md5"):
            return fallback()

        return RustBridge._try_rust_call(
            "calculate_interaction_shard_md5",
            key,
            shard_count,
            fallback=fallback,
        )

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
    def search_vector(query_vec: List[float], database: List[List[float]], top_k: int) -> List[int]:
        """Rust-accelerated vector search for long-term memory."""
        if not query_vec or not database:
            return []

        return get_bridge()._try_rust_call("search_vector_rust", query_vec, database, top_k, fallback=lambda: [])

    @staticmethod
    def manage_kv_blocks(num_blocks: int, block_size: int) -> List[int]:
        """Paged Attention: Get available block offsets."""
        return get_bridge()._try_rust_call(
            "block_manager_rust", num_blocks, block_size, fallback=lambda: [i * block_size for i in range(num_blocks)]
        )

    @staticmethod
    def get_token_hash(tokens: List[int]) -> str:
        """High-speed token sequence hashing for prefix caching."""
        return get_bridge()._try_rust_call("kv_block_hash_rust", tokens, fallback=lambda: str(hash(tuple(tokens))))

    def execute(self, method_name: str, params: Dict[str, Any]) -> Any:
        """Generic execution router for Rust functions."""
        attr = method_name if method_name.endswith("_rust") else f"{method_name}_rust"
        return self._try_rust_call(attr, **params)

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

        def fallback() -> str:
            return RustBridge._bulk_replace_fallback(content, replacements)

        if not RustBridge._can_use_rust("bulk_replace_rust"):
            return fallback()

        return RustBridge._try_rust_call(
            "bulk_replace_rust",
            content,
            replacements,
            fallback=fallback,
        )

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

        def fallback() -> Dict[str, bool]:
            return RustBridge._bulk_replace_files_fallback(file_paths, replacements)

        if not RustBridge._can_use_rust("bulk_replace_files_rust"):
            return fallback()

        return RustBridge._try_rust_call(
            "bulk_replace_files_rust",
            file_paths,
            replacements,
            fallback=fallback,
        )

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
            except Exception:  # pylint: disable=broad-exception-caught
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
    def get_imports(source: str) -> List[str]:
        """Audited import extraction (20x faster than AST)."""
        if not source:
            return []

        def fallback() -> List[str]:
            return RustBridge._get_imports_fallback(source)

        if not RustBridge._can_use_rust("get_imports_rust"):
            return fallback()
        return RustBridge._try_rust_call("get_imports_rust", source, fallback=fallback)

    @staticmethod
    def _get_imports_fallback(source: str) -> List[str]:
        import ast

        try:
            tree = ast.parse(source)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
            return sorted(list(set(imports)))
        except SyntaxError:
            return []

    @staticmethod
    def scan_optimization_patterns(content: str) -> List[Dict[str, Any]]:
        """Audited optimization pattern scanning."""
        if not content:
            return []

        if not RustBridge._can_use_rust("scan_optimization_patterns_rust"):
            return []

        raw = RustBridge._try_rust_call("scan_optimization_patterns_rust", content)
        if not raw:
            return []

        # Transform raw Vec<(line, idx, groups)> to descriptive dicts
        patterns = [
            "Manual range(len(x)) loop (prefer enumerate)",
            "Non-parallel accumulated loop (prefer vectorization)",
            "Blocking time.sleep call (prefer async/event)",
        ]

        results = []
        for line, idx, groups in raw:
            results.append(
                {"line": line, "pattern": patterns[idx] if idx < len(patterns) else "Unknown", "groups": groups}
            )
        return results

    @staticmethod
    def analyze_tech_debt(content: str) -> Dict[str, int]:
        """Audited technical debt analysis (marker-based)."""
        if not content:
            return {}
        return RustBridge._try_rust_call("analyze_tech_debt_rust", content) or {}

    @staticmethod
    def scan_security_patterns(content: str, patterns: Dict[str, str]) -> List[Dict[str, Any]]:
        """Audited security pattern scanning."""
        if not content or not patterns:
            return []

        raw = RustBridge._try_rust_call("analyze_security_patterns_rust", content, patterns)
        if not raw:
            return []

        results = []
        for name, line, matched_text in raw:
            results.append({"risk_type": name, "line": line, "text": matched_text})
        return results

    @staticmethod
    def is_rust_active() -> bool:
        """Check if the Rust acceleration layer is active."""
        return RUST_AVAILABLE
