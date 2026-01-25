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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Base class for incremental detokenization.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from src.infrastructure.engine.tokenization.detokenizer.stop_checker import \
    StopChecker
from src.infrastructure.engine.tokenization.detokenizer.types import (
    DetokenizeResult, TokenizerLike)


class IncrementalDetokenizer(ABC):
    """
    Abstract base class for incremental detokenization.
    """

    def __init__(
        self,
        tokenizer: TokenizerLike,
        skip_special_tokens: bool = True,
        spaces_between_special_tokens: bool = True,
        stop_checker: Optional[StopChecker] = None,
    ):
        self.tokenizer = tokenizer
        self.skip_special_tokens = skip_special_tokens
        self.spaces_between_special_tokens = spaces_between_special_tokens
        self.stop_checker = stop_checker

        # State
        self.token_ids: List[int] = []
        self.prefix_offset: int = 0
        self.read_offset: int = 0
        self.output_text: str = ""
        self._finished: bool = False
        self._stop_reason: Optional[Union[str, int]] = None

    def reset(self) -> None:
        """Reset the detokenizer state."""
        self.token_ids.clear()
        self.prefix_offset = 0
        self.read_offset = 0
        self.output_text = ""
        self._finished = False
        self._stop_reason = None

    @property
    def is_finished(self) -> bool:
        """Check if detokenization is finished."""
        return self._finished

    @abstractmethod
    def _decode_tokens(
        self,
        token_ids: List[int],
        prefix_offset: int,
        read_offset: int,
    ) -> Tuple[str, int, int]:
        """Decode tokens to text with offset tracking."""
        raise NotImplementedError("Subclasses must implement _decode_tokens()")

    def update(
        self,
        new_token_ids: Union[int, List[int]],
        finished: bool = False,
    ) -> DetokenizeResult:
        """Update with new token IDs and return new text."""
        if self._finished:
            return DetokenizeResult(
                new_text="",
                full_text=self.output_text,
                prefix_offset=self.prefix_offset,
                read_offset=self.read_offset,
                finished=True,
                stop_reason=self._stop_reason,
            )

        # Normalize to list
        if isinstance(new_token_ids, int):
            new_token_ids = [new_token_ids]

        # Check for stop tokens
        if self.stop_checker:
            for token_id in new_token_ids:
                stop_token = self.stop_checker.check_token(token_id)
                if stop_token is not None:
                    self._finished = True
                    self._stop_reason = stop_token
                    break
            else:
                self.token_ids.extend(new_token_ids)
        else:
            self.token_ids.extend(new_token_ids)

        # Decode tokens
        new_text, new_prefix, new_read = self._decode_tokens(
            self.token_ids,
            self.prefix_offset,
            self.read_offset,
        )

        self.prefix_offset = new_prefix
        self.read_offset = new_read

        # Check for stop strings
        if self.stop_checker and new_text:
            stop_string, text_before = self.stop_checker.check_text(self.output_text + new_text)
            if stop_string is not None:
                new_text = text_before[len(self.output_text) :]
                self._finished = True
                self._stop_reason = stop_string

        self.output_text += new_text

        # If this is the final update, flush any buffered text
        if finished and not self._finished:
            self._finished = True

        return DetokenizeResult(
            new_text=new_text,
            full_text=self.output_text,
            prefix_offset=self.prefix_offset,
            read_offset=self.read_offset,
            finished=self._finished,
            stop_reason=self._stop_reason,
        )

    def finalize(self) -> DetokenizeResult:
        """Finalize and return remaining text."""
        return self.update([], finished=True)
