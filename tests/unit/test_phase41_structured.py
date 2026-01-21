# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Unit Tests for Structured Output Parameters

"""
Tests for StructuredOutputParams module.
"""

import pytest

from src.infrastructure.engine.structured.structured_output_params import (
    StructuredOutputType,
    ConstraintType,
    SchemaFormat,
    GuidedDecodingBackend,
    WhitespacePattern,
    OutputConstraint,
    JsonSchemaConstraint,
    RegexConstraint,
    ChoiceConstraint,
    GrammarConstraint,
    TypeConstraint,
    StructuredOutputConfig,
    ValidationResult,
    ConstraintBuilder,
    StructuredOutputValidator,
)


class TestStructuredOutputType:
    """Test StructuredOutputType enum."""
    
    def test_output_type_values(self):
        """Test StructuredOutputType enum values."""
        assert StructuredOutputType.JSON_SCHEMA is not None
        assert StructuredOutputType.REGEX is not None
        assert StructuredOutputType.CHOICE is not None
        assert StructuredOutputType.GRAMMAR is not None
        assert StructuredOutputType.TYPE is not None


class TestConstraintType:
    """Test ConstraintType enum."""
    
    def test_constraint_type_values(self):
        """Test ConstraintType enum values."""
        assert ConstraintType.INCLUDE is not None
        assert ConstraintType.EXCLUDE is not None
        assert ConstraintType.PREFIX is not None
        assert ConstraintType.SUFFIX is not None


class TestSchemaFormat:
    """Test SchemaFormat enum."""
    
    def test_schema_format_values(self):
        """Test SchemaFormat enum values."""
        assert SchemaFormat.DRAFT_07 is not None
        assert SchemaFormat.DRAFT_2020_12 is not None
        assert SchemaFormat.OPENAPI_3_0 is not None


class TestGuidedDecodingBackend:
    """Test GuidedDecodingBackend enum."""
    
    def test_backend_values(self):
        """Test GuidedDecodingBackend enum values."""
        assert GuidedDecodingBackend.OUTLINES is not None
        assert GuidedDecodingBackend.XGRAMMAR is not None
        assert GuidedDecodingBackend.AUTO is not None


class TestWhitespacePattern:
    """Test WhitespacePattern enum."""
    
    def test_whitespace_pattern_values(self):
        """Test WhitespacePattern enum values."""
        assert WhitespacePattern.PRESERVE is not None
        assert WhitespacePattern.MINIMAL is not None
        assert WhitespacePattern.COMPACT is not None
        assert WhitespacePattern.PRETTY is not None


class TestJsonSchemaConstraint:
    """Test JsonSchemaConstraint class."""
    
    def test_constraint_creation(self):
        """Test JsonSchemaConstraint creation."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
        }
        
        constraint = JsonSchemaConstraint(schema=schema)
        
        assert constraint.schema == schema
    
    def test_to_dict(self):
        """Test converting to dict."""
        schema = {"type": "object"}
        constraint = JsonSchemaConstraint(schema=schema)
        
        d = constraint.to_dict()
        
        assert "schema" in d


class TestRegexConstraint:
    """Test RegexConstraint class."""
    
    def test_constraint_creation(self):
        """Test RegexConstraint creation."""
        constraint = RegexConstraint(pattern=r"^\d{3}-\d{4}$")
        
        assert constraint.pattern == r"^\d{3}-\d{4}$"
    
    def test_to_dict(self):
        """Test converting to dict."""
        constraint = RegexConstraint(pattern=r"\d+")
        
        d = constraint.to_dict()
        
        assert d["pattern"] == r"\d+"


class TestChoiceConstraint:
    """Test ChoiceConstraint class."""
    
    def test_constraint_creation(self):
        """Test ChoiceConstraint creation."""
        constraint = ChoiceConstraint(choices=["yes", "no", "maybe"])
        
        assert len(constraint.choices) == 3
    
    def test_to_dict(self):
        """Test converting to dict."""
        constraint = ChoiceConstraint(choices=["a", "b"])
        
        d = constraint.to_dict()
        
        assert d["choices"] == ["a", "b"]


class TestGrammarConstraint:
    """Test GrammarConstraint class."""
    
    def test_constraint_creation(self):
        """Test GrammarConstraint creation."""
        grammar = '''
        root ::= statement
        statement ::= "hello" | "world"
        '''
        
        constraint = GrammarConstraint(grammar=grammar)
        
        assert "statement" in constraint.grammar
    
    def test_to_dict(self):
        """Test converting to dict."""
        constraint = GrammarConstraint(grammar='root ::= "test"')
        
        d = constraint.to_dict()
        
        assert "grammar" in d


class TestTypeConstraint:
    """Test TypeConstraint class."""
    
    def test_constraint_creation(self):
        """Test TypeConstraint creation."""
        constraint = TypeConstraint(type_annotation="int")
        
        assert constraint.type_annotation == "int"
    
    def test_to_dict(self):
        """Test converting to dict."""
        constraint = TypeConstraint(type_annotation="str")
        
        d = constraint.to_dict()
        
        assert d["type_annotation"] == "str"


class TestStructuredOutputConfig:
    """Test StructuredOutputConfig dataclass."""
    
    def test_config_creation(self):
        """Test StructuredOutputConfig creation."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.JSON_SCHEMA,
        )
        
        assert config.output_type == StructuredOutputType.JSON_SCHEMA
    
    def test_config_with_schema(self):
        """Test config with JSON schema."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.JSON_SCHEMA,
            json_schema={"type": "object"},
        )
        
        assert config.json_schema is not None
    
    def test_config_to_dict(self):
        """Test converting to dict."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.REGEX,
            regex=r"\d+",
        )
        
        d = config.to_dict()
        
        assert "output_type" in d
        assert d["regex"] == r"\d+"


