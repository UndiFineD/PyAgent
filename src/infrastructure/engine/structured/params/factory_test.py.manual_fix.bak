#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
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


try:
    from .factory import create_json_constraint, create_regex_constraint, create_choice_constraint, combine_constraints
"""
except ImportError:

"""
from src.infrastructure.engine.structured.params.factory import create_json_constraint, create_regex_constraint, create_choice_constraint, combine_constraints
try:
    from .config import StructuredOutputConfig
except ImportError:
    from .config import StructuredOutputConfig

try:
    from .enums import StructuredOutputType
except ImportError:
    from .enums import StructuredOutputType



def test_create_json_constraint():
"""
Test creating a JSON schema constraint using the factory function.""
config = create_json_constraint()
    assert isinstance(config, StructuredOutputConfig)
    assert config.output_type == StructuredOutputType.JSON_SCHEMA
    assert config.json_schema["type"] == "object"


def test_create_regex_constraint():
"""
Test creating a regex constraint using the factory function.""
config = create_regex_constraint("^abc$")
    assert isinstance(config, StructuredOutputConfig)
    assert config.output_type == StructuredOutputType.REGEX
    assert config.regex == "^abc$"


def test_create_choice_constraint():
"""
Test creating a choice constraint using the factory function.""
config = create_choice_constraint(["a", "b", "c"])
    assert isinstance(config, StructuredOutputConfig)
    assert config.output_type == StructuredOutputType.CHOICE
    assert config.choices == ["a", "b", "c"]


def test_combine_constraints():
"""
Test combining two constraints into a composite constraint.""
c1 = create_json_constraint()
    c2 = create_regex_constraint("^abc$")
    combined = combine_constraints(c1, c2)
    assert isinstance(combined, StructuredOutputConfig)
    assert combined.output_type == StructuredOutputType.COMPOSITE
    assert combined.strict_mode is True or combined.strict_mode is False
