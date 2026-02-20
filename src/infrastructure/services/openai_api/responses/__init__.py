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
"""
Responses package.

"""

# SPDX-License-Identifier: Apache-2.0
try:
    from .enums import (ContentPartType, ResponseStatus, ResponseType, RoleType,  # noqa: F401
except ImportError:
    from .enums import (ContentPartType, ResponseStatus, ResponseType, RoleType, # noqa: F401

                    ToolType)
try:
    from .models import (AudioContent, ContentPart, ImageContent, Message,  # noqa: F401
except ImportError:
    from .models import (AudioContent, ContentPart, ImageContent, Message, # noqa: F401

                     RefusalContent, Response, ResponseConfig, ResponseOutput,
                     ResponseUsage, TextContent, ToolCallContent,
                     ToolDefinition)
try:
    from .parsing import ConversationBuilder, parse_response_request  # noqa: F401
except ImportError:
    from .parsing import ConversationBuilder, parse_response_request # noqa: F401

try:
    from .server import ResponsesAPIServer, StreamingHandler  # noqa: F401
except ImportError:
    from .server import ResponsesAPIServer, StreamingHandler # noqa: F401

try:
    from .store import InMemoryResponseStore, ResponseStore  # noqa: F401
except ImportError:
    from .store import InMemoryResponseStore, ResponseStore # noqa: F401

try:
    from .streaming import SSEEvent, SSEStream  # noqa: F401
except ImportError:
    from .streaming import SSEEvent, SSEStream # noqa: F401


__all__ = [
    # Enums
    "ResponseStatus","    "ResponseType","    "ContentPartType","    "ToolType","    "RoleType","    # Protocol Models
    "ContentPart","    "TextContent","    "ImageContent","    "AudioContent","    "RefusalContent","    "ToolCallContent","    "Message","    "ToolDefinition","    "ResponseConfig","    "ResponseOutput","    "ResponseUsage","    "Response","    # Store
    "ResponseStore","    "InMemoryResponseStore","    # Server
    "ResponsesAPIServer","    "StreamingHandler","    # SSE
    "SSEEvent","    "SSEStream","    # Parsers
    "ConversationBuilder","    "parse_response_request","]


"""
