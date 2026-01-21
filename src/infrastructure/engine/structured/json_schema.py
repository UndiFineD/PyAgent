# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
JSON Schema to grammar engine.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .models import FSMTransitionTable
from .base import GrammarEngine


class JsonSchemaGrammar(GrammarEngine):
    """
    JSON Schema to grammar conversion.
    """
    
    JSON_CHARS = set('{}[]":,0123456789.-+eEnulltruefalse ')
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._schema_cache: Dict[str, FSMTransitionTable] = {}
    
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from JSON Schema."""
        if spec in self._schema_cache:
            return self._schema_cache[spec]
        
        try:
            schema = json.loads(spec)
            fsm = self._schema_to_fsm(schema)
            self._schema_cache[spec] = fsm
            return fsm
        except json.JSONDecodeError:
            return self._build_generic_json_fsm()
    
    def _schema_to_fsm(self, schema: Dict[str, Any]) -> FSMTransitionTable:
        """Convert JSON Schema to FSM."""
        schema_type = schema.get("type", "any")
        
        if schema_type == "object":
            return self._build_object_fsm(schema)
        elif schema_type == "array":
            return self._build_array_fsm(schema)
        elif schema_type == "string":
            return self._build_string_fsm(schema)
        elif schema_type == "number" or schema_type == "integer":
            return self._build_number_fsm(schema)
        elif schema_type == "boolean":
            return self._build_boolean_fsm()
        elif schema_type == "null":
            return self._build_null_fsm()
        else:
            return self._build_generic_json_fsm()
    
    def _build_object_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON object."""
        fsm = FSMTransitionTable(num_states=7, initial_state=0, accepting_states=frozenset({6}))
        fsm.add_transition(0, "{", 1)
        fsm.add_transition(0, " ", 0)
        fsm.add_transition(1, '"', 2)
        fsm.add_transition(1, "}", 6)
        fsm.add_transition(1, " ", 1)
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
            fsm.add_transition(2, c, 2)
        fsm.add_transition(2, '"', 3)
        fsm.add_transition(3, ":", 4)
        fsm.add_transition(3, " ", 3)
        for c in '"0123456789-ntf{[':
            fsm.add_transition(4, c, 5)
        fsm.add_transition(4, " ", 4)
        fsm.add_transition(5, ",", 1)
        fsm.add_transition(5, "}", 6)
        fsm.add_transition(5, " ", 5)
        return fsm

    def _build_array_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON array."""
        fsm = FSMTransitionTable(num_states=4, initial_state=0, accepting_states=frozenset({3}))
        fsm.add_transition(0, "[", 1)
        fsm.add_transition(0, " ", 0)
        for c in '"0123456789-ntf{[':
            fsm.add_transition(1, c, 2)
        fsm.add_transition(1, "]", 3)
        fsm.add_transition(1, " ", 1)
        fsm.add_transition(2, ",", 1)
        fsm.add_transition(2, "]", 3)
        fsm.add_transition(2, " ", 2)
        return fsm

    def _build_string_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON string."""
        fsm = FSMTransitionTable(num_states=3, initial_state=0, accepting_states=frozenset({2}))
        fsm.add_transition(0, '"', 1)
        fsm.add_transition(0, " ", 0)
        for i in range(32, 127):
            c = chr(i)
            if c == '"': fsm.add_transition(1, c, 2)
            elif c == '\\': fsm.add_transition(1, c, 1)
            else: fsm.add_transition(1, c, 1)
        return fsm

    def _build_number_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON number."""
        fsm = FSMTransitionTable(num_states=4, initial_state=0, accepting_states=frozenset({1, 2, 3}))
        fsm.add_transition(0, "-", 0)
        for c in "0123456789": fsm.add_transition(0, c, 1)
        for c in "0123456789": fsm.add_transition(1, c, 1)
        fsm.add_transition(1, ".", 2)
        fsm.add_transition(1, "e", 3)
        fsm.add_transition(1, "E", 3)
        for c in "0123456789": fsm.add_transition(2, c, 2)
        fsm.add_transition(2, "e", 3)
        fsm.add_transition(2, "E", 3)
        fsm.add_transition(3, "+", 3)
        fsm.add_transition(3, "-", 3)
        for c in "0123456789": fsm.add_transition(3, c, 3)
        return fsm

    def _build_boolean_fsm(self) -> FSMTransitionTable:
        """Build FSM for JSON boolean."""
        fsm = FSMTransitionTable(num_states=10, initial_state=0, accepting_states=frozenset({4, 9}))
        fsm.add_transition(0, "t", 1); fsm.add_transition(1, "r", 2); fsm.add_transition(2, "u", 3); fsm.add_transition(3, "e", 4)
        fsm.add_transition(0, "f", 5); fsm.add_transition(5, "a", 6); fsm.add_transition(6, "l", 7); fsm.add_transition(7, "s", 8); fsm.add_transition(8, "e", 9)
        return fsm

    def _build_null_fsm(self) -> FSMTransitionTable:
        fsm = FSMTransitionTable(num_states=5, initial_state=0, accepting_states=frozenset({4}))
        fsm.add_transition(0, "n", 1); fsm.add_transition(1, "u", 2); fsm.add_transition(2, "l", 3); fsm.add_transition(3, "l", 4)
        return fsm

    def _build_generic_json_fsm(self) -> FSMTransitionTable:
        fsm = FSMTransitionTable(num_states=2, initial_state=0, accepting_states=frozenset({0, 1}))
        for c in self.JSON_CHARS:
            fsm.add_transition(0, c, 0); fsm.add_transition(1, c, 1)
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            fsm.add_transition(0, c, 0); fsm.add_transition(1, c, 1)
        return fsm
