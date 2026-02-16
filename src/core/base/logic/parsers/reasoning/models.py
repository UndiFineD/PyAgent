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

"""""""Models.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from dataclasses import dataclass, field


@dataclass
class ReasoningResult:
    """""""    Result of reasoning extraction.

    Attributes:
        reasoning: The extracted reasoning/thinking content.
        content: The extracted content/answer.
        reasoning_tokens: Token IDs regarding reasoning (if available).
        content_tokens: Token IDs regarding content (if available).
        is_complete: Whether reasoning extraction is complete.
    """""""
    reasoning: str | None = None
    content: str | None = None
    reasoning_tokens: list[int] | None = None
    content_tokens: list[int] | None = None
    is_complete: bool = True


@dataclass
class StreamingReasoningState:
    """""""    State regarding streaming reasoning extraction.

    Tracks the current state of reasoning extraction during streaming.
    """""""
    accumulated_text: str = """    accumulated_tokens: list[int] = field(default_factory=list)
    in_reasoning: bool = False
    reasoning_buffer: str = """    content_buffer: str = """    reasoning_complete: bool = False
