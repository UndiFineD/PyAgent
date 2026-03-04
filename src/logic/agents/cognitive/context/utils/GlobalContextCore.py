from typing import Dict, List, Any, Optional
from datetime import datetime

class GlobalContextCore:
    """
    Pure logic for GlobalContext.
    Handles data merging, pruning, and summary formatting.
    No I/O or direct disk access.
    """

    def partition_memory(self, memory: Dict[str, Any], max_entries_per_shard: int = 1000) -> Dict[str, Dict[str, Any]]:
        """
        Splits memory into shards if it exceeds thresholds.
        Implements stable sub-sharding for trillion-parameter scalability (Phase 104).
        """
        import zlib
        shards: Dict[str, Dict[str, Any]] = {"default": {}}
        for category, data in memory.items():
            if isinstance(data, dict):
                if len(data) > max_entries_per_shard:
                    # Logic for Sub-sharding (Stable Hash-based)
                    num_sub_shards = (len(data) // max_entries_per_shard) + 1
                    for key, val in data.items():
                        # Stable hash assignment
                        bucket = zlib.adler32(key.encode()) % num_sub_shards
                        shard_name = f"{category}_{bucket}"
                        if shard_name not in shards: shards[shard_name] = {}
                        shards[shard_name][key] = val
                else:
                    shards["default"][category] = data
            else:
                shards["default"][category] = data
        return shards

    def prepare_fact(self, key: str, value: Any) -> Dict[str, Any]:
        """Prepares a fact entry with timestamp."""
        return {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }

    def prepare_insight(self, insight: str, source_agent: str) -> Dict[str, Any]:
        """Prepares an insight entry."""
        return {
            "text": insight,
            "source": source_agent,
            "timestamp": datetime.now().isoformat()
        }

    def merge_entity_info(self, existing: Dict[str, Any], new_attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Merges new attributes into an entity record."""
        updated = existing.copy()
        updated.update(new_attributes)
        updated["last_modified"] = datetime.now().isoformat()
        return updated

    def prune_lessons(self, lessons: List[Dict[str, Any]], max_lessons: int = 20) -> List[Dict[str, Any]]:
        """Prunes lessons to keep only the most recent."""
        return lessons[-max_lessons:]

    def generate_markdown_summary(self, memory: Dict[str, Any]) -> str:
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
            for i in memory["insights"][-5:]: # Show last 5
                summary.append(f"- {i['text']} (via {i['source']})")
                
        if memory.get("lessons_learned"):
            summary.append("\n## 🎓 Lessons Learned")
            for l in memory["lessons_learned"][-3:]:
                summary.append(f"- **Issue**: {l['failure']} | **Fix**: {l['correction']}")

        return "\n".join(summary)
