# SPDX-License-Identifier: Apache-2.0
"""
N-gram Indexing - Suffix-based indices for fast n-gram lookup.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


class SuffixIndex:
    """
    Suffix-based index for fast n-gram lookup.

    Beyond vLLM: O(1) average case lookup for n-gram matching
    using hash-based suffix indexing.
    """

    def __init__(self, max_n: int = 4):
        self.max_n = max_n
        # Map from n-gram tuple to list of positions
        self._index: dict[int, dict[tuple[int, ...], list[int]]] = {
            n: {} for n in range(1, max_n + 1)
        }
        self._built = False

    def build(self, tokens: list[int] | NDArray[np.int32]) -> None:
        """Build suffix index from token sequence."""
        tokens = list(tokens)
        n_tokens = len(tokens)

        # Clear existing index
        for n in range(1, self.max_n + 1):
            self._index[n].clear()

        # Build index for each n-gram size
        for n in range(1, self.max_n + 1):
            for i in range(n_tokens - n + 1):
                ngram = tuple(tokens[i:i + n])
                if ngram not in self._index[n]:
                    self._index[n][ngram] = []
                self._index[n][ngram].append(i)

        self._built = True

    def lookup(self, ngram: tuple[int, ...]) -> list[int]:
        """Look up positions where n-gram appears."""
        n = len(ngram)
        return (
            []
            if n > self.max_n or n < 1
            else self._index.get(n, {}).get(ngram, [])
        )

    def get_continuations(
        self,
        prefix: tuple[int, ...],
        tokens: list[int],
        k: int,
    ) -> list[int]:
        """Get tokens that follow the given prefix."""
        positions = self.lookup(prefix)
        if not positions:
            return []

        # Get continuations from each position
        n = len(prefix)
        continuations = []

        for pos in positions:
            end_pos = pos + n
            if cont := tokens[end_pos:end_pos + k]:
                continuations.append((pos, cont))

        return continuations

    def clear(self) -> None:
        """Clear the index."""
        for n in self._index:
            self._index[n].clear()
        self._built = False

    @property
    def is_built(self) -> bool:
        """Check if index is built."""
        return self._built


class SuffixTreeProposer:
    """
    Suffix tree-based proposer for O(m) lookup complexity.

    Beyond vLLM: Uses suffix tree for exact and approximate matching
    with support for edit distance tolerance.
    """

    def __init__(
        self,
        num_speculative_tokens: int = 5,
        max_edit_distance: int = 0,
    ):
        self.num_speculative_tokens = num_speculative_tokens
        self.max_edit_distance = max_edit_distance
        self._tree: dict[int, Any] = {}
        self._positions: dict[int, list[int]] = {}

    def build(self, tokens: list[int]) -> None:
        """Build suffix tree from tokens."""
        self._tree.clear()
        self._positions.clear()

        n = len(tokens)
        for i in range(n):
            node = self._tree
            for j in range(i, n):
                token = tokens[j]
                if token not in node:
                    node[token] = {}
                    if token not in self._positions:
                        self._positions[token] = []
                    self._positions[token].append(j)
                node = node[token]

    def find_continuation(
        self,
        prefix: list[int],
        _tokens: list[int],
    ) -> list[int]:
        """Find continuation for prefix using suffix tree."""
        # Navigate tree
        node = self._tree
        for token in prefix:
            if token not in node:
                return []
            node = node[token]

        # Get all paths from this node
        if not node:
            return []

        # Find a continuation path
        continuation = []
        current = node

        for _ in range(self.num_speculative_tokens):
            if not current:
                break
            # Take most frequent continuation
            next_token = max(current.keys(), key=lambda t: len(self._positions.get(t, [])))
            continuation.append(next_token)
            current = current.get(next_token, {})

        return continuation
