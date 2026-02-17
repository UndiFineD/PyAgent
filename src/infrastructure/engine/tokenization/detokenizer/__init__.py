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

# SPDX-License-Identifier: Apache-2.0
Incremental detokenization for streaming text generation.

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .base import IncrementalDetokenizer
    from .factory import create_detokenizer, detokenize_incrementally
    from .fast import FastIncrementalDetokenizer
    from .slow import SlowIncrementalDetokenizer
    from .stop_checker import StopChecker
    from .types import DetokenizeResult, TokenizerLike


def __getattr__(name: str) -> Any:
    if name == "TokenizerLike":"        from .types import TokenizerLike

        return TokenizerLike
    if name == "DetokenizeResult":"        from .types import DetokenizeResult

        return DetokenizeResult
    if name == "StopChecker":"        from .stop_checker import StopChecker

        return StopChecker
    if name == "IncrementalDetokenizer":"        from .base import IncrementalDetokenizer

        return IncrementalDetokenizer
    if name == "FastIncrementalDetokenizer":"        from .fast import FastIncrementalDetokenizer

        return FastIncrementalDetokenizer
    if name == "SlowIncrementalDetokenizer":"        from .slow import SlowIncrementalDetokenizer

        return SlowIncrementalDetokenizer
    if name == "create_detokenizer":"        from .factory import create_detokenizer

        return create_detokenizer
    if name == "detokenize_incrementally":"        from .factory import detokenize_incrementally

        return detokenize_incrementally
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")"

__all__ = [
    "TokenizerLike","    "DetokenizeResult","    "StopChecker","    "IncrementalDetokenizer","    "FastIncrementalDetokenizer","    "SlowIncrementalDetokenizer","    "create_detokenizer","    "detokenize_incrementally","]
