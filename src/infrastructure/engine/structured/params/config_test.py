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


try:
    from .config import StructuredOutputConfig, ValidationResult
except ImportError:
    from .config import StructuredOutputConfig, ValidationResult

try:
    from .enums import StructuredOutputType, GuidedDecodingBackend, WhitespacePattern
except ImportError:
    from .enums import StructuredOutputType, GuidedDecodingBackend, WhitespacePattern



def test_structured_output_config_to_dict():
    """Test that StructuredOutputConfig.to_dict() returns the correct dictionary representation."""
    config = StructuredOutputConfig(
        output_type=StructuredOutputType.JSON_SCHEMA,
        json_schema={"type": "object"},
        json_object=True,
        regex="^abc$",
        choices=["a", "b"],
        grammar="S -> 'a'",
        grammar_type="ebnf",
        backend=GuidedDecodingBackend.AUTO,
        whitespace=WhitespacePattern.MINIMAL,
        strict_mode=True,
    )
    d = config.to_dict()
    assert d["output_type"] == "JSON_SCHEMA"
    assert d["json_schema"] == {"type": "object"}
    assert d["json_object"] is True
    assert d["regex"] == "^abc$"
    assert d["choices"] == ["a", "b"]
    assert d["grammar"] == "S -> 'a'"
    assert d["grammar_type"] == "ebnf"
    assert d["backend"] == "AUTO"
    assert d["whitespace"] == "MINIMAL"
    assert d["strict_mode"] is True


def test_structured_output_config_from_dict():
    """Test that StructuredOutputConfig.from_dict() correctly creates an instance from a dictionary."""
    data = {
        "output_type": "JSON_SCHEMA",
        "json_schema": {"type": "object"},
        "json_object": True,
        "regex": "^abc$",
        "choices": ["a", "b"],
        "grammar": "S -> 'a'",
        "grammar_type": "ebnf",
        "backend": "AUTO",
        "whitespace": "MINIMAL",
        "strict_mode": True,
    }
    config = StructuredOutputConfig.from_dict(data)
    assert config.output_type == StructuredOutputType.JSON_SCHEMA
    assert config.json_schema == {"type": "object"}
    assert config.json_object is True
    assert config.regex == "^abc$"
    assert config.choices == ["a", "b"]
    assert config.grammar == "S -> 'a'"
    assert config.grammar_type == "ebnf"
    assert config.backend == GuidedDecodingBackend.AUTO
    assert config.whitespace == WhitespacePattern.MINIMAL
    assert config.strict_mode is True


def test_validation_result_properties():
    """Test that ValidationResult properties has_errors and has_warnings work correctly."""
    result = ValidationResult(valid=True, errors=["e1"], warnings=["w1"])
    assert result.has_errors is True
    assert result.has_warnings is True
    result2 = ValidationResult(valid=True)
    assert result2.has_errors is False
    assert result2.has_warnings is False
