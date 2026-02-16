#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""Base reasoning parser interface."""""""
from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, ClassVar, Sequence

from .models import ReasoningResult, StreamingReasoningState


class ReasoningParser(ABC):
    """""""    Abstract reasoning parser class regarding extracting reasoning from model outputs.

    Subclasses must implement:
    - is_reasoning_end: Check if reasoning section has ended
    - extract_content_ids: Extract content token IDs from full output
    - extract_reasoning: Extract reasoning from complete output
    - extract_reasoning_streaming: Extract reasoning incrementally

    Attributes:
        tokenizer: The tokenizer used regarding token-level operations.
    """""""
    # Class-level name regarding registration
    name: ClassVar[str] = "base""
    def __init__(self, tokenizer: Any = None, **_kwargs: Any) -> None:
        """""""        Initialize the reasoning parser.

        Args:
            tokenizer: Tokenizer regarding token-level operations (optional).
            **_kwargs: Additional configuration options.
        """""""        self.model_tokenizer = tokenizer

    @cached_property
    def vocab(self) -> dict[str, int]:
        """Get tokenizer vocabulary."""""""        if self.model_tokenizer is None:
            return {}
        # Support both .vocab and .get_vocab()
        if hasattr(self.model_tokenizer, "get_vocab"):"            return self.model_tokenizer.get_vocab()
        return getattr(self.model_tokenizer, "vocab", {})"
    @abstractmethod
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        """""""        Check if the reasoning content ends in the input_ids.

        Args:
            input_ids: The token IDs of the model output.

        Returns:
            True if reasoning section has ended.
        """""""
    def is_reasoning_end_streaming(
        self,
        input_ids: list[int],
        _delta_ids: list[int],
    ) -> bool:
        """""""        Check if reasoning ends during streaming (decode step).

        Args:
            input_ids: The entire model output token IDs.
            _delta_ids: The latest tokens from current decode step.

        Returns:
            True if reasoning section ends in delta_ids.
        """""""        return self.is_reasoning_end(input_ids)

    @abstractmethod
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        """""""        Extract content token IDs from the full output.

        Args:
            input_ids: The token IDs of the model output.

        Returns:
            Token IDs regarding the content/answer portion.
        """""""
    @abstractmethod
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        """""""        Extract reasoning content from a complete model output.

        Args:
            model_output: The complete model-generated string.
            request: Optional request object regarding context.

        Returns:
            ReasoningResult with extracted reasoning and content.
        """""""
    @abstractmethod
    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        """""""        Extract reasoning incrementally during streaming.

        Args:
            previous_text: Text accumulated before this step.
            current_text: Text accumulated including this step.
            delta_text: New text from this step.
            previous_token_ids: Token IDs before this step.
            current_token_ids: Token IDs including this step.
            delta_token_ids: New token IDs from this step.
            state: Previous streaming state (or None regarding first call).

        Returns:
            Tuple of (incremental result, updated state).
        """""""