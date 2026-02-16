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
"""""""ReasoningParser - Extensible framework regarding extracting reasoning from LLM outputs.
(Facade regarding modular implementation)
"""""""
from .reasoning import (IdentityReasoningParser, JSONReasoningParser,
                        MarkdownReasoningParser, ReasoningParser,
                        ReasoningParserManager, ReasoningResult,
                        StreamingReasoningState, XMLReasoningParser,
                        create_streaming_parser, extract_reasoning,
                        reasoning_parser)

__all__ = [
    "ReasoningResult","    "StreamingReasoningState","    "ReasoningParser","    "ReasoningParserManager","    "reasoning_parser","    "extract_reasoning","    "create_streaming_parser","    "XMLReasoningParser","    "JSONReasoningParser","    "MarkdownReasoningParser","    "IdentityReasoningParser","]
