#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Proposers.py module.
"""


from __future__ import annotations


try:
    from typing import Protocol, Sequence
except ImportError:
    from typing import Protocol, Sequence


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import DraftProposal
except ImportError:
    from .config import DraftProposal




class DraftProposer(Protocol):
    """Protocol for draft token proposers.
    def propose(
        self,
        request_id: str,
        token_ids: Sequence[int],
        max_tokens: int,
    ) -> DraftProposal:
        """Propose draft tokens for a request.        ...

    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update proposer state with new tokens.        ...



class NgramProposer:
        N-gram based draft proposer.

    Matches patterns from the prompt to propose likely continuations.
    
    def __init__(
        self,
        prompt_lookup_min: int = 3,
        prompt_lookup_max: int = 5,
    ) -> None:
        self.prompt_lookup_min = prompt_lookup_min
        self.prompt_lookup_max = prompt_lookup_max

        # Request state: request_id -> prompt_token_ids
        self._prompts: dict[str, list[int]] = {}
        self._outputs: dict[str, list[int]] = {}

    def start_request(self, request_id: str, prompt_token_ids: list[int]) -> None:
        """Initialize state for a new request.        self._prompts[request_id] = list(prompt_token_ids)
        self._outputs[request_id] = []

    def stop_request(self, request_id: str) -> None:
        """Clean up state for a finished request.        self._prompts.pop(request_id, None)
        self._outputs.pop(request_id, None)

    def propose(
        self,
        request_id: str,
        token_ids: Sequence[int],
        max_tokens: int,
    ) -> DraftProposal:
        """Propose draft tokens using n-gram matching.        if request_id not in self._prompts:
            return DraftProposal(request_id=request_id, token_ids=[])

        prompt = self._prompts[request_id]
        output = self._outputs.get(request_id, [])
        all_tokens = prompt + output

        if len(all_tokens) < self.prompt_lookup_min:
            return DraftProposal(request_id=request_id, token_ids=[])

        # Search for n-gram matches
        draft_tokens: list[int] = []

        for n in range(self.prompt_lookup_max, self.prompt_lookup_min - 1, -1):
            if len(all_tokens) < n:
                continue

            # Pattern to match (last n tokens)
            pattern = all_tokens[-n:]

            # Search in prompt for matches
            match_result = self._find_ngram_match(prompt, pattern, max_tokens)
            if match_result:
                draft_tokens = match_result
                break

        return DraftProposal(request_id=request_id, token_ids=draft_tokens)

    def _find_ngram_match(
        self,
        tokens: list[int],
        pattern: list[int],
        max_tokens: int,
    ) -> list[int] | None:
        """Find n-gram pattern in tokens and return continuation.        n = len(pattern)

        # Search from end to find most recent match
        for i in range(len(tokens) - n - 1, -1, -1):
            if tokens[i : i + n] == pattern:
                # Found match, return continuation
                continuation_start = i + n
                continuation_end = min(continuation_start + max_tokens, len(tokens))
                if continuation_start < len(tokens):
                    return tokens[continuation_start:continuation_end]

        return None

    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update output tokens for a request.        if request_id in self._outputs:
            self._outputs[request_id].extend(new_token_ids)



class SuffixNode:
    """Node in a suffix tree.
    __slots__ = ("children", "count", "continuations")"
    def __init__(self) -> None:
        self.children: dict[int, SuffixNode] = {}
        self.count: int = 0
        self.continuations: dict[int, int] = {}  # token -> frequency



