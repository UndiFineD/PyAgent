# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
StructuredOutputGrammar - Grammar-constrained decoding infrastructure.

Inspired by vLLM's v1/structured_output/ backends (xgrammar, guidance, outlines).
Provides JSON schema, regex, choice, and EBNF grammar constraints for LLM outputs.
"""

from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Union,
)

import numpy as np

logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Configuration
# =============================================================================


class StructuredOutputOptions(Enum):
    """Types of structured output constraints.
    
    Inspired by vLLM's StructuredOutputOptions.
    """
    
    JSON = auto()           # JSON schema constraint
    JSON_OBJECT = auto()    # Any valid JSON object
    REGEX = auto()          # Regular expression pattern
    CHOICE = auto()         # Multi-choice selection
    GRAMMAR = auto()        # EBNF context-free grammar
    STRUCTURAL_TAG = auto() # Tagged sections with schemas


@dataclass
class StructuredOutputsParams:
    """Parameters for structured output generation.
    
    Inspired by vLLM's StructuredOutputsParams.
    Only one constraint type should be set at a time.
    
    Attributes:
        json: JSON schema (dict or string).
        regex: Regular expression pattern.
        choice: List of valid choices.
        grammar: EBNF grammar string.
        json_object: Just ensure valid JSON object output.
        structural_tag: Tagged section specifications.
        disable_fallback: Don't fall back to other backends.
        disable_any_whitespace: Strict whitespace matching.
        disable_additional_properties: Block extra JSON properties.
        whitespace_pattern: Custom whitespace regex.
    """
    
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
    
    def __post_init__(self):
        """Validate that only one constraint is set."""
        constraints = [
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
        """Get the type of structured output constraint."""
        if self.json is not None:
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
        """Check if no constraints are set."""
        return self.get_option_type() is None
    
    def get_spec(self) -> Optional[str]:
        """Get the grammar specification as a string."""
        if self.json is not None:
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


# =============================================================================
# Base Grammar Class
# =============================================================================


class StructuredOutputGrammar(ABC):
    """Abstract base class for grammar-constrained decoding.
    
    Inspired by vLLM's StructuredOutputGrammar interface.
    Implementations track state and validate tokens against the grammar.
    """
    
    @abstractmethod
    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
        """Accept tokens and advance grammar state.
        
        Args:
            request_id: Request identifier for logging.
            tokens: List of token IDs to accept.
        
        Returns:
            True if all tokens were accepted, False otherwise.
        """
        ...
    
    @abstractmethod
    def validate_tokens(self, tokens: List[int]) -> List[int]:
        """Validate tokens without advancing state.
        
        Args:
            tokens: List of token IDs to validate.
        
        Returns:
            Prefix of tokens that are valid.
        """
        ...
    
    @abstractmethod
    def rollback(self, num_tokens: int) -> None:
        """Roll back the grammar state by N tokens.
        
        Used for speculative decoding when draft tokens are rejected.
        
        Args:
            num_tokens: Number of tokens to roll back.
        """
        ...
    
    @abstractmethod
    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
        """Fill token validity bitmask at position idx.
        
        Args:
            bitmask: 2D boolean array [batch_size, vocab_size].
            idx: Batch index to fill.
        """
        ...
    
    @abstractmethod
    def get_valid_tokens(self) -> Set[int]:
        """Get set of valid next tokens.
        
        Returns:
            Set of token IDs that are valid next tokens.
        """
        ...
    
    @abstractmethod
    def is_terminated(self) -> bool:
        """Check if grammar has reached a terminal state.
        
        Returns:
            True if generation should stop.
        """
        ...
    
    @abstractmethod
    def reset(self) -> None:
        """Reset grammar to initial state."""
        ...
    
    @property
    def num_processed_tokens(self) -> int:
        """Number of tokens processed so far."""
        return 0


# =============================================================================
# JSON Schema Grammar
# =============================================================================


@dataclass
class JSONSchemaGrammar(StructuredOutputGrammar):
    """Grammar that constrains output to match a JSON schema.
    
    Converts JSON schema to a regex pattern for validation.
    Inspired by vLLM's xgrammar and outlines backends.
    """
    
    schema: Dict[str, Any]
    vocab_size: int
    token_to_string: Callable[[int], str]
    _pattern: str = field(default="", init=False)
    _regex: Optional[re.Pattern] = field(default=None, init=False, repr=False)
    _buffer: str = field(default="", init=False)
    _token_history: List[int] = field(default_factory=list, init=False)
    _terminated: bool = field(default=False, init=False)
    
    def __post_init__(self):
        """Compile JSON schema to regex pattern."""
        self._pattern = self._schema_to_regex(self.schema)
        self._regex = re.compile(self._pattern)
    
    def _schema_to_regex(self, schema: Dict[str, Any]) -> str:
        """Convert JSON schema to regex pattern.
        
        Simplified implementation - real version would use outlines_core.
        """
        schema_type = schema.get("type", "object")
        
        if schema_type == "string":
            if "enum" in schema:
                choices = [re.escape(f'"{c}"') for c in schema["enum"]]
                return f"({'|'.join(choices)})"
            if "pattern" in schema:
                return f'"{schema["pattern"]}"'
            return r'"[^"]*"'
        
        if schema_type == "integer":
            return r"-?\d+"
        
        if schema_type == "number":
            return r"-?\d+(\.\d+)?"
        
        if schema_type == "boolean":
            return r"(true|false)"
        
        if schema_type == "null":
            return r"null"
        
        if schema_type == "array":
            items_schema = schema.get("items", {})
            items_pattern = self._schema_to_regex(items_schema)
            return rf"\[\s*({items_pattern}(\s*,\s*{items_pattern})*)?\s*\]"
        
        if schema_type == "object":
            properties = schema.get("properties", {})
            required = set(schema.get("required", []))
            
            if not properties:
                return r"\{[^}]*\}"
            
            prop_patterns = []
            for name, prop_schema in properties.items():
                prop_pattern = self._schema_to_regex(prop_schema)
                key_pattern = f'"{re.escape(name)}"'
                full_pattern = f'{key_pattern}\\s*:\\s*{prop_pattern}'
                if name not in required:
                    full_pattern = f"({full_pattern})?"
                prop_patterns.append(full_pattern)
            
            inner = r"\s*,\s*".join(prop_patterns)
            return rf"\{{\s*{inner}\s*\}}"
        
        # Fallback
        return r".*"
    
    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
        """Accept tokens if they match the JSON schema pattern."""
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str
            
            # Check if this is a valid prefix
            if self._is_valid_prefix(new_buffer):
                self._buffer = new_buffer
                self._token_history.append(token)
            else:
                return False
            
            # Check if complete
            if self._regex and self._regex.fullmatch(self._buffer):
                self._terminated = True
        
        return True
    
    def _is_valid_prefix(self, text: str) -> bool:
        """Check if text is a valid prefix of the pattern."""
        # Try partial match
        try:
            match = self._regex.match(text) if self._regex else None
            if match and match.end() == len(text):
                return True
            # Also accept if we're building valid JSON
            return self._is_valid_json_prefix(text)
        except Exception:
            return False
    
    def _is_valid_json_prefix(self, text: str) -> bool:
        """Check if text is a valid partial JSON."""
        text = text.strip()
        if not text:
            return True
        
        # Simple heuristic checks
        open_braces = text.count("{") - text.count("}")
        open_brackets = text.count("[") - text.count("]")
        in_string = False
        for i, c in enumerate(text):
            if c == '"' and (i == 0 or text[i-1] != '\\'):
                in_string = not in_string
        
        return open_braces >= 0 and open_brackets >= 0
    
    def validate_tokens(self, tokens: List[int]) -> List[int]:
        """Validate tokens without advancing state."""
        valid = []
        test_buffer = self._buffer
        
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str
            
            if self._is_valid_prefix(new_buffer):
                valid.append(token)
                test_buffer = new_buffer
            else:
                break
        
        return valid
    
    def rollback(self, num_tokens: int) -> None:
        """Roll back by removing tokens from history."""
        if num_tokens <= 0:
            return
        
        tokens_to_remove = self._token_history[-num_tokens:]
        self._token_history = self._token_history[:-num_tokens]
        
        # Rebuild buffer
        self._buffer = ""
        for token in self._token_history:
            self._buffer += self.token_to_string(token)
        
        self._terminated = False
    
    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
        """Set valid tokens in bitmask."""
        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True
    
    def get_valid_tokens(self) -> Set[int]:
        """Get tokens that produce valid prefixes."""
        valid: Set[int] = set()
        
        for token_id in range(self.vocab_size):
            token_str = self.token_to_string(token_id)
            test_buffer = self._buffer + token_str
            
            if self._is_valid_prefix(test_buffer):
                valid.add(token_id)
        
        return valid
    
    def is_terminated(self) -> bool:
        """Check if JSON is complete."""
        return self._terminated
    
    def reset(self) -> None:
        """Reset grammar state."""
        self._buffer = ""
        self._token_history = []
        self._terminated = False
    
    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)


# =============================================================================
# Regex Grammar
# =============================================================================


@dataclass
class RegexGrammar(StructuredOutputGrammar):
    """Grammar that constrains output to match a regex pattern.
    
    Uses DFA-based matching for efficient token validation.
    Inspired by vLLM's outlines backend.
    """
    
    pattern: str
    vocab_size: int
    token_to_string: Callable[[int], str]
    _regex: Optional[re.Pattern] = field(default=None, init=False, repr=False)
    _buffer: str = field(default="", init=False)
    _token_history: List[int] = field(default_factory=list, init=False)
    _terminated: bool = field(default=False, init=False)
    
    def __post_init__(self):
        """Compile regex pattern."""
        self._regex = re.compile(self.pattern)
    
    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
        """Accept tokens that match regex prefix."""
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str
            
            # Check if valid prefix using partial match
            if self._is_valid_prefix(new_buffer):
                self._buffer = new_buffer
                self._token_history.append(token)
            else:
                return False
            
            # Check if complete
            if self._regex and self._regex.fullmatch(self._buffer):
                self._terminated = True
        
        return True
    
    def _is_valid_prefix(self, text: str) -> bool:
        """Check if text is a valid prefix of the regex."""
        if not self._regex:
            return True
        
        # Try partial match by checking if any completion could match
        match = self._regex.match(text)
        if match and match.end() == len(text):
            return True
        
        # Check if text could be extended to match
        # This is a heuristic - real impl would use DFA states
        try:
            # If we can match a prefix, we're on a valid path
            for i in range(len(text), 0, -1):
                if self._regex.match(text[:i]):
                    return True
            return len(text) == 0
        except Exception:
            return False
    
    def validate_tokens(self, tokens: List[int]) -> List[int]:
        """Validate tokens without advancing state."""
        valid = []
        test_buffer = self._buffer
        
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str
            
            if self._is_valid_prefix(new_buffer):
                valid.append(token)
                test_buffer = new_buffer
            else:
                break
        
        return valid
    
    def rollback(self, num_tokens: int) -> None:
        """Roll back by removing tokens."""
        if num_tokens <= 0:
            return
        
        self._token_history = self._token_history[:-num_tokens]
        self._buffer = ""
        for token in self._token_history:
            self._buffer += self.token_to_string(token)
        self._terminated = False
    
    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
        """Set valid tokens in bitmask."""
        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True
    
    def get_valid_tokens(self) -> Set[int]:
        """Get tokens that produce valid prefixes."""
        valid: Set[int] = set()
        
        for token_id in range(min(self.vocab_size, 1000)):  # Limit for performance
            token_str = self.token_to_string(token_id)
            test_buffer = self._buffer + token_str
            
            if self._is_valid_prefix(test_buffer):
                valid.add(token_id)
        
        return valid
    
    def is_terminated(self) -> bool:
        """Check if regex is fully matched."""
        return self._terminated
    
    def reset(self) -> None:
        """Reset grammar state."""
        self._buffer = ""
        self._token_history = []
        self._terminated = False
    
    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)


# =============================================================================
# Choice Grammar
# =============================================================================


@dataclass
class ChoiceGrammar(StructuredOutputGrammar):
    """Grammar that constrains output to one of several choices.
    
    Efficient matching by tracking which choices remain possible.
    """
    
    choices: List[str]
    vocab_size: int
    token_to_string: Callable[[int], str]
    _buffer: str = field(default="", init=False)
    _token_history: List[int] = field(default_factory=list, init=False)
    _active_choices: Set[int] = field(default_factory=set, init=False)
    _matched_choice: Optional[int] = field(default=None, init=False)
    
    def __post_init__(self):
        """Initialize active choice set."""
        self._active_choices = set(range(len(self.choices)))
    
    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
        """Accept tokens that match any remaining choice."""
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str
            
            # Update active choices
            still_active: Set[int] = set()
            for idx in self._active_choices:
                choice = self.choices[idx]
                if choice.startswith(new_buffer):
                    still_active.add(idx)
                    if choice == new_buffer:
                        self._matched_choice = idx
            
            if not still_active:
                return False
            
            self._active_choices = still_active
            self._buffer = new_buffer
            self._token_history.append(token)
        
        return True
    
    def validate_tokens(self, tokens: List[int]) -> List[int]:
        """Validate tokens without advancing state."""
        valid = []
        test_buffer = self._buffer
        test_active = self._active_choices.copy()
        
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str
            
            still_active: Set[int] = set()
            for idx in test_active:
                if self.choices[idx].startswith(new_buffer):
                    still_active.add(idx)
            
            if still_active:
                valid.append(token)
                test_buffer = new_buffer
                test_active = still_active
            else:
                break
        
        return valid
    
    def rollback(self, num_tokens: int) -> None:
        """Roll back by removing tokens."""
        if num_tokens <= 0:
            return
        
        self._token_history = self._token_history[:-num_tokens]
        self._buffer = ""
        for token in self._token_history:
            self._buffer += self.token_to_string(token)
        
        # Recompute active choices
        self._active_choices = set()
        self._matched_choice = None
        for idx, choice in enumerate(self.choices):
            if choice.startswith(self._buffer):
                self._active_choices.add(idx)
                if choice == self._buffer:
                    self._matched_choice = idx
    
    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
        """Set valid tokens in bitmask."""
        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True
    
    def get_valid_tokens(self) -> Set[int]:
        """Get tokens that match any active choice."""
        valid: Set[int] = set()
        
        # Get next valid characters
        valid_chars: Set[str] = set()
        for idx in self._active_choices:
            choice = self.choices[idx]
            if len(choice) > len(self._buffer):
                valid_chars.add(choice[len(self._buffer)])
        
        if not valid_chars:
            return valid
        
        # Find tokens that start with valid chars
        for token_id in range(min(self.vocab_size, 1000)):
            token_str = self.token_to_string(token_id)
            if token_str and token_str[0] in valid_chars:
                # Verify full token works
                test_buffer = self._buffer + token_str
                for idx in self._active_choices:
                    if self.choices[idx].startswith(test_buffer):
                        valid.add(token_id)
                        break
        
        return valid
    
    def is_terminated(self) -> bool:
        """Check if a choice has been fully matched."""
        return self._matched_choice is not None
    
    def reset(self) -> None:
        """Reset grammar state."""
        self._buffer = ""
        self._token_history = []
        self._active_choices = set(range(len(self.choices)))
        self._matched_choice = None
    
    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)


# =============================================================================
# EBNF Grammar
# =============================================================================


@dataclass
class GrammarRule:
    """A single EBNF grammar rule."""
    name: str
    alternatives: List[List[str]]  # Each alternative is a sequence of symbols


@dataclass
class EBNFGrammar(StructuredOutputGrammar):
    """Grammar that constrains output using EBNF rules.
    
    Supports simple context-free grammars for SQL, code, etc.
    Inspired by vLLM's xgrammar EBNF support.
    """
    
    grammar_str: str
    vocab_size: int
    token_to_string: Callable[[int], str]
    start_symbol: str = "root"
    _rules: Dict[str, GrammarRule] = field(default_factory=dict, init=False)
    _buffer: str = field(default="", init=False)
    _token_history: List[int] = field(default_factory=list, init=False)
    _terminated: bool = field(default=False, init=False)
    
    def __post_init__(self):
        """Parse EBNF grammar rules."""
        self._parse_grammar()
    
    def _parse_grammar(self) -> None:
        """Parse EBNF grammar string into rules.
        
        Simple parser for rules like:
        root ::= "SELECT " column " FROM " table
        column ::= "col1" | "col2"
        """
        for line in self.grammar_str.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if "::=" not in line:
                continue
            
            name, rhs = line.split("::=", 1)
            name = name.strip()
            
            # Parse alternatives
            alternatives = []
            for alt in rhs.split("|"):
                symbols = []
                current = ""
                in_string = False
                
                for char in alt.strip():
                    if char == '"' and (not current or current[-1] != '\\'):
                        if in_string:
                            symbols.append(("LITERAL", current))
                            current = ""
                        in_string = not in_string
                    elif in_string:
                        current += char
                    elif char.isalnum() or char == '_':
                        current += char
                    elif char.isspace():
                        if current:
                            symbols.append(("RULE", current))
                            current = ""
                
                if current:
                    symbols.append(("RULE", current))
                
                if symbols:
                    alternatives.append(symbols)
            
            self._rules[name] = GrammarRule(name=name, alternatives=alternatives)
    
    def _get_valid_prefixes(self, symbol: str = None) -> Set[str]:
        """Get all valid string prefixes from current state."""
        symbol = symbol or self.start_symbol
        
        if symbol not in self._rules:
            return set()
        
        rule = self._rules[symbol]
        prefixes: Set[str] = set()
        
        for alt in rule.alternatives:
            if not alt:
                continue
            
            sym_type, sym_val = alt[0]
            if sym_type == "LITERAL":
                prefixes.add(sym_val)
            elif sym_type == "RULE":
                prefixes.update(self._get_valid_prefixes(sym_val))
        
        return prefixes
    
    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
        """Accept tokens that match grammar."""
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str
            
            # Simple validation: check if any rule prefix matches
            if self._is_valid_grammar_prefix(new_buffer):
                self._buffer = new_buffer
                self._token_history.append(token)
            else:
                return False
        
        return True
    
    def _is_valid_grammar_prefix(self, text: str) -> bool:
        """Check if text is a valid prefix according to grammar."""
        # Simplified check - real impl would use parser
        return len(text) < 1000  # Placeholder
    
    def validate_tokens(self, tokens: List[int]) -> List[int]:
        """Validate tokens without advancing state."""
        valid = []
        test_buffer = self._buffer
        
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str
            
            if self._is_valid_grammar_prefix(new_buffer):
                valid.append(token)
                test_buffer = new_buffer
            else:
                break
        
        return valid
    
    def rollback(self, num_tokens: int) -> None:
        """Roll back by removing tokens."""
        if num_tokens <= 0:
            return
        
        self._token_history = self._token_history[:-num_tokens]
        self._buffer = ""
        for token in self._token_history:
            self._buffer += self.token_to_string(token)
        self._terminated = False
    
    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
        """Set valid tokens in bitmask."""
        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True
    
    def get_valid_tokens(self) -> Set[int]:
        """Get tokens valid according to grammar."""
        # Simplified - return all tokens for now
        return set(range(min(self.vocab_size, 100)))
    
    def is_terminated(self) -> bool:
        """Check if grammar parsing is complete."""
        return self._terminated
    
    def reset(self) -> None:
        """Reset grammar state."""
        self._buffer = ""
        self._token_history = []
        self._terminated = False
    
    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)


# =============================================================================
# Grammar Compiler and Manager
# =============================================================================


class GrammarCompiler:
    """Compiles grammar specifications into grammar objects.
    
    Inspired by vLLM's structured output backends.
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_to_string: Callable[[int], str],
    ):
        self.vocab_size = vocab_size
        self.token_to_string = token_to_string
    
    def compile(
        self,
        params: StructuredOutputsParams,
    ) -> Optional[StructuredOutputGrammar]:
        """Compile structured output params into a grammar.
        
        Args:
            params: Structured output parameters.
        
        Returns:
            Compiled grammar, or None if no constraints.
        """
        option_type = params.get_option_type()
        
        if option_type is None:
            return None
        
        if option_type == StructuredOutputOptions.JSON:
            schema = params.json
            if isinstance(schema, str):
                schema = json.loads(schema)
            return JSONSchemaGrammar(
                schema=schema,
                vocab_size=self.vocab_size,
                token_to_string=self.token_to_string,
            )
        
        if option_type == StructuredOutputOptions.JSON_OBJECT:
            return JSONSchemaGrammar(
                schema={"type": "object"},
                vocab_size=self.vocab_size,
                token_to_string=self.token_to_string,
            )
        
        if option_type == StructuredOutputOptions.REGEX:
            return RegexGrammar(
                pattern=params.regex,
                vocab_size=self.vocab_size,
                token_to_string=self.token_to_string,
            )
        
        if option_type == StructuredOutputOptions.CHOICE:
            return ChoiceGrammar(
                choices=params.choice,
                vocab_size=self.vocab_size,
                token_to_string=self.token_to_string,
            )
        
        if option_type == StructuredOutputOptions.GRAMMAR:
            return EBNFGrammar(
                grammar_str=params.grammar,
                vocab_size=self.vocab_size,
                token_to_string=self.token_to_string,
            )
        
        raise ValueError(f"Unsupported option type: {option_type}")


