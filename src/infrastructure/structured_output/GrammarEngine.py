# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Grammar Engine for Structured Output
# Inspired by vLLM's structured output backends

"""
GrammarEngine: FSM-based grammar constraint engine.

Provides:
- Regex to FSM compilation
- JSON Schema to grammar conversion
- EBNF grammar support
- Token-level constraint masks
"""

from __future__ import annotations

import json
import re
import sys
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, FrozenSet, List, Optional, Set, Tuple, Union
import numpy as np

# Handle sre_parse deprecation in Python 3.11+
# sre_parse moved to re._parser in 3.11 and will be removed in 3.13
if sys.version_info >= (3, 11):
    try:
        # Python 3.11+ uses re._parser
        import re._parser as _sre_parse
    except ImportError:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            import sre_parse as _sre_parse
else:
    import sre_parse as _sre_parse


# =============================================================================
# FSM State Management
# =============================================================================

@dataclass(frozen=True)
class FSMState:
    """
    Immutable representation of FSM state.
    
    Supports comparison, hashing, and transition tracking.
    """
    state_id: int
    is_accepting: bool = False
    is_initial: bool = False
    transitions: Tuple[Tuple[str, int], ...] = ()  # (char, next_state)
    
    def get_transition(self, char: str) -> Optional[int]:
        """Get next state for a character transition."""
        for c, next_state in self.transitions:
            if c == char:
                return next_state
        return None
    
    def get_all_transitions(self) -> Dict[str, int]:
        """Get all transitions as a dict."""
        return dict(self.transitions)


