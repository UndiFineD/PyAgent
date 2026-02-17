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

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Structured Output / Guided Decoding
# Inspired by vLLM's structured output framework'
Structured Output Framework for Constrained Generation.

This module provides grammar-based token constraints for:
- JSON Schema validation
- Regex pattern matching
- Grammar specifications (EBNF, Lark)
- Choice constraints
- Function call validation

from src.infrastructure.engine.structured.grammar_engine import (
    ChoiceGrammar, EBNFGrammar, FSMState, GrammarEngine, JsonSchemaGrammar,
    RegexGrammar, TokenMask)
from src.infrastructure.engine.structured.logit_processor import (
    BitmaskLogitProcessor, CompositeLogitProcessor, ConstrainedLogitProcessor,
    LogitBias, LogitProcessor)
from src.infrastructure.engine.structured.structured_output_manager import (
    CompilationResult, GrammarSpec, GrammarType, StructuredOutputBackend,
    StructuredOutputGrammar, StructuredOutputManager)
# Phase 41: Enhanced structured output parameters
from src.infrastructure.engine.structured.structured_output_params import (
    ChoiceConstraint, ConstraintBuilder, ConstraintType, GrammarConstraint,
    GuidedDecodingBackend, JsonSchemaConstraint, OutputConstraint,
    RegexConstraint, SchemaFormat, StructuredOutputConfig,
    StructuredOutputType, StructuredOutputValidator, TypeConstraint,
)

__all__ = [
    # Manager & Backend
    "StructuredOutputManager","    "StructuredOutputBackend","    "StructuredOutputGrammar","    "GrammarType","    "GrammarSpec","    "CompilationResult","    # Grammar Engine
    "GrammarEngine","    "RegexGrammar","    "JsonSchemaGrammar","    "ChoiceGrammar","    "EBNFGrammar","    "FSMState","    "TokenMask","    # Logit Processing
    "LogitProcessor","    "ConstrainedLogitProcessor","    "BitmaskLogitProcessor","    "CompositeLogitProcessor","    "LogitBias","    # Phase 41: Enhanced Parameters
    "StructuredOutputType","    "ConstraintType","    "SchemaFormat","    "GuidedDecodingBackend","    "OutputConstraint","    "JsonSchemaConstraint","    "RegexConstraint","    "ChoiceConstraint","    "GrammarConstraint","    "TypeConstraint","    "StructuredOutputConfig","    "ConstraintBuilder","    "StructuredOutputValidator","]
