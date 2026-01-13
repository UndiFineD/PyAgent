
"""
Core logic for Report Deduplication (Phase 183).
Handles similarity calculations and JSONL export.
"""

import json
from typing import List, Dict, Any

class DeduplicationCore:
    @staticmethod
    def jaccard_similarity(s1: str, s2: str) -> float:
        """
        Calculates Jaccard similarity between two strings based on words.
        """
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    @staticmethod
    def deduplicate_items(items: list[dict[str, Any]], key: str = "message", threshold: float = 0.8) -> list[dict[str, Any]]:
        """
        Removes items that are too similar to already seen items.
        """
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
    def export_to_jsonl(items: list[dict[str, Any]], output_path: str):
        """
        Exports a list of dicts to a JSONL file.
        """
        with open(output_path, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")