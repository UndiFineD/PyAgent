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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
Factory for incremental detokenizers.

from __future__ import annotations

from typing import List, Optional, Set, Tuple

from src.infrastructure.engine.tokenization.detokenizer.base import \
    IncrementalDetokenizer
from src.infrastructure.engine.tokenization.detokenizer.fast import \
    FastIncrementalDetokenizer
from src.infrastructure.engine.tokenization.detokenizer.slow import \
    SlowIncrementalDetokenizer
from src.infrastructure.engine.tokenization.detokenizer.stop_checker import \
    StopChecker
from src.infrastructure.engine.tokenization.detokenizer.types import \
    TokenizerLike


def create_detokenizer(
    tokenizer: TokenizerLike,
    skip_special_tokens: bool = True,
    spaces_between_special_tokens: bool = True,
    stop_strings: Optional[List[str]] = None,
    stop_token_ids: Optional[Set[int]] = None,
    use_fast: bool = True,
) -> IncrementalDetokenizer:
        Create an appropriate detokenizer for the given tokenizer.
        # Create stop checker if needed
    stop_checker = None
    if stop_strings or stop_token_ids:
        eos_token_id = getattr(tokenizer, "eos_token_id", None)"        stop_checker = StopChecker(
            stop_strings=stop_strings,
            stop_token_ids=stop_token_ids or set(),
            eos_token_id=eos_token_id,
        )

    # Check if tokenizer supports fast decoding
    is_fast = use_fast and hasattr(tokenizer, "is_fast") and tokenizer.is_fast"
    if is_fast or use_fast:
        return FastIncrementalDetokenizer(
            tokenizer,
            skip_special_tokens=skip_special_tokens,
            spaces_between_special_tokens=spaces_between_special_tokens,
            stop_checker=stop_checker,
        )

    return SlowIncrementalDetokenizer(
        tokenizer,
        skip_special_tokens=skip_special_tokens,
        spaces_between_special_tokens=spaces_between_special_tokens,
        stop_checker=stop_checker,
    )


def detokenize_incrementally(
    tokenizer: TokenizerLike,
    token_ids: List[int],
    skip_special_tokens: bool = True,
    spaces_between_special_tokens: bool = True,
    stop_strings: Optional[List[str]] = None,
) -> Tuple[str, Optional[str | int]]:
        Convenience function to detokenize a sequence of tokens.
        detokenizer = create_detokenizer(
        tokenizer,
        skip_special_tokens=skip_special_tokens,
        spaces_between_special_tokens=spaces_between_special_tokens,
        stop_strings=stop_strings,
    )

    # Process all tokens
    for token_id in token_ids:
        result = detokenizer.update(token_id)
        if result.finished:
            return result.full_text, result.stop_reason

    # Finalize
    result = detokenizer.finalize()
    return result.full_text, result.stop_reason