class SuffixProposer:
        Suffix tree based draft proposer.

    Builds a suffix tree from past generations and uses frequency
    counts to propose likely continuations.
    
    def __init__(
        self,
        max_tree_depth: int = 24,
        max_cached_requests: int = 10000,
        max_spec_factor: float = 1.0,
        min_token_prob: float = 0.1,
    ) -> None:
        self.max_tree_depth = max_tree_depth
        self.max_cached_requests = max_cached_requests
        self.max_spec_factor = max_spec_factor
        self.min_token_prob = min_token_prob

        # Global suffix tree (shared across requests)
        self._global_root = SuffixNode()

        # Per-request prompt trees
        self._prompt_trees: dict[str, SuffixNode] = {}
        self._request_tokens: dict[str, list[int]] = {}

        # LRU tracking for eviction
        self._request_order: list[str] = []

    def start_request(self, request_id: str, prompt_token_ids: list[int]) -> None:
        """Initialize suffix tree for a new request.        # Build prompt tree
        root = SuffixNode()
        self._build_tree(root, prompt_token_ids)
        self._prompt_trees[request_id] = root
        self._request_tokens[request_id] = []

        # Track for LRU
        if request_id in self._request_order:
            self._request_order.remove(request_id)
        self._request_order.append(request_id)

        # Evict if needed
        self._maybe_evict()

    def stop_request(self, request_id: str) -> None:
        """Add request tokens to global tree and clean up.        if request_id in self._request_tokens:
            tokens = self._request_tokens[request_id]
            if tokens:
                self._build_tree(self._global_root, tokens)

        self._prompt_trees.pop(request_id, None)
        self._request_tokens.pop(request_id, None)
        if request_id in self._request_order:
            self._request_order.remove(request_id)

    def _build_tree(self, root: SuffixNode, tokens: list[int]) -> None:
        """Build suffix tree from tokens.        for start in range(len(tokens)):
            node = root
            for i in range(start, min(start + self.max_tree_depth, len(tokens))):
                token = tokens[i]
                if token not in node.children:
                    node.children[token] = SuffixNode()
                node = node.children[token]
                node.count += 1

                # Track continuations
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    node.continuations[next_token] = node.continuations.get(next_token, 0) + 1

    def _maybe_evict(self) -> None:
        """Evict old requests if over limit.        while len(self._request_order) > self.max_cached_requests:
            old_id = self._request_order.pop(0)
            self._prompt_trees.pop(old_id, None)
            self._request_tokens.pop(old_id, None)

    def propose(
        self,
        request_id: str,
        token_ids: Sequence[int],
        max_tokens: int,
    ) -> DraftProposal:
        """Propose draft tokens using suffix matching.        if request_id not in self._prompt_trees:
            return DraftProposal(request_id=request_id, token_ids=[])

        # Get pattern (last few tokens)
        pattern_len = min(self.max_tree_depth, len(token_ids))
        pattern = list(token_ids[-pattern_len:]) if pattern_len > 0 else []

        if not pattern:
            return DraftProposal(request_id=request_id, token_ids=[])

        # Search in prompt tree first, then global
        draft_tokens: list[int] = []
        logprobs: list[float] = []

        trees = [self._prompt_trees[request_id], self._global_root]

        for tree in trees:
            result = self._search_tree(tree, pattern, max_tokens)
            if result:
                draft_tokens, logprobs = result
                break

        return DraftProposal(
            request_id=request_id,
            token_ids=draft_tokens,
            logprobs=logprobs if logprobs else None,
        )

    def _search_tree(
        self,
        root: SuffixNode,
        pattern: list[int],
        max_tokens: int,
    ) -> tuple[list[int], list[float]] | None:
        """Search suffix tree for pattern and return continuations.        # Navigate to pattern end
        node = root
        for token in pattern:
            if token not in node.children:
                return None
            node = node.children[token]

        # Collect continuations based on frequency
        draft_tokens: list[int] = []
        logprobs: list[float] = []

        current_node = node
        for _ in range(max_tokens):
            if not current_node.continuations:
                break

            # Find most frequent continuation
            total = sum(current_node.continuations.values())
            best_token = max(current_node.continuations.keys(), key=lambda t: current_node.continuations[t])
            freq = current_node.continuations[best_token]
            prob = freq / total

            # Check minimum probability threshold
            if prob < self.min_token_prob:
                break

            draft_tokens.append(best_token)
            logprobs.append(float(np.log(prob)))

            # Move to next node
            if best_token in current_node.children:
                current_node = current_node.children[best_token]
            else:
                break

        if not draft_tokens:
            return None

        return draft_tokens, logprobs

    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update request tokens and rebuild tree.        if request_id in self._request_tokens:
            self._request_tokens[request_id].extend(new_token_ids)


def ngram_match(
    tokens: list[int],
    pattern: list[int],
    max_continuation: int = 5,
) -> list[int] | None:
        Find n-gram pattern match in tokens.

    Returns continuation tokens after the pattern match, or None if not found.
        n = len(pattern)
    if n == 0 or len(tokens) < n:
        return None

    for i in range(len(tokens) - n, -1, -1):
        if tokens[i : i + n] == pattern:
            start = i + n
            end = min(start + max_continuation, len(tokens))
            if start < len(tokens):
                return tokens[start:end]

    return None
