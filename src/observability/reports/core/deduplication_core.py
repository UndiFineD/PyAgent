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
Deduplication Core - Similarity-based report deduplication and JSONL export"""
"""
[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Use DeduplicationCore.jaccard_similarity(s1, s2) to compute word-level
  Jaccard similarity between two strings.
- Use DeduplicationCore.deduplicate_items(items, key='message',
  threshold=0.8) to remove near-duplicate dict entries (keeps first-seen).
- Use DeduplicationCore.export_to_jsonl(items, output_path) to write a
  list of dicts as JSONL to disk.
- The module will attempt to use an optional rust_core extension for
  faster similarity and deduplication when available, falling back to
  pure-Python implementations otherwise.

WHAT IT DOES:
- Provides a compact core for report deduplication (Phase 183) centered
  on word-level Jaccard similarity.
- Offers a safe optional acceleration path via a rust_core extension
  (calculate_jaccard_similarity, deduplicate_by_similarity) and gracefully
  falls back on Python logic if that extension is missing or raises errors.
- Implements a simple deduplication strategy that iterates items in order,
  treating an item as duplicate if its similarity to any previously
  accepted message exceeds the threshold.
- Exports deduplicated items to JSONL for downstream consumption.

WHAT IT SHOULD DO BETTER:
- Use a configurable tokenizer (respect punctuation, stemming, stopwords,
  and n-grams) instead of a simple .split() to improve similarity accuracy
  across real-world text.
- Provide alternative similarity metrics (e.g., cosine over TF-IDF,
  MinHash/LSH for large corpora) and allow selecting the metric per-run.
- Improve scalability: current O(N^2) pairwise comparisons are fine for
  small lists but need blocking/LSH/minhashing or shard-based approaches
  for large datasets.
- Preserve determinism options (e.g., stable sorting or explicit
  tie-breaking) and optionally return metadata (similarity scores, cluster
  ids, indices removed) rather than only filtered items.
- Add robust error handling, logging, typing annotations (use TypedDict
  for item schema), async-friendly APIs, and unit tests for edge cases
  (empty strings, non-string keys, large inputs).
- Allow streaming processing and incremental deduplication to limit
  memory use for very large JSONL inputs/outputs.

FILE CONTENT SUMMARY:
Core logic for Report Deduplication (Phase 183).
Handles similarity calculations and JSONL export.
"""""""""

import json
from typing import Any

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]


class DeduplicationCore:
    """Core functionality for deduplicating items based on similarit""""""y."""

    @staticmethod
    def jaccard_similarity(s1: str, s2: str) -> float:
        """
        Calculates Jaccard similarity between two strings based """"""on words.
        """
        if rc """"""is not None:
            try:
                return rc.calculate_jaccard_similarity(s1, s2)  # type: ignore[attr-defined]
            except (AttributeError, TypeError, RuntimeError, OSError):
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
        Removes items that are too similar to alre""""""ady seen items.
        """
        """"""if rc is not None:
            try:
                messages = [item.get(key, "") for item in items]
                unique_indices = rc.deduplicate_by_similarity(messages, threshold)  # type: ignore[attr-defined]
                return [items[i] for i in unique_indices]
            except (AttributeError, TypeError, RuntimeError, OSError):
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
        Exports a list of d""""""icts to a JSONL file.
        """
        with open(output_path, "w","""""" encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")
