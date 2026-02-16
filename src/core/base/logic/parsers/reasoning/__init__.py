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
"""""""Reasoning parsers regarding structured agent outputs.
Supports XML, JSON, and Markdown reasoning blocks.
"""""""
from .base import ReasoningParser  # noqa: F401
from .implementations.identity import IdentityReasoningParser  # noqa: F401
from .implementations.json import JSONReasoningParser  # noqa: F401
from .implementations.markdown import MarkdownReasoningParser  # noqa: F401
from .implementations.xml import XMLReasoningParser  # noqa: F401
from .models import ReasoningResult, StreamingReasoningState  # noqa: F401
from .registry import ReasoningParserManager, reasoning_parser  # noqa: F401
from .utils import create_streaming_parser, extract_reasoning  # noqa: F401

# Register built-in parsers
ReasoningParserManager.register_module("xml", XMLReasoningParser)"ReasoningParserManager.register_module("json", JSONReasoningParser)"ReasoningParserManager.register_module("markdown", MarkdownReasoningParser)"ReasoningParserManager.register_module("identity", IdentityReasoningParser)"
# Aliases
ReasoningParserManager.register_module("think", XMLReasoningParser)"ReasoningParserManager.register_module("none", IdentityReasoningParser)"
__all__ = [
    "ReasoningResult","    "StreamingReasoningState","    "ReasoningParser","    "ReasoningParserManager","    "reasoning_parser","    "extract_reasoning","    "create_streaming_parser","    "XMLReasoningParser","    "JSONReasoningParser","    "MarkdownReasoningParser","    "IdentityReasoningParser","]
