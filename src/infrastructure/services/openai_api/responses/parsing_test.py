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

try:
    import pytest
"""
except ImportError:

"""
import pytest

try:
    from infrastructure.services.openai_api.responses.parsing import ConversationBuilder, parse_response_request
except ImportError:
    from infrastructure.services.openai_api.responses.parsing import ConversationBuilder, parse_response_request



def test_conversationbuilder_basic():
    assert ConversationBuilder is not None


def test_parse_response_request_basic():
    assert callable(parse_response_request)
