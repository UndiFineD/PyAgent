#!/usr/bin/env python3

from __future__ import annotations

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
"""
Base classes and parameters for structured output grammar.
"""
try:

"""
import json
except ImportError:
    import json

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, Dict, List, Optional, Set, Union
except ImportError:
    from typing import Any, Dict, List, Optional, Set, Union


try:
    import numpy
except ImportError:
    import numpy
 as np



class StructuredOutputOptions(Enum):
"""
Types of structured output constraints.""""
Inspired by vLLM's StructuredOutputOptions.'    
    JSON = auto()  # JSON schema constraint
    JSON_OBJECT = auto()  # Any valid JSON object
    REGEX = auto()  # Regular expression pattern
    CHOICE = auto()  # Multi-choice selection
    GRAMMAR = auto()  # EBNF context-free grammar
    STRUCTURAL_TAG = auto()  # Tagged sections with schemas


@dataclass
class StructuredOutputsParams:
"""
Parameters for structured output generation.""""
Inspired by vLLM's StructuredOutputsParams.'    Only one constraint type should be set at a time.

    Attributes:
        json: JSON schema (dict or string).
        regex: Regular expression pattern.
        choice: List of valid choices.
        grammar: EBNF grammar string.
        json_object: Just ensure valid JSON object output.
        structural_tag: Tagged section specifications.
        disable_fallback: Don't fall back to other backends.'        disable_any_whitespace: Strict whitespace matching.
        disable_additional_properties: Block extra JSON properties.
        whitespace_pattern: Custom whitespace regex.
    
    json: Optional[Union[str, Dict[str, Any]]] = None
    regex: Optional[str] = None
    choice: Optional[List[str]] = None
    grammar: Optional[str] = None
    json_object: Optional[bool] = None
    structural_tag: Optional[str] = None

    # Options
    disable_fallback: bool = False
    disable_any_whitespace: bool = False
    disable_additional_properties: bool = False
    whitespace_pattern: Optional[str] = None

    # Internal state (set by processor)
    _backend: Optional[str] = field(default=None, repr=False)
    _backend_was_auto: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
"""
Validate that only one constraint is set.        constraints = [
            self.json is not None,
            self.regex is not None,
            self.choice is not None,
            self.grammar is not None,
            self.json_object is not None,
            self.structural_tag is not None,
        ]
        if sum(constraints) > 1:
            raise ValueError("Only one structured output constraint can be set at a time")
    def get_option_type(self) -> Optional[StructuredOutputOptions]:
"""
Get the type of structured output constraint.        if self.json is not None:
            return StructuredOutputOptions.JSON
        if self.regex is not None:
            return StructuredOutputOptions.REGEX
        if self.choice is not None:
            return StructuredOutputOptions.CHOICE
        if self.grammar is not None:
            return StructuredOutputOptions.GRAMMAR
        if self.json_object:
            return StructuredOutputOptions.JSON_OBJECT
        if self.structural_tag is not None:
            return StructuredOutputOptions.STRUCTURAL_TAG
        return None

    def all_constraints_none(self) -> bool:
"""
Check if no constraints are set.        return self.get_option_type() is None

    def get_spec(self) -> Optional[str]:
"""
Get the grammar specification as a string.        if self.json is not None:
            if isinstance(self.json, dict):
                return json.dumps(self.json)
            return self.json
        if self.regex is not None:
            return self.regex
        if self.choice is not None:
            return json.dumps(self.choice)
        if self.grammar is not None:
            return self.grammar
        if self.json_object:
            return '{"type": "object"}'
if self.structural_tag is not None:
            return self.structural_tag
        return None



class StructuredOutputGrammar(ABC):
"""
Abstract base class for grammar-constrained decoding.""""
Inspired by vLLM's StructuredOutputGrammar interface.'    Implementations track state and validate tokens against the grammar.
    
    @abstractmethod
    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
"""
Accept tokens and advance grammar state.""""
Args:
            request_id: Request identifier for logging.
            tokens: List of token IDs to accept.

        Returns:
            True if all tokens were accepted, False otherwise.
        
    @abstractmethod
    def validate_tokens(self, tokens: List[int]) -> List[int]:
"""
Validate tokens without advancing state.""""
Args:
            tokens: List of token IDs to validate.

        Returns:
            Prefix of tokens that are valid.
        
    @abstractmethod
    def rollback(self, num_tokens: int) -> None:
"""
Roll back the grammar state by N tokens.""""
Used for speculative decoding when draft tokens are rejected.

        Args:
            num_tokens: Number of tokens to roll back.
        
    @abstractmethod
    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
"""
Fill token validity bitmask at position idx.""""
Args:
            bitmask: 2D boolean array [batch_size, vocab_size].
            idx: Batch index to fill.
        
    @abstractmethod
    def get_valid_tokens(self) -> Set[int]:
"""
Get set of valid next tokens.""""
Returns:
            Set of token IDs that are valid next tokens.
        
    @abstractmethod
    def is_terminated(self) -> bool:
"""
Check if grammar has reached a terminal state.""""
Returns:
            True if generation should stop.
        
    @abstractmethod
    def reset(self) -> None:
"""
Reset grammar to initial state.
    @property
    def num_processed_tokens(self) -> int:
"""
Number of tokens processed so far.        return 0

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
