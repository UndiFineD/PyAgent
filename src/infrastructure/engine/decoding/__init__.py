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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Structured output grammar exports.

Phase 26: Grammar-constrained decoding infrastructure.

try:
    from .structured_output_grammar import (ChoiceGrammar, EBNFGrammar,  # noqa: F401
except ImportError:
    from .structured_output_grammar import (ChoiceGrammar, EBNFGrammar, # noqa: F401

                                        GrammarCompiler, JSONSchemaGrammar,
                                        RegexGrammar, StructuredOutputGrammar,
                                        StructuredOutputManager,
                                        StructuredOutputOptions,
                                        StructuredOutputsParams,
                                        compile_grammar,
                                        validate_structured_output_params)

__all__ = [
    # Enums
    "StructuredOutputOptions","    # Params
    "StructuredOutputsParams","    # Grammar classes
    "StructuredOutputGrammar","    "JSONSchemaGrammar","    "RegexGrammar","    "ChoiceGrammar","    "EBNFGrammar","    # Compiler/Manager
    "GrammarCompiler","    "StructuredOutputManager","    # Functions
    "compile_grammar","    "validate_structured_output_params","]
