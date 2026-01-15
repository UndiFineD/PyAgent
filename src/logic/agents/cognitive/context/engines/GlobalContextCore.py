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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Any
from datetime import datetime

__version__ = VERSION




class GlobalContextCore:
    """
    Pure logic for GlobalContext.
    Handles data merging, pruning, and summary formatting.
    No I/O or direct disk access.
    """

    def partition_memory(self, memory: dict[str, Any], max_entries_per_shard: int = 1000) -> dict[str, dict[str, Any]]:
        """
        Splits memory into shards if it exceeds thresholds.
        Implements stable sub-sharding for trillion-parameter scalability (Phase 104).
        Refined in Phase 119 for adaptive rebalancing.
        """
        import zlib
        shards: dict[str, dict[str, Any]] = {"default": {}}
        for category, data in memory.items():
            if not isinstance(data, dict) or not data:
                shards["default"][category] = data
                continue

            count = len(data)
            if count > max_entries_per_shard:
                # Logic for Sub-sharding (Stable Hash-based)
                # Phase 119: Adaptive rebalancing - we adjust shard count based on density
                num_sub_shards = 2**((count // max_entries_per_shard).bit_length())

                for key, val in data.items():
                    # Adler-32 is fast and sufficient for non-cryptographic sharding
                    hash_input = f"{category}:{key}"
                    bucket = zlib.adler32(hash_input.encode()) % num_sub_shards
                    shard_name = f"{category}_{bucket}"
                    if shard_name not in shards:
                        shards[shard_name] = {}
                    shards[shard_name][key] = val
            else:
                shards["default"][category] = data
        return shards

    def detect_shard_bloat(self, shards: dict[str, dict[str, Any]], size_threshold_bytes: int = 5_000_000) -> list[str]:
        """
        Identifies shards that are exceeding the recommended size for zero-latency retrieval.
        Phase 119: Adaptive Shard Rebalancing logic.
        """
        import json
        bloated = []
        for name, data in shards.items():
            # Estimate size via JSON serialization
            size = len(json.dumps(data))
            if size > size_threshold_bytes:
                bloated.append(name)
        return bloated

    def prepare_fact(self, key: str, value: Any) -> dict[str, Any]:
        """Prepares a fact entry with timestamp."""
        return {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }

    def prepare_insight(self, insight: str, source_agent: str) -> dict[str, Any]:
        """Prepares an insight entry."""
        return {
            "text": insight,
            "source": source_agent,
            "timestamp": datetime.now().isoformat()
        }

    def merge_entity_info(self, existing: dict[str, Any], new_attributes: dict[str, Any]) -> dict[str, Any]:
        """Merges new attributes into an entity record."""
        updated = existing.copy()
        updated.update(new_attributes)
        updated["last_modified"] = datetime.now().isoformat()
        return updated

    def resolve_conflict(self, existing: Any, incoming: Any, strategy: str = "latest") -> Any:
        """
        Logic to resolve conflicts when multiple agents update the same key.
        - 'latest': Uses timestamp if available, else incoming.
        - 'merge': Merges dicts/lists.
        - 'accumulate': For numeric types.
        """
        if strategy == "latest":
            if isinstance(existing, dict) and isinstance(incoming, dict):
                e_ts = existing.get("updated_at", "")
                i_ts = incoming.get("updated_at", "")
                return incoming if i_ts >= e_ts else existing
            return incoming

        if strategy == "merge":
            if isinstance(existing, dict) and isinstance(incoming, dict):
                merged = existing.copy()
                merged.update(incoming)
                return merged
            if isinstance(existing, list) and isinstance(incoming, list):
                return list(set(existing + incoming))
            return incoming

        if strategy == "accumulate":
            if isinstance(existing, (int, float)) and isinstance(incoming, (int, float)):
                return existing + incoming
            return incoming

        return incoming

    def prune_lessons(self, lessons: list[dict[str, Any]], max_lessons: int = 20) -> list[dict[str, Any]]:
        """Prunes lessons to keep only the most recent."""
        return lessons[-max_lessons:]

    def generate_markdown_summary(self, memory: dict[str, Any]) -> str:
        """Logic for formatting the cognitive summary."""
        summary = ["# 🧠 Long-Term Memory Summary"]

        if memory.get("facts"):
            summary.append("\n## 📋 Project Facts")
            for k, v in memory["facts"].items():
                summary.append(f"- **{k}**: {v['value']}")

        if memory.get("constraints"):
            summary.append("\n## ⚠️ Constraints")
            for c in memory["constraints"]:
                summary.append(f"- {c}")

        if memory.get("insights"):
            summary.append("\n## 💡 Key Insights")
            for i in memory["insights"][-5:]:  # Show last 5
                summary.append(f"- {i['text']} (via {i['source']})")

        if memory.get("lessons_learned"):
            summary.append("\n## 🎓 Lessons Learned")
            for lesson in memory["lessons_learned"][-3:]:
                summary.append(f"- **Issue**: {lesson['failure']} | **Fix**: {lesson['correction']}")

        return "\n".join(summary)
