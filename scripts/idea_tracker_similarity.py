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

from __future__ import annotations

from typing import Any, Callable


def _jaccard_similarity(left: set[str], right: set[str]) -> float:
    """Return the Jaccard similarity between two token sets.

    Args:
        left: Left token set.
        right: Right token set.

    Returns:
        Jaccard similarity value between 0.0 and 1.0.

    """
    if not left and not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _idea_similarity(left_row: dict[str, Any], right_row: dict[str, Any]) -> dict[str, float]:
    """Compute weighted similarity signals from persisted token rows.

    Args:
        left_row: Left token row.
        right_row: Right token row.

    Returns:
        Weighted score and component similarity values.

    """
    title_sim = _jaccard_similarity(
        set(left_row.get("title_tokens", [])),
        set(right_row.get("title_tokens", [])),
    )
    mapping_sim = _jaccard_similarity(
        set(left_row.get("project_tokens", [])),
        set(right_row.get("project_tokens", [])),
    )
    source_sim = _jaccard_similarity(
        set(left_row.get("source_reference_tokens", [])),
        set(right_row.get("source_reference_tokens", [])),
    )
    score = (0.5 * title_sim) + (0.3 * mapping_sim) + (0.2 * source_sim)
    return {
        "score": round(score, 4),
        "title_similarity": round(title_sim, 4),
        "mapping_similarity": round(mapping_sim, 4),
        "source_similarity": round(source_sim, 4),
    }


def build_similarity_candidates(
    mapping_rows: list[dict[str, Any]],
    token_rows: list[dict[str, Any]],
    merge_threshold: float,
    review_threshold: float,
    scope_idea_ids: set[str] | None = None,
    log: Callable[[str], None] | None = None,
    progress_every: int = 1000,
    similarity_batch_id: str = "",
) -> list[dict[str, Any]]:
    """Build similarity candidates from persisted mapping and token artifacts.

    Args:
        mapping_rows: Persisted mapping rows.
        token_rows: Persisted token rows.
        merge_threshold: Merge-candidate threshold.
        review_threshold: Review-candidate threshold.
        scope_idea_ids: Optional set of idea IDs that triggered this similarity pass.
        log: Optional progress logger.
        progress_every: Preferred heartbeat interval.
        similarity_batch_id: Batch identifier recorded in candidate rows.

    Returns:
        Similarity candidate rows suitable for persistence.

    """
    mapping_index = {row.get("idea_id", ""): row for row in mapping_rows if row.get("idea_id")}
    active_token_rows = [
        row for row in token_rows if mapping_index.get(row.get("idea_id", ""), {}).get("status") == "active"
    ]
    if not active_token_rows:
        return []

    if log is not None:
        log(f"[IdeaTracker] Similarity stage: building blocks from {len(active_token_rows)} active records...")

    block_map: dict[str, list[dict[str, Any]]] = {}
    for row in active_token_rows:
        for key in row.get("blocking_keys", []):
            block_map.setdefault(key, []).append(row)

    if log is not None:
        log(f"[IdeaTracker] Similarity stage: evaluating {len(block_map)} blocks...")

    seen_pairs: set[tuple[str, str]] = set()
    candidate_rows: list[dict[str, Any]] = []
    total_blocks = len(block_map)
    step = max(1, min(max(1, progress_every), max(1, total_blocks // 50)))
    for block_index, block in enumerate(block_map.values(), start=1):
        if log is not None and (block_index % step == 0 or block_index == total_blocks):
            log(
                f"[IdeaTracker] Similarity stage: processed blocks "
                f"{block_index}/{total_blocks} (pairs seen={len(seen_pairs)})"
            )
        if len(block) < 2:
            continue
        for left_index in range(len(block) - 1):
            left_row = block[left_index]
            left_id = left_row.get("idea_id", "")
            if not left_id:
                continue
            for right_index in range(left_index + 1, len(block)):
                right_row = block[right_index]
                right_id = right_row.get("idea_id", "")
                if not right_id:
                    continue
                pair_key = (min(left_id, right_id), max(left_id, right_id))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)
                if scope_idea_ids is not None and not ({left_id, right_id} & scope_idea_ids):
                    continue
                signals = _idea_similarity(left_row, right_row)
                score = signals["score"]
                if score < review_threshold:
                    continue
                left_mapping = mapping_index[left_id]
                right_mapping = mapping_index[right_id]
                candidate_rows.append(
                    {
                        "left_idea_id": pair_key[0],
                        "right_idea_id": pair_key[1],
                        "score": score,
                        "type": "merge_candidate" if score >= merge_threshold else "review_candidate",
                        "signals": signals,
                        "paths": [left_mapping.get("source_path", ""), right_mapping.get("source_path", "")],
                        "batch_id": similarity_batch_id,
                    }
                )

    if log is not None:
        total_active = len(active_token_rows)
        exhaustive = total_active * (total_active - 1) // 2
        log(
            f"[IdeaTracker] Similarity blocking: {total_active} active records, "
            f"{len(seen_pairs)} pairs evaluated (vs {exhaustive} exhaustive), "
            f"{len(candidate_rows)} above threshold"
        )

    return sorted(
        candidate_rows,
        key=lambda item: (-item.get("score", 0.0), item.get("left_idea_id", ""), item.get("right_idea_id", "")),
    )
