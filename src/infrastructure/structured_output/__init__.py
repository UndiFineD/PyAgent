# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Structured Output / Guided Decoding
# Inspired by vLLM's structured output framework

"""
Structured Output Framework for Constrained Generation.

This module provides grammar-based token constraints for:
- JSON Schema validation
- Regex pattern matching
- Grammar specifications (EBNF, Lark)
- Choice constraints
- Function call validation
"""

from src.infrastructure.structured_output.StructuredOutputManager import (
    StructuredOutputManager,
    StructuredOutputBackend,
    StructuredOutputGrammar,
    GrammarType,
    GrammarSpec,
    CompilationResult,
)

from src.infrastructure.structured_output.GrammarEngine import (
    GrammarEngine,
    RegexGrammar,
    JsonSchemaGrammar,
    ChoiceGrammar,
    EBNFGrammar,
    FSMState,
    TokenMask,
)

from src.infrastructure.structured_output.LogitProcessor import (
    LogitProcessor,
    ConstrainedLogitProcessor,
    BitmaskLogitProcessor,
    CompositeLogitProcessor,
    LogitBias,
)

# Phase 41: Enhanced structured output parameters
from src.infrastructure.structured_output.StructuredOutputParams import (
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
    create_json_constraint,
    create_regex_constraint,
    create_choice_constraint,
    combine_constraints,
)

__all__ = [
    # Manager
    "StructuredOutputManager",
    "StructuredOutputBackend",
    "StructuredOutputGrammar",
    "GrammarType",
    "GrammarSpec",
    "CompilationResult",
    # Grammar Engine
    "GrammarEngine",
    "RegexGrammar",
    "JsonSchemaGrammar",
    "ChoiceGrammar",
    "EBNFGrammar",
    "FSMState",
    "TokenMask",
    # Logit Processing
    "LogitProcessor",
    "ConstrainedLogitProcessor",
    "BitmaskLogitProcessor",
    "CompositeLogitProcessor",
    "LogitBias",
    # Phase 41: Enhanced Parameters
    "StructuredOutputType",
    "ConstraintType",
    "SchemaFormat",
    "GuidedDecodingBackend",
    "WhitespacePattern",
    "OutputConstraint",
    "JsonSchemaConstraint",
    "RegexConstraint",
    "ChoiceConstraint",
    "GrammarConstraint",
    "TypeConstraint",
    "StructuredOutputConfig",
    "ValidationResult",
    "ConstraintBuilder",
    "StructuredOutputValidator",
    "create_json_constraint",
    "create_regex_constraint",
    "create_choice_constraint",
    "combine_constraints",
]
