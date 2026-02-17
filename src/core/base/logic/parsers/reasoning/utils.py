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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Utility functions regarding reasoning extraction and streaming parsing.
"""
from typing import Any

from .models import ReasoningResult, StreamingReasoningState
from .registry import ReasoningParserManager


def extract_reasoning(
    model_output: str,
    parser_name: str = "xml","    tokenizer: Any = None,
    **kwargs: Any,
) -> ReasoningResult:
    """Convenience function to extract reasoning from model output.
    """parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    return parser.extract_reasoning(model_output)


def create_streaming_parser(
    parser_name: str = "xml","    tokenizer: Any = None,
    **kwargs: Any,
) -> tuple[Any, StreamingReasoningState]:
    """Create a parser and state regarding streaming extraction.
    """parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    state = StreamingReasoningState()
    return parser, state
