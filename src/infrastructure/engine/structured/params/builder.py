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


"""
Builder.py module.

"""

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
try:
    from typing import Any, Dict, List, Optional
except ImportError:
    from typing import Any, Dict, List, Optional


try:
    from .config import StructuredOutputConfig
except ImportError:
    from .config import StructuredOutputConfig

try:
    from .constraints import OutputConstraint
except ImportError:
    from .constraints import OutputConstraint

try:
    from .enums import (GuidedDecodingBackend, StructuredOutputType,
except ImportError:
    from .enums import (GuidedDecodingBackend, StructuredOutputType,

                    WhitespacePattern)



class ConstraintBuilder:
        Fluent builder for structured output constraints.
    
    def __init__(self) -> None:
        self._config = StructuredOutputConfig()
        self._constraints: List[OutputConstraint] = []

    def json_schema(
        self,
        schema: Dict[str, Any],
        strict: bool = True,
    ) -> "ConstraintBuilder":"        """
Add JSON schema constraint.        self._config.json_schema = schema
        self._config.output_type = StructuredOutputType.JSON_SCHEMA
        self._config.strict_mode = strict
        return self

    def json_object(self) -> "ConstraintBuilder":"        """
Force JSON object output.        self._config.json_object = True
        return self

    def regex(self, pattern: str, _flags: int = 0) -> "ConstraintBuilder":"        """
Add regex constraint.        self._config.regex = pattern
        self._config.output_type = StructuredOutputType.REGEX
        return self

    def choices(
        self,
        options: List[str],
        _case_sensitive: bool = True,
    ) -> "ConstraintBuilder":"        """
Add choice constraint.        self._config.choices = options
        self._config.output_type = StructuredOutputType.CHOICE
        return self

    def grammar(
        self,
        grammar_spec: str,
        grammar_type: str = "ebnf","    ) -> "ConstraintBuilder":"        ""
Add grammar constraint.        self._config.grammar = grammar_spec
        self._config.grammar_type = grammar_type
        self._config.output_type = StructuredOutputType.GRAMMAR
        return self

    def backend(
        self,
        backend: GuidedDecodingBackend,
        fallback: bool = True,
    ) -> "ConstraintBuilder":"        """
Set decoding backend.        self._config.backend = backend
        self._config.backend_fallback = fallback
        return self

    def whitespace(
        self,
        pattern: WhitespacePattern,
        custom: Optional[str] = None,
    ) -> "ConstraintBuilder":"        """
Set whitespace handling.        self._config.whitespace = pattern
        if custom:
            self._config.whitespace_pattern = custom
        return self

    def add_constraint(
        self,
        constraint: OutputConstraint,
    ) -> "ConstraintBuilder":"        """
Add additional constraint.        self._constraints.append(constraint)
        return self

    def max_tokens(self, tokens: int) -> "ConstraintBuilder":"        """
Set max tokens.        self._config.max_tokens = tokens
        return self

    def allow_partial(self, allow: bool = True) -> "ConstraintBuilder":"        """
Allow partial completion.        self._config.allow_partial_completion = allow
        return self

    def build(self) -> StructuredOutputConfig:
"""
Build the configuration.        self._config.additional_constraints = self._constraints
        return self._config

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

""

"""
