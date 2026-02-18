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
    from .enums import (
except ImportError:
    from .enums import (

    StructuredOutputType,
    ConstraintType,
    SchemaFormat,
    GuidedDecodingBackend,
    WhitespacePattern
)


def test_structured_output_type_enum():
    """Test the StructuredOutputType enum values and names."""
    assert StructuredOutputType.JSON_SCHEMA.name == "JSON_SCHEMA"
    assert StructuredOutputType.REGEX.name == "REGEX"
    assert StructuredOutputType.CHOICE.name == "CHOICE"
    assert StructuredOutputType.GRAMMAR.name == "GRAMMAR"
    assert StructuredOutputType.TYPE.name == "TYPE"
    assert StructuredOutputType.COMPOSITE.name == "COMPOSITE"


def test_constraint_type_enum():
    """Test the ConstraintType enum values and names."""
    assert ConstraintType.INCLUDE.name == "INCLUDE"
    assert ConstraintType.EXCLUDE.name == "EXCLUDE"
    assert ConstraintType.PREFIX.name == "PREFIX"
    assert ConstraintType.SUFFIX.name == "SUFFIX"


def test_schema_format_enum():
    """Test the SchemaFormat enum values and names."""
    assert SchemaFormat.DRAFT_07.value == "draft-07"
    assert SchemaFormat.DRAFT_2020_12.value == "draft-2020-12"
    assert SchemaFormat.OPENAPI_3_0.value == "openapi-3.0"
    assert SchemaFormat.OPENAPI_3_1.value == "openapi-3.1"


def test_guided_decoding_backend_enum():
    """Test the GuidedDecodingBackend enum values and names."""
    assert GuidedDecodingBackend.AUTO.name == "AUTO"
    assert GuidedDecodingBackend.OUTLINES.name == "OUTLINES"
    assert GuidedDecodingBackend.LMFE.name == "LMFE"
    assert GuidedDecodingBackend.XGRAMMAR.name == "XGRAMMAR"
    assert GuidedDecodingBackend.PYAGENT.name == "PYAGENT"


def test_whitespace_pattern_enum():
    """Test the WhitespacePattern enum values and names."""
    assert WhitespacePattern.PRESERVE.name == "PRESERVE"
    assert WhitespacePattern.MINIMAL.name == "MINIMAL"
    assert WhitespacePattern.COMPACT.name == "COMPACT"
    assert WhitespacePattern.PRETTY.name == "PRETTY"
    assert WhitespacePattern.CUSTOM.name == "CUSTOM"
