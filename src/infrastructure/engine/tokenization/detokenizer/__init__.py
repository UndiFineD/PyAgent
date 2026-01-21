# SPDX-License-Identifier: Apache-2.0
"""
Incremental detokenization for streaming text generation.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .types import TokenizerLike, DetokenizeResult
    from .stop_checker import StopChecker
    from .base import IncrementalDetokenizer
    from .fast import FastIncrementalDetokenizer
    from .slow import SlowIncrementalDetokenizer
    from .factory import create_detokenizer, detokenize_incrementally

def __getattr__(name: str) -> Any:
    if name == "TokenizerLike":
        from .types import TokenizerLike
        return TokenizerLike
    if name == "DetokenizeResult":
        from .types import DetokenizeResult
        return DetokenizeResult
    if name == "StopChecker":
        from .stop_checker import StopChecker
        return StopChecker
    if name == "IncrementalDetokenizer":
        from .base import IncrementalDetokenizer
        return IncrementalDetokenizer
    if name == "FastIncrementalDetokenizer":
        from .fast import FastIncrementalDetokenizer
        return FastIncrementalDetokenizer
    if name == "SlowIncrementalDetokenizer":
        from .slow import SlowIncrementalDetokenizer
        return SlowIncrementalDetokenizer
    if name == "create_detokenizer":
        from .factory import create_detokenizer
        return create_detokenizer
    if name == "detokenize_incrementally":
        from .factory import detokenize_incrementally
        return detokenize_incrementally
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "TokenizerLike",
    "DetokenizeResult",
    "StopChecker",
    "IncrementalDetokenizer",
    "FastIncrementalDetokenizer",
    "SlowIncrementalDetokenizer",
    "create_detokenizer",
    "detokenize_incrementally",
]

