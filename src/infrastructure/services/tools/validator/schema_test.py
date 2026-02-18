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
except ImportError:
    import pytest

try:
    from infrastructure.services.tools.validator.schema import validate_tool_call, validate_tool_schema, validate_argument_type
except ImportError:
    from infrastructure.services.tools.validator.schema import validate_tool_call, validate_tool_schema, validate_argument_type



def test_validate_tool_call_basic():
    assert callable(validate_tool_call)


def test_validate_tool_schema_basic():
    assert callable(validate_tool_schema)


def test_validate_argument_type_basic():
    assert callable(validate_argument_type)
