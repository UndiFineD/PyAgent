#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
JSON Schema to grammar engine.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from .base import GrammarEngine
from .models import FSMTransitionTable


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
        if schema_type == "array":
            return self._build_array_fsm(schema)
        if schema_type == "string":
            return self._build_string_fsm(schema)
        if schema_type in ("number", "integer"):
            return self._build_number_fsm(schema)
        if schema_type == "boolean":
            return self._build_boolean_fsm()
        if schema_type == "null":
            return self._build_null_fsm()
        return self._build_generic_json_fsm()

    def _build_object_fsm(self, _schema: Dict) -> FSMTransitionTable:
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

    def _build_array_fsm(self, _schema: Dict) -> FSMTransitionTable:
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

    def _build_string_fsm(self, _schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON string."""
        fsm = FSMTransitionTable(num_states=3, initial_state=0, accepting_states=frozenset({2}))
        fsm.add_transition(0, '"', 1)
        fsm.add_transition(0, " ", 0)
        for i in range(32, 127):
            c = chr(i)
            if c == '"':
                fsm.add_transition(1, c, 2)
            elif c == "\\":
                fsm.add_transition(1, c, 1)
            else:
                fsm.add_transition(1, c, 1)
        return fsm

    def _build_number_fsm(self, _schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON number."""
        fsm = FSMTransitionTable(num_states=4, initial_state=0, accepting_states=frozenset({1, 2, 3}))
        fsm.add_transition(0, "-", 0)
        for c in "0123456789":
            fsm.add_transition(0, c, 1)
        for c in "0123456789":
            fsm.add_transition(1, c, 1)
        fsm.add_transition(1, ".", 2)
        fsm.add_transition(1, "e", 3)
        fsm.add_transition(1, "E", 3)
        for c in "0123456789":
            fsm.add_transition(2, c, 2)
        fsm.add_transition(2, "e", 3)
        fsm.add_transition(2, "E", 3)
        fsm.add_transition(3, "+", 3)
        fsm.add_transition(3, "-", 3)
        for c in "0123456789":
            fsm.add_transition(3, c, 3)
        return fsm

    def _build_boolean_fsm(self) -> FSMTransitionTable:
        """Build FSM for JSON boolean."""
        fsm = FSMTransitionTable(num_states=10, initial_state=0, accepting_states=frozenset({4, 9}))
        fsm.add_transition(0, "t", 1)
        fsm.add_transition(1, "r", 2)
        fsm.add_transition(2, "u", 3)
        fsm.add_transition(3, "e", 4)

        fsm.add_transition(0, "f", 5)
        fsm.add_transition(5, "a", 6)
        fsm.add_transition(6, "l", 7)
        fsm.add_transition(7, "s", 8)
        fsm.add_transition(8, "e", 9)
        return fsm

    def _build_null_fsm(self) -> FSMTransitionTable:
        fsm = FSMTransitionTable(num_states=5, initial_state=0, accepting_states=frozenset({4}))
        fsm.add_transition(0, "n", 1)
        fsm.add_transition(1, "u", 2)
        fsm.add_transition(2, "l", 3)
        fsm.add_transition(3, "l", 4)
        return fsm

    def _build_generic_json_fsm(self) -> FSMTransitionTable:
        fsm = FSMTransitionTable(num_states=2, initial_state=0, accepting_states=frozenset({0, 1}))
        for c in self.JSON_CHARS:
            fsm.add_transition(0, c, 0)
            fsm.add_transition(1, c, 1)
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            fsm.add_transition(0, c, 0)
            fsm.add_transition(1, c, 1)
        return fsm