@dataclass
class FSMTransitionTable:
    """
    Transition table for efficient FSM execution.
    
    Uses integer arrays for fast state transitions.
    """
    num_states: int
    initial_state: int
    accepting_states: FrozenSet[int]
    
    # transition_table[state][char_code] = next_state (-1 = invalid)
    transition_table: np.ndarray = field(default=None)
    
    # Allowed characters per state (for bitmask generation)
    allowed_chars: Dict[int, Set[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.transition_table is None:
            # Default: 256 ASCII characters
            self.transition_table = np.full(
                (self.num_states, 256), -1, dtype=np.int32
            )
    
    def add_transition(self, from_state: int, char: str, to_state: int) -> None:
        """Add a transition."""
        char_code = ord(char) if len(char) == 1 else ord(char[0])
        if 0 <= char_code < 256:
            self.transition_table[from_state, char_code] = to_state
            
            if from_state not in self.allowed_chars:
                self.allowed_chars[from_state] = set()
            self.allowed_chars[from_state].add(char)
    
    def get_next_state(self, current_state: int, char: str) -> int:
        """Get next state for a character. Returns -1 if invalid."""
        char_code = ord(char) if len(char) == 1 else ord(char[0])
        if 0 <= char_code < 256:
            return int(self.transition_table[current_state, char_code])
        return -1
    
    def is_accepting(self, state: int) -> bool:
        """Check if state is accepting."""
        return state in self.accepting_states
    
    def get_allowed_chars(self, state: int) -> Set[str]:
        """Get allowed characters at a state."""
        return self.allowed_chars.get(state, set())


# =============================================================================
# Token Mask
# =============================================================================

@dataclass
class TokenMask:
    """
    Token-level constraint mask.
    
    Efficiently represents which tokens are allowed at a given FSM state.
    """
    vocab_size: int
    mask: np.ndarray = field(default=None)
    
    def __post_init__(self):
        if self.mask is None:
            self.mask = np.ones(self.vocab_size, dtype=np.bool_)
    
    def allow_only(self, token_ids: Set[int]) -> None:
        """Set mask to allow only specified tokens."""
        self.mask.fill(False)
        for tid in token_ids:
            if 0 <= tid < self.vocab_size:
                self.mask[tid] = True
    
    def disallow(self, token_ids: Set[int]) -> None:
        """Disallow specific tokens."""
        for tid in token_ids:
            if 0 <= tid < self.vocab_size:
                self.mask[tid] = False
    
    def apply_to_logits(self, logits: np.ndarray) -> np.ndarray:
        """Apply mask to logits (set disallowed to -inf)."""
        result = logits.copy()
        result[~self.mask] = float("-inf")
        return result
    
    def get_allowed_count(self) -> int:
        """Get number of allowed tokens."""
        return int(np.sum(self.mask))
    
    def get_allowed_tokens(self) -> List[int]:
        """Get list of allowed token IDs."""
        return list(np.where(self.mask)[0])
    
    def combine_and(self, other: "TokenMask") -> "TokenMask":
        """Combine masks with AND."""
        result = TokenMask(self.vocab_size)
        result.mask = self.mask & other.mask
        return result
    
    def combine_or(self, other: "TokenMask") -> "TokenMask":
        """Combine masks with OR."""
        result = TokenMask(self.vocab_size)
        result.mask = self.mask | other.mask
        return result


# =============================================================================
# Grammar Engine Base
# =============================================================================

class GrammarEngine(ABC):
    """
    Abstract base class for grammar engines.
    
    A grammar engine manages FSM construction and token constraint generation
    for a specific type of grammar (regex, JSON schema, EBNF, etc.).
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        self.vocab_size = vocab_size
        self.token_strings = token_strings or {}
        self.eos_token_id = eos_token_id
        
        # Reverse mapping: string -> token IDs
        self._string_to_tokens: Dict[str, List[int]] = {}
        for tid, tstr in self.token_strings.items():
            if tstr not in self._string_to_tokens:
                self._string_to_tokens[tstr] = []
            self._string_to_tokens[tstr].append(tid)
    
    @abstractmethod
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from specification string."""
        pass
    
    def get_tokens_for_chars(self, chars: Set[str]) -> Set[int]:
        """Get token IDs that start with any of the given characters."""
        tokens = set()
        
        for tid, tstr in self.token_strings.items():
            if tstr and tstr[0] in chars:
                tokens.add(tid)
        
        return tokens
    
    def get_token_mask(
        self,
        fsm: FSMTransitionTable,
        state: int,
    ) -> TokenMask:
        """Get token mask for current FSM state."""
        mask = TokenMask(self.vocab_size)
        
        if state < 0 or state >= fsm.num_states:
            # Invalid state - disallow all
            mask.mask.fill(False)
            return mask
        
        allowed_chars = fsm.get_allowed_chars(state)
        
        if not allowed_chars:
            # No transitions - might be accepting state
            if fsm.is_accepting(state) and self.eos_token_id is not None:
                mask.allow_only({self.eos_token_id})
            else:
                mask.mask.fill(False)
            return mask
        
        allowed_tokens = self.get_tokens_for_chars(allowed_chars)
        
        # If accepting, also allow EOS
        if fsm.is_accepting(state) and self.eos_token_id is not None:
            allowed_tokens.add(self.eos_token_id)
        
        mask.allow_only(allowed_tokens)
        return mask


# =============================================================================
# Regex Grammar Engine
# =============================================================================

class RegexGrammar(GrammarEngine):
    """
    Regex-based grammar engine.
    
    Converts regular expressions to FSMs for token-level constraints.
    Uses Thompson's construction for NFA, then subset construction for DFA.
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._compiled_cache: Dict[str, FSMTransitionTable] = {}
    
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build DFA from regex pattern."""
        if spec in self._compiled_cache:
            return self._compiled_cache[spec]
        
        try:
            # Use module-level _sre_parse for regex parsing
            parsed = _sre_parse.parse(spec)
            
            # Build NFA
            nfa = self._build_nfa(parsed)
            
            # Convert to DFA via subset construction
            dfa = self._nfa_to_dfa(nfa)
            
            self._compiled_cache[spec] = dfa
            return dfa
            
        except Exception as e:
            # Fallback: simple pattern matching
            return self._build_simple_fsm(spec)
    
    def _build_nfa(self, parsed) -> Dict[int, Dict[str, Set[int]]]:
        """Build NFA from parsed regex."""
        nfa: Dict[int, Dict[str, Set[int]]] = {0: {}}
        state_counter = [1]  # Mutable counter
        accepting = set()
        
        def process_pattern(pattern, start_state: int) -> Set[int]:
            """Process pattern recursively, return set of end states."""
            end_states = {start_state}
            
            for op, av in pattern:
                new_end_states = set()
                
                for state in end_states:
                    if state not in nfa:
                        nfa[state] = {}
                    
                    if op == _sre_parse.LITERAL:
                        # Single character
                        char = chr(av)
                        new_state = state_counter[0]
                        state_counter[0] += 1
                        
                        if char not in nfa[state]:
                            nfa[state][char] = set()
                        nfa[state][char].add(new_state)
                        
                        if new_state not in nfa:
                            nfa[new_state] = {}
                        new_end_states.add(new_state)
                        
                    elif op == _sre_parse.ANY:
                        # Match any character
                        new_state = state_counter[0]
                        state_counter[0] += 1
                        
                        # Add transitions for common chars
                        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                            if c not in nfa[state]:
                                nfa[state][c] = set()
                            nfa[state][c].add(new_state)
                        
                        if new_state not in nfa:
                            nfa[new_state] = {}
                        new_end_states.add(new_state)
                        
                    elif op == _sre_parse.IN:
                        # Character class
                        new_state = state_counter[0]
                        state_counter[0] += 1
                        
                        for item_op, item_av in av:
                            if item_op == _sre_parse.LITERAL:
                                char = chr(item_av)
                                if char not in nfa[state]:
                                    nfa[state][char] = set()
                                nfa[state][char].add(new_state)
                            elif item_op == _sre_parse.RANGE:
                                for code in range(item_av[0], item_av[1] + 1):
                                    char = chr(code)
                                    if char not in nfa[state]:
                                        nfa[state][char] = set()
                                    nfa[state][char].add(new_state)
                        
                        if new_state not in nfa:
                            nfa[new_state] = {}
                        new_end_states.add(new_state)
                        
                    elif op == _sre_parse.SUBPATTERN:
                        # Subpattern (group)
                        _, _, _, subpattern = av
                        sub_end = process_pattern(subpattern, state)
                        new_end_states.update(sub_end)
                        
                    elif op == _sre_parse.MAX_REPEAT or op == _sre_parse.MIN_REPEAT:
                        # Repetition
                        min_count, max_count, subpattern = av
                        
                        # Handle + and *
                        current_states = {state}
                        for _ in range(min(min_count, 10)):  # Limit unrolling
                            next_states = set()
                            for s in current_states:
                                ends = process_pattern(subpattern, s)
                                next_states.update(ends)
                            current_states = next_states
                        
                        # Add loop for * and +
                        if max_count > min_count or max_count == _sre_parse.MAXREPEAT:
                            for s in current_states:
                                loop_ends = process_pattern(subpattern, s)
                                # Add epsilon transitions back
                                for end in loop_ends:
                                    for char, targets in nfa.get(s, {}).items():
                                        if char not in nfa.get(end, {}):
                                            if end not in nfa:
                                                nfa[end] = {}
                                            nfa[end][char] = targets.copy()
                        
                        new_end_states.update(current_states)
                    else:
                        # Unsupported - just continue
                        new_end_states.add(state)
                
                end_states = new_end_states if new_end_states else end_states
            
            return end_states
        
        final_states = process_pattern(parsed, 0)
        accepting.update(final_states)
        
        return {"nfa": nfa, "accepting": accepting, "initial": 0}
    
    def _nfa_to_dfa(self, nfa_data: Dict) -> FSMTransitionTable:
        """Convert NFA to DFA using subset construction."""
        nfa = nfa_data["nfa"]
        accepting = nfa_data["accepting"]
        initial = nfa_data["initial"]
        
        # Simplified DFA construction
        dfa_states: Dict[FrozenSet[int], int] = {}
        dfa_transitions: Dict[int, Dict[str, int]] = {}
        dfa_accepting = set()
        
        initial_set = frozenset({initial})
        dfa_states[initial_set] = 0
        dfa_transitions[0] = {}
        
        if initial in accepting:
            dfa_accepting.add(0)
        
        worklist = [initial_set]
        state_counter = 1
        
        while worklist:
            current_set = worklist.pop()
            current_dfa = dfa_states[current_set]
            
            # Find all possible characters from this set
            all_chars = set()
            for nfa_state in current_set:
                if nfa_state in nfa:
                    all_chars.update(nfa[nfa_state].keys())
            
            for char in all_chars:
                # Compute next state set
                next_set = set()
                for nfa_state in current_set:
                    if nfa_state in nfa and char in nfa[nfa_state]:
                        next_set.update(nfa[nfa_state][char])
                
                if not next_set:
                    continue
                
                next_frozen = frozenset(next_set)
                
                if next_frozen not in dfa_states:
                    dfa_states[next_frozen] = state_counter
                    dfa_transitions[state_counter] = {}
                    
                    if next_set & accepting:
                        dfa_accepting.add(state_counter)
                    
                    worklist.append(next_frozen)
                    state_counter += 1
                
                dfa_transitions[current_dfa][char] = dfa_states[next_frozen]
        
        # Build transition table
        fsm = FSMTransitionTable(
            num_states=state_counter,
            initial_state=0,
            accepting_states=frozenset(dfa_accepting),
        )
        
        for from_state, transitions in dfa_transitions.items():
            for char, to_state in transitions.items():
                fsm.add_transition(from_state, char, to_state)
        
        return fsm
    
    def _build_simple_fsm(self, spec: str) -> FSMTransitionTable:
        """Build simple FSM for literal pattern matching."""
        # Each character is a state transition
        fsm = FSMTransitionTable(
            num_states=len(spec) + 1,
            initial_state=0,
            accepting_states=frozenset({len(spec)}),
        )
        
        for i, char in enumerate(spec):
            fsm.add_transition(i, char, i + 1)
        
        return fsm


# =============================================================================
# JSON Schema Grammar
# =============================================================================

class JsonSchemaGrammar(GrammarEngine):
    """
    JSON Schema to grammar conversion.
    
    Converts JSON Schema specifications to FSM-based constraints
    for generating valid JSON objects.
    """
    
    # JSON structural characters
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
            # Invalid schema - use generic JSON FSM
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
        # States: 0=start, 1=after{, 2=in_key, 3=after:, 4=in_value, 5=after_value, 6=end
        fsm = FSMTransitionTable(
            num_states=7,
            initial_state=0,
            accepting_states=frozenset({6}),
        )
        
        # State 0: expect {
        fsm.add_transition(0, "{", 1)
        fsm.add_transition(0, " ", 0)
        
        # State 1: after { - expect " for key or }
        fsm.add_transition(1, '"', 2)
        fsm.add_transition(1, "}", 6)
        fsm.add_transition(1, " ", 1)
        
        # State 2: in key - any string chars then "
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
            fsm.add_transition(2, c, 2)
        fsm.add_transition(2, '"', 3)
        
        # State 3: after key " - expect :
        fsm.add_transition(3, ":", 4)
        fsm.add_transition(3, " ", 3)
        
        # State 4: expect value
        for c in '"0123456789-ntf{[':
            fsm.add_transition(4, c, 5)
        fsm.add_transition(4, " ", 4)
        
        # State 5: after value - expect , or }
        fsm.add_transition(5, ",", 1)
        fsm.add_transition(5, "}", 6)
        fsm.add_transition(5, " ", 5)
        
        return fsm
    
    def _build_array_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON array."""
        fsm = FSMTransitionTable(
            num_states=4,
            initial_state=0,
            accepting_states=frozenset({3}),
        )
        
        # State 0: expect [
        fsm.add_transition(0, "[", 1)
        fsm.add_transition(0, " ", 0)
        
        # State 1: after [ - expect value or ]
        for c in '"0123456789-ntf{[':
            fsm.add_transition(1, c, 2)
        fsm.add_transition(1, "]", 3)
        fsm.add_transition(1, " ", 1)
        
        # State 2: after value - expect , or ]
        fsm.add_transition(2, ",", 1)
        fsm.add_transition(2, "]", 3)
        fsm.add_transition(2, " ", 2)
        
        return fsm
    
    def _build_string_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON string."""
        fsm = FSMTransitionTable(
            num_states=3,
            initial_state=0,
            accepting_states=frozenset({2}),
        )
        
        # State 0: expect "
        fsm.add_transition(0, '"', 1)
        fsm.add_transition(0, " ", 0)
        
        # State 1: in string
        for i in range(32, 127):
            c = chr(i)
            if c == '"':
                fsm.add_transition(1, c, 2)
            elif c == '\\':
                fsm.add_transition(1, c, 1)  # Simplified escape handling
            else:
                fsm.add_transition(1, c, 1)
        
        return fsm
    
    def _build_number_fsm(self, schema: Dict) -> FSMTransitionTable:
        """Build FSM for JSON number."""
        fsm = FSMTransitionTable(
            num_states=4,
            initial_state=0,
            accepting_states=frozenset({1, 2, 3}),
        )
        
        # State 0: start - expect digit or -
        fsm.add_transition(0, "-", 0)
        for c in "0123456789":
            fsm.add_transition(0, c, 1)
        
        # State 1: after digit - more digits or . or e
        for c in "0123456789":
            fsm.add_transition(1, c, 1)
        fsm.add_transition(1, ".", 2)
        fsm.add_transition(1, "e", 3)
        fsm.add_transition(1, "E", 3)
        
        # State 2: after decimal - digits
        for c in "0123456789":
            fsm.add_transition(2, c, 2)
        fsm.add_transition(2, "e", 3)
        fsm.add_transition(2, "E", 3)
        
        # State 3: exponent
        fsm.add_transition(3, "+", 3)
        fsm.add_transition(3, "-", 3)
        for c in "0123456789":
            fsm.add_transition(3, c, 3)
        
        return fsm
    
    def _build_boolean_fsm(self) -> FSMTransitionTable:
        """Build FSM for JSON boolean."""
        # true or false
        fsm = FSMTransitionTable(
            num_states=10,
            initial_state=0,
            accepting_states=frozenset({4, 9}),
        )
        
        # true path
        fsm.add_transition(0, "t", 1)
        fsm.add_transition(1, "r", 2)
        fsm.add_transition(2, "u", 3)
        fsm.add_transition(3, "e", 4)
        
        # false path
        fsm.add_transition(0, "f", 5)
        fsm.add_transition(5, "a", 6)
        fsm.add_transition(6, "l", 7)
        fsm.add_transition(7, "s", 8)
        fsm.add_transition(8, "e", 9)
        
        return fsm
    
    def _build_null_fsm(self) -> FSMTransitionTable:
        """Build FSM for JSON null."""
        fsm = FSMTransitionTable(
            num_states=5,
            initial_state=0,
            accepting_states=frozenset({4}),
        )
        
        fsm.add_transition(0, "n", 1)
        fsm.add_transition(1, "u", 2)
        fsm.add_transition(2, "l", 3)
        fsm.add_transition(3, "l", 4)
        
        return fsm
    
    def _build_generic_json_fsm(self) -> FSMTransitionTable:
        """Build generic FSM that accepts any JSON."""
        # Simplified: accept common JSON chars
        fsm = FSMTransitionTable(
            num_states=2,
            initial_state=0,
            accepting_states=frozenset({0, 1}),
        )
        
        for c in self.JSON_CHARS:
            fsm.add_transition(0, c, 0)
            fsm.add_transition(1, c, 1)
        
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            fsm.add_transition(0, c, 0)
            fsm.add_transition(1, c, 1)
        
        return fsm


# =============================================================================
# Choice Grammar
# =============================================================================

class ChoiceGrammar(GrammarEngine):
    """
    Grammar engine for fixed choice selection.
    
    Builds a trie-based FSM for efficient prefix matching.
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        super().__init__(vocab_size, token_strings, eos_token_id)
    
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from choice list (JSON array)."""
        choices = json.loads(spec)
        return self._build_trie_fsm(choices)
    
    def _build_trie_fsm(self, choices: List[str]) -> FSMTransitionTable:
        """Build trie-based FSM for choices."""
        # Build trie structure
        trie: Dict[int, Dict[str, int]] = {0: {}}
        accepting = set()
        state_counter = 1
        
        for choice in choices:
            current_state = 0
            
            for char in choice:
                if char not in trie[current_state]:
                    trie[current_state][char] = state_counter
                    trie[state_counter] = {}
                    state_counter += 1
                
                current_state = trie[current_state][char]
            
            accepting.add(current_state)
        
        # Build FSM
        fsm = FSMTransitionTable(
            num_states=state_counter,
            initial_state=0,
            accepting_states=frozenset(accepting),
        )
        
        for from_state, transitions in trie.items():
            for char, to_state in transitions.items():
                fsm.add_transition(from_state, char, to_state)
        
        return fsm


# =============================================================================
# EBNF Grammar
# =============================================================================

class EBNFGrammar(GrammarEngine):
    """
    EBNF/Lark grammar engine.
    
    Parses EBNF grammar specifications and converts to FSM.
    Supports common grammar constructs:
    - Alternation (|)
    - Sequence (concatenation)
    - Optional (?)
    - Repetition (* +)
    - Grouping (())
    - Character classes ([])
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._rule_cache: Dict[str, FSMTransitionTable] = {}
    
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from EBNF grammar."""
        if spec in self._rule_cache:
            return self._rule_cache[spec]
        
        try:
            # Parse EBNF rules
            rules = self._parse_ebnf(spec)
            
            # Build FSM from start rule
            if "start" in rules:
                fsm = self._rule_to_fsm(rules["start"], rules)
            else:
                # Use first rule as start
                first_rule = next(iter(rules.values()))
                fsm = self._rule_to_fsm(first_rule, rules)
            
            self._rule_cache[spec] = fsm
            return fsm
            
        except Exception:
            # Fallback to simple literal matching
            return self._build_literal_fsm(spec)
    
    def _parse_ebnf(self, spec: str) -> Dict[str, str]:
        """Parse EBNF grammar into rules."""
        rules = {}
        
        # Simple parser for EBNF-like rules
        # Format: rule_name: expression
        for line in spec.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if ":" in line:
                name, expr = line.split(":", 1)
                rules[name.strip()] = expr.strip()
        
        return rules
    
    def _rule_to_fsm(
        self,
        rule: str,
        all_rules: Dict[str, str],
    ) -> FSMTransitionTable:
        """Convert a single rule to FSM."""
        # Simplified: treat as regex-like pattern
        regex_engine = RegexGrammar(
            self.vocab_size, self.token_strings, self.eos_token_id
        )
        
        # Convert common EBNF to regex
        pattern = rule
        pattern = pattern.replace(" ", "")
        pattern = re.sub(r'\[([^\]]+)\]', r'[\1]', pattern)  # Keep char classes
        
        return regex_engine.build_fsm(pattern)
    
    def _build_literal_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM for literal string matching."""
        fsm = FSMTransitionTable(
            num_states=len(spec) + 1,
            initial_state=0,
            accepting_states=frozenset({len(spec)}),
        )
        
        for i, char in enumerate(spec):
            fsm.add_transition(i, char, i + 1)
        
        return fsm
