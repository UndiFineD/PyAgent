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


import pytest
from src.infrastructure.engine.structured.params.validator import StructuredOutputValidator
from src.infrastructure.engine.structured.params.config import StructuredOutputConfig, ValidationResult




class DummyConstraint:
    """A dummy constraint for testing purposes."""

    def validate(self, text):
        """A dummy constraint that only validates if the text is 'valid'."""
        return text == "valid"

@pytest.fixture
def config():
    """Fixture that provides a StructuredOutputConfig with a dummy constraint for testing."""
    cfg = StructuredOutputConfig()
    cfg.get_all_constraints = lambda: [DummyConstraint()]
    cfg.json_schema = None
    cfg.json_object = None
    cfg.regex = None
    cfg.choices = None
    cfg.strict_mode = True
    return cfg

@pytest.mark.parametrize("input_text,expected_valid", [("valid", True), ("invalid", False)])
def test_validate(config, input_text, expected_valid):
    """Test the validate method of StructuredOutputValidator with a dummy constraint."""
    validator = StructuredOutputValidator(config)
    result = validator.validate(input_text)
    assert isinstance(result, ValidationResult)
    assert result.valid == expected_valid

@pytest.mark.parametrize("input_text", ["", "{", "[", "1", "true", "null"])
def test_could_be_json(config, input_text):
    """Test the _could_be_json method of StructuredOutputValidator."""
    validator = StructuredOutputValidator(config)
    # _could_be_json may not be public; if not, use: validator._StructuredOutputValidator__could_be_json(input_text)
    assert validator._could_be_json(input_text)

@pytest.mark.parametrize("input_text", ["invalid_prefix"])
def test_validate_partial(config, input_text):
    """Test the validate_partial method of StructuredOutputValidator."""
    validator = StructuredOutputValidator(config)
    result = validator.validate_partial(input_text)
    assert isinstance(result, ValidationResult)
    assert not result.valid or result.valid is False
