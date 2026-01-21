"""
Core logic for Report Deduplication (Phase 183).
Handles similarity calculations and JSONL export.
"""

import json
from typing import Any

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]


class DeduplicationCore:
    @staticmethod
    def jaccard_similarity(s1: str, s2: str) -> float:
        """
        Calculates Jaccard similarity between two strings based on words.
        """
        if rc:
            try:
                return rc.calculate_jaccard_similarity(s1, s2)  # type: ignore[attr-defined]
            except Exception:
                pass

        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    @staticmethod
    def deduplicate_items(
        items: list[dict[str, Any]], key: str = "message", threshold: float = 0.8
    ) -> list[dict[str, Any]]:
        """
        Removes items that are too similar to already seen items.
        """
        if rc:
            try:
                messages = [item.get(key, "") for item in items]
                unique_indices = rc.deduplicate_by_similarity(messages, threshold)  # type: ignore[attr-defined]
                return [items[i] for i in unique_indices]
            except Exception:
                pass

        unique_items = []
        seen_messages: list[str] = []

        for item in items:
            msg = item.get(key, "")
            is_duplicate = False
            for seen in seen_messages:
                if DeduplicationCore.jaccard_similarity(msg, seen) > threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_items.append(item)
                seen_messages.append(msg)

        return unique_items

    @staticmethod
    def export_to_jsonl(items: list[dict[str, Any]], output_path: str) -> None:
        """
        Exports a list of dicts to a JSONL file.
        """
        with open(output_path, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")
