# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
StructuredOutputGrammar - Grammar-constrained decoding infrastructure.

Inspired by vLLM's v1/structured_output/ backends (xgrammar, guidance, outlines).
Provides JSON schema, regex, choice, and EBNF grammar constraints for LLM outputs.
"""

from .grammar import (
    ChoiceGrammar,
    EBNFGrammar,
    GrammarCompiler,
    GrammarRule,
    JSONSchemaGrammar,
    RegexGrammar,
    StructuredOutputGrammar,
    StructuredOutputManager,
    StructuredOutputOptions,
    StructuredOutputsParams,
    compile_grammar,
    validate_structured_output_params,
)

__all__ = [
    "StructuredOutputOptions",
    "StructuredOutputsParams",
    "StructuredOutputGrammar",
    "JSONSchemaGrammar",
    "RegexGrammar",
    "ChoiceGrammar",
    "EBNFGrammar",
    "GrammarRule",
    "GrammarCompiler",
    "StructuredOutputManager",
    "compile_grammar",
    "validate_structured_output_params",
]
