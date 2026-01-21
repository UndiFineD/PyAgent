# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Backend selection and dispatching logic for structured output grammars.
"""

from __future__ import annotations

import json
import logging
import re
from typing import (
    Callable,
    Dict,
    List,
    Optional,
)

import numpy as np

from .base import (
    StructuredOutputGrammar,
    StructuredOutputOptions,
    StructuredOutputsParams,
)
from .ebnf_grammar import EBNFGrammar
from .json_constraint import JSONSchemaGrammar
from .regex_constraint import ChoiceGrammar, RegexGrammar

logger = logging.getLogger(__name__)


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
        elif not params.choice:
            errors.append("Choice list cannot be empty")
    
    if params.grammar is not None:
        if not isinstance(params.grammar, str):
            errors.append("Grammar must be a string")
        elif "::=" not in params.grammar:
            errors.append("Grammar must contain at least one rule (::=)")
    
    return errors
