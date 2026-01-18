# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Truncation management for prompt rendering.
"""

from __future__ import annotations

from typing import List, Tuple

from .models import TruncationResult, TruncationStrategy


class TruncationManager:
    """Manage prompt truncation strategies."""

    @classmethod
    def truncate(
        cls,
        tokens: List[int],
        max_tokens: int,
        strategy: TruncationStrategy = TruncationStrategy.AUTO,
        reserve_tokens: int = 0,
    ) -> Tuple[List[int], TruncationResult]:
        """Truncate token sequence to fit within limit."""
        target_tokens = max_tokens - reserve_tokens
        original_len = len(tokens)

        if original_len <= target_tokens:
            return tokens, TruncationResult(
                original_tokens=original_len,
                truncated_tokens=original_len,
                removed_tokens=0,
                strategy_used=TruncationStrategy.NONE,
            )

        if strategy == TruncationStrategy.NONE:
            return tokens, TruncationResult(
                original_tokens=original_len,
                truncated_tokens=original_len,
                removed_tokens=0,
                strategy_used=TruncationStrategy.NONE,
                warning_message=f"Prompt exceeds limit by {original_len - target_tokens} tokens",
            )

        if strategy in (TruncationStrategy.AUTO, TruncationStrategy.LEFT):
            return cls._truncate_left(tokens, target_tokens, original_len)
        if strategy == TruncationStrategy.RIGHT:
            return cls._truncate_right(tokens, target_tokens, original_len)
        if strategy == TruncationStrategy.MIDDLE:
            return cls._truncate_middle(tokens, target_tokens, original_len)
        if strategy == TruncationStrategy.SMART:
            return cls._truncate_smart(tokens, target_tokens, original_len)

        return cls._truncate_left(tokens, target_tokens, original_len)

    @classmethod
    def _truncate_left(cls, tokens: List[int], target: int, original: int) -> Tuple[List[int], TruncationResult]:
        removed = original - target
        truncated = tokens[removed:]
        return truncated, TruncationResult(
            original_tokens=original, truncated_tokens=len(truncated), removed_tokens=removed,
            strategy_used=TruncationStrategy.LEFT, removed_ranges=[(0, removed)]
        )

    @classmethod
    def _truncate_right(cls, tokens: List[int], target: int, original: int) -> Tuple[List[int], TruncationResult]:
        truncated = tokens[:target]
        removed = original - target
        return truncated, TruncationResult(
            original_tokens=original, truncated_tokens=len(truncated), removed_tokens=removed,
            strategy_used=TruncationStrategy.RIGHT, removed_ranges=[(target, original)]
        )

    @classmethod
    def _truncate_middle(cls, tokens: List[int], target: int, original: int) -> Tuple[List[int], TruncationResult]:
        keep_start = target // 2
        keep_end = target - keep_start
        truncated = tokens[:keep_start] + tokens[-keep_end:]
        removed = original - target
        return truncated, TruncationResult(
            original_tokens=original, truncated_tokens=len(truncated), removed_tokens=removed,
            strategy_used=TruncationStrategy.MIDDLE, removed_ranges=[(keep_start, original - keep_end)]
        )

    @classmethod
    def _truncate_smart(cls, tokens: List[int], target: int, original: int) -> Tuple[List[int], TruncationResult]:
        return cls._truncate_left(tokens, target, original)
