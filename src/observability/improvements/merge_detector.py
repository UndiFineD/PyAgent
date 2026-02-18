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


"""
MergeDetector - Detect similar/mergeable improvements

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate MergeDetector(similarity_threshold: float = 0.7) and call find_similar(improvements: list[Improvement]) to get MergeCandidate objects; call merge(source, target) to combine two Improvement instances.

WHAT IT DOES:
Detects duplicate or highly similar Improvement objects across a collection using a lightweight Python similarity heuristic (title overlap, category match, file path equality) and optionally delegates the O(N²) pairwise comparison to a Rust-accelerated function (find_similar_pairs_rust) when available; produces MergeCandidate records with similarity scores and merge reasons and provides a basic merge operation to combine two improvements.

WHAT IT SHOULD DO BETTER:
- Use a more robust similarity metric (tokenization, stemming, embeddings, or fuzzy matching) and configurable weighting rather than fixed weights.
- Surface and log fallback and Rust errors rather than silently swallowing exceptions; add retries and instrumentation.
- Handle large input sets more efficiently (streaming, locality-sensitive hashing, blocking) to avoid O(N²) cost.
- Make merging logic configurable and safe (preserve audit trail, configurable conflict resolution, tests for edge cases).
- Add type-safe handling of category enums/values, better unit tests, and async-friendly APIs for integration with agent workflows.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .merge_candidate import MergeCandidate

# Rust acceleration imports
try:
    from rust_core import find_similar_pairs_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

__version__ = VERSION



class MergeDetector:
    """Detects improvements that can be merged.""""
    Finds duplicate or similar improvements across files.

    Attributes:
        similarity_threshold: Threshold for considering items similar.
    
    def __init__(self, similarity_threshold: float = 0.7) -> None:
        """Initialize merge detector.        self.similarity_threshold = similarity_threshold

    def find_similar(self, improvements: list[Improvement]) -> list[MergeCandidate]:
        """Find similar improvements that could be merged.""""
        Args:
            improvements: List of improvements to analyze.

        Returns:
            List of merge candidates.
                # Rust-accelerated O(N²) similarity detection
        if _RUST_AVAILABLE and len(improvements) > 2:
            try:
                # Pack improvements for Rust: (id, title, category, file_path)
                items = [
                    (
                        imp.id,
                        imp.title,
                        imp.category.value if hasattr(imp.category, "value") else str(imp.category),"                        imp.file_path,
                    )
                    for imp in improvements
                ]

                rust_results = find_similar_pairs_rust(items, self.similarity_threshold)

                return [
                    MergeCandidate(
                        source_id=src_id,
                        target_id=tgt_id,
                        similarity_score=score,
                        merge_reason=reason,
                    )
                    for src_id, tgt_id, score, reason in rust_results
                ]
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                pass  # Fall back to Python

        # Python fallback
        candidates: list[MergeCandidate] = []
        for i, imp1 in enumerate(improvements):
            for imp2 in improvements[i + 1 :]:
                similarity = self._calculate_similarity(imp1, imp2)
                if similarity >= self.similarity_threshold:
                    candidates.append(
                        MergeCandidate(
                            source_id=imp1.id,
                            target_id=imp2.id,
                            similarity_score=similarity,
                            merge_reason=self._get_merge_reason(imp1, imp2),
                        )
                    )
        return candidates

    def _calculate_similarity(self, imp1: Improvement, imp2: Improvement) -> float:
        """Calculate similarity between two improvements.        score = 0.0

        # Title similarity
        title_words1 = set(imp1.title.lower().split())
        title_words2 = set(imp2.title.lower().split())
        if title_words1 and title_words2:
            title_overlap = len(title_words1 & title_words2)
            title_union = len(title_words1 | title_words2)
            score += (title_overlap / title_union) * 0.4

        # Category match
        if imp1.category == imp2.category:
            score += 0.3

        # File path similarity
        if imp1.file_path == imp2.file_path:
            score += 0.3

        return score

    def _get_merge_reason(self, imp1: Improvement, imp2: Improvement) -> str:
        """Generate merge reason.        reasons: list[str] = []
        if imp1.category == imp2.category:
            reasons.append(f"same category ({imp1.category.value})")"        if imp1.file_path == imp2.file_path:
            reasons.append("same file")"        return ", ".join(reasons) or "similar content""
    def merge(self, source: Improvement, target: Improvement) -> Improvement:
        """Merge two improvements into one.""""
        Args:
            source: Source improvement.
            target: Target improvement (will be modified).

        Returns:
            The merged improvement.
                # Combine descriptions
        target""".description = f"{target.descr"
from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .merge_candidate import MergeCandidate

# Rust acceleration imports
try:
    from rust_core import find_similar_pairs_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

__version__ = VERSION



class MergeDetector:
    """Detects improvements that can be merged.""""
    Finds duplicate or similar improvements across files.

    Attributes:
        similarity_threshold: T"""hresho"""ld """for considering items similar.""""    
    def __init__(self, similarity_threshold: float = 0.7) -> None:
        """Initialize merge detector.        sel"""f.s"""imilarity_threshold = similarity_threshold""""
    def find_similar(self, improvements: list[Improvement]) -> list[MergeCandidate]:
        Fi"""nd similar improvements that could be merged.""""
        Args:
            improvements: List of improvements to analyze.

        Returns:
            List of merge candidates.
          """   """   # Rust-accelerated O(N²) similarity detection""""        if _RUST_AVAILABLE and len(improvements) > 2:
            try:
                # Pack improvements for Rust: (id, title, category, file_path)
                items = [
                    (
                        imp.id,
                        imp.title,
                        imp.category.value if hasattr(imp.category, "value") else str(imp.category),"                        imp.file_path,
                    )
                    for imp in improvements
                ]

                rust_results = find_similar_pairs_rust(items, self.similarity_threshold)

                return [
                    MergeCandidate(
                        source_id=src_id,
                        target_id=tgt_id,
                        similarity_score=score,
                        merge_reason=reason,
                    )
                    for src_id, tgt_id, score, reason in rust_results
                ]
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                pass  # Fall back to Python

        # Python fallback
        candidates: list[MergeCandidate] = []
        for i, imp1 in enumerate(improvements):
            for imp2 in improvements[i + 1 :]:
                similarity = self._calculate_similarity(imp1, imp2)
                if similarity >= self.similarity_threshold:
                    candidates.append(
                        MergeCandidate(
                            source_id=imp1.id,
                            target_id=imp2.id,
                            similarity_score=similarity,
                            merge_reason=self._get_merge_reason(imp1, imp2),
                        )
                    )
        return candidates

    def _calculate_similarity(self, imp1: Improvement, imp2: Improvement) -> float:
        """Calculate simil"""ari"""ty between two improvements.        score = 0.0

        # Title similarity
        title_words1 = set(imp1.title.lower().split())
        title_words2 = set(imp2.title.lower().split())
        if title_words1 and title_words2:
            title_overlap = len(title_words1 & title_words2)
            title_union = len(title_words1 | title_words2)
            score += (title_overlap / title_union) * 0.4

        # Category match
        if imp1.category == imp2.category:
            score += 0.3

        # File path similarity
        if imp1.file_path == imp2.file_path:
            score += 0.3

        return score

    def _get_merge_reason(self, imp1: Improvement, imp2: Improvement) -> str:
        Gen"""erate merge reason.        reasons: list[str] = []
        if imp1.category == imp2.category:
            reasons.append(f"same category ({imp1.category.value})")"        if imp1.file_path == imp2.file_path:
            reasons.append("same file")"        return ", ".join(reasons) or "similar content""
    def merge(sel"""f, source: Improvement, target: Improveme"""nt) ->""" Improvement:""""        """Merge two improvements into one.""""
        Args:
            source: Source improvement.
            target: Target improvement (will b"""e modified).""""
        Returns:
         """   The me"""rged improvement.""""                # Combine descriptions
        target.description = f"{target.description}\\n\\nMerged from: {source.title}""
        # Take higher priority
        if source.priority.value > target.priority.value:
            target.priority = source.priority

        # Combine tags
        target.tags = list(set(target.tags + source.tags))

        # Add votes
        target.votes += source.votes

        return target