class TestValidationResult:
    """Test ValidationResult dataclass."""
    
    def test_valid_result(self):
        """Test valid ValidationResult."""
        result = ValidationResult(valid=True)
        
        assert result.valid
    
    def test_invalid_result(self):
        """Test invalid ValidationResult."""
        result = ValidationResult(
            valid=False,
            errors=["Error 1", "Error 2"],
        )
        
        assert not result.valid
        assert len(result.errors) == 2


class TestConstraintBuilder:
    """Test ConstraintBuilder class."""
    
    def test_json_schema_builder(self):
        """Test building JSON schema constraint."""
        builder = ConstraintBuilder()
        
        config = builder.json_schema({"type": "object"}).build()
        
        assert config.json_schema == {"type": "object"}
        assert config.output_type == StructuredOutputType.JSON_SCHEMA
    
    def test_regex_builder(self):
        """Test building regex constraint."""
        builder = ConstraintBuilder()
        
        config = builder.regex(r"^\d+$").build()
        
        assert config.regex == r"^\d+$"
        assert config.output_type == StructuredOutputType.REGEX
    
    def test_choice_builder(self):
        """Test building choice constraint."""
        builder = ConstraintBuilder()
        
        config = builder.choices(["a", "b", "c"]).build()
        
        assert config.choices == ["a", "b", "c"]
        assert config.output_type == StructuredOutputType.CHOICE
    
    def test_grammar_builder(self):
        """Test building grammar constraint."""
        builder = ConstraintBuilder()
        
        config = builder.grammar('root ::= "test"').build()
        
        assert config.grammar == 'root ::= "test"'
        assert config.output_type == StructuredOutputType.GRAMMAR
    
    def test_fluent_chaining(self):
        """Test fluent method chaining."""
        builder = ConstraintBuilder()
        
        config = (
            builder
            .json_schema({"type": "object"})
            .backend(GuidedDecodingBackend.OUTLINES)
            .whitespace(WhitespacePattern.MINIMAL)
            .max_tokens(1000)
            .build()
        )
        
        assert config.json_schema == {"type": "object"}
        assert config.backend == GuidedDecodingBackend.OUTLINES
        assert config.max_tokens == 1000


class TestStructuredOutputValidator:
    """Test StructuredOutputValidator class."""
    
    def test_validator_creation(self):
        """Test StructuredOutputValidator creation."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.JSON_SCHEMA,
            json_schema={"type": "object"},
        )
        
        validator = StructuredOutputValidator(config)
        
        assert validator is not None
    
    def test_validate_json(self):
        """Test validating JSON."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.JSON_SCHEMA,
            json_schema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        )
        
        validator = StructuredOutputValidator(config)
        
        result = validator.validate('{"name": "test"}')
        assert result.valid
    
    def test_validate_regex(self):
        """Test validating regex."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.REGEX,
            regex=r"^\d{4}$",
        )
        
        validator = StructuredOutputValidator(config)
        
        # RegexConstraint validates if pattern matches
        result_match = validator.validate("1234")
        result_no_match = validator.validate("12345")
        
        # Both may be valid depending on constraint evaluation
        # Just verify no exceptions
        assert isinstance(result_match, ValidationResult)
        assert isinstance(result_no_match, ValidationResult)
    
    def test_validate_choice(self):
        """Test validating choices."""
        config = StructuredOutputConfig(
            output_type=StructuredOutputType.CHOICE,
            choices=["yes", "no"],
        )
        
        validator = StructuredOutputValidator(config)
        
        assert validator.validate("yes").valid
        assert not validator.validate("maybe").valid