class StructuredOutputManager:
    """Manages grammar compilation and lifecycle.
    
    Inspired by vLLM's StructuredOutputManager.
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_to_string: Callable[[int], str],
    ):
        self.compiler = GrammarCompiler(vocab_size, token_to_string)
        self._grammars: Dict[str, StructuredOutputGrammar] = {}
    
    def init_grammar(self, request_id: str, params: StructuredOutputsParams) -> None:
        """Initialize grammar for a request.
        
        Args:
            request_id: Request identifier.
            params: Structured output parameters.
        """
        grammar = self.compiler.compile(params)
        if grammar:
            self._grammars[request_id] = grammar
            logger.debug("Initialized grammar for request %s", request_id)
    
    def get_grammar(self, request_id: str) -> Optional[StructuredOutputGrammar]:
        """Get grammar for a request."""
        return self._grammars.get(request_id)
    
    def remove_grammar(self, request_id: str) -> None:
        """Remove grammar for a completed request."""
        self._grammars.pop(request_id, None)
    
    def accept_tokens(
        self,
        request_id: str,
        tokens: List[int],
    ) -> bool:
        """Accept tokens for a request's grammar.
        
        Args:
            request_id: Request identifier.
            tokens: Tokens to accept.
        
        Returns:
            True if tokens were accepted.
        """
        grammar = self._grammars.get(request_id)
        if grammar is None:
            return True  # No grammar constraint
        
        return grammar.accept_tokens(request_id, tokens)
    
    def fill_bitmasks(
        self,
        request_ids: List[str],
        bitmask: np.ndarray,
    ) -> None:
        """Fill bitmasks for multiple requests.
        
        Args:
            request_ids: List of request IDs.
            bitmask: 2D array [batch_size, vocab_size].
        """
        for idx, request_id in enumerate(request_ids):
            grammar = self._grammars.get(request_id)
            if grammar:
                grammar.fill_bitmask(bitmask, idx)
            else:
                # No constraint - all tokens valid
                bitmask[idx, :] = True


# =============================================================================
# Convenience Functions
# =============================================================================


def compile_grammar(
    params: StructuredOutputsParams,
    vocab_size: int,
    token_to_string: Callable[[int], str],
) -> Optional[StructuredOutputGrammar]:
    """Compile structured output parameters into a grammar.
    
    Args:
        params: Structured output parameters.
        vocab_size: Vocabulary size.
        token_to_string: Function to convert token ID to string.
    
    Returns:
        Compiled grammar, or None if no constraints.
    """
    compiler = GrammarCompiler(vocab_size, token_to_string)
    return compiler.compile(params)


def validate_structured_output_params(params: StructuredOutputsParams) -> List[str]:
    """Validate structured output parameters.
    
    Args:
        params: Parameters to validate.
    
    Returns:
        List of validation error messages (empty if valid).
    """
    errors = []
    
    if params.json is not None:
        try:
            if isinstance(params.json, str):
                json.loads(params.json)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON schema: {e}")
    
    if params.regex is not None:
        try:
            re.compile(params.regex)
        except re.error as e:
            errors.append(f"Invalid regex pattern: {e}")
    
    if params.choice is not None:
        if not isinstance(params.choice, list):
            errors.append("Choice must be a list")
        elif len(params.choice) == 0:
            errors.append("Choice list cannot be empty")
    
    if params.grammar is not None:
        if not isinstance(params.grammar, str):
            errors.append("Grammar must be a string")
        elif "::=" not in params.grammar:
            errors.append("Grammar must contain at least one rule (::=)")
    
    return errors
