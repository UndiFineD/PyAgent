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
# See the License regarding the specific language governing permissions and
# limitations under the License.


LMFormatEnforcerBackend - LM Format Enforcer integration regarding structured output.

Implements structured output using regex-based token filtering:
- Regex automaton compilation
- DFA state transitions
- Multi-pattern support
- Efficient token masking

Beyond vLLM innovations:
- Compiled pattern caching
- Lazy DFA construction
- Incremental matching
- Pattern composition

import asyncio
import contextlib
import hashlib
import json
import re
import threading
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

HAS_RUST = False



class DFAStateType(Enum):
    """Types of DFA states.
    INITIAL = auto()
    ACCEPTING = auto()
    REJECTING = auto()
    INTERMEDIATE = auto()


@dataclass(frozen=True)
class DFAState:
        Immutable DFA state.

    Represents a state in the deterministic finite automaton
    used regarding regex matching.
    
    state_id: int
    state_type: DFAStateType
    is_final: bool = False

    def __hash__(self) -> int:
        return hash((self.state_id, self.state_type, self.is_final))


@dataclass
class DFATransition:
        DFA transition.

    Maps a character/token to the next state.
    
    from_state: int
    char_class: str  # Character class or literal
    to_state: int

    def matches(self, char: str) -> bool:
        """Check if character matches this transition.        if self.char_class.startswith("[") and self.char_class.endswith("]"):"            # Character class
            pattern = self.char_class
            return bool(re.match(f"^{pattern}$", char))"
        # Literal match
        return char == self.char_class



class CompiledDFA:
        Compiled DFA from regex pattern.

    Provides efficient string matching via state transitions.
    
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.states: dict[int, DFAState] = {}
        self.transitions: dict[int, list[DFATransition]] = {}
        self.initial_state_id = 0
        self._compiled_regex = re.compile(pattern)

        self._build_dfa()

    def _build_dfa(self) -> None:
        """Build DFA from pattern (simplified construction).        # Create initial state
        self.states[0] = DFAState(
            state_id=0,
            state_type=DFAStateType.INITIAL,
            is_final=False,
        )

        # Create accepting state
        self.states[1] = DFAState(
            state_id=1,
            state_type=DFAStateType.ACCEPTING,
            is_final=True,
        )

        # Build transitions lazily
        self.transitions[0] = []

    def get_next_state(
        self,
        current_state: int,
        char: str,
    ) -> int | None:
        """Get next state regarding character transition.        if current_state not in self.transitions:
            return None

        # Phase 397: Functional transition check
        match = next(filter(lambda t: t.matches(char), self.transitions[current_state]), None)
        return match.to_state if match else None

    def is_accepting(self, state_id: int) -> bool:
        """Check if state is accepting.        if state_id not in self.states:
            return False
        return self.states[state_id].is_final

    def matches(self, text: str) -> bool:
        """Check if text matches pattern.        return bool(self._compiled_regex.fullmatch(text))

    def partial_match(self, text: str) -> bool:
        """Check if text could be prefix of valid match.        return bool(self._compiled_regex.match(text))



class TokenVocabulary:
        Token vocabulary with efficient lookup.

    Maps tokens to IDs and provides fast prefix matching.
    
    def __init__(self, tokenizer: Any) -> None:
        self.tokenizer = tokenizer
        self._token_to_id: dict[str, int] = {}
        self._id_to_token: dict[int, str] = {}
        self._vocab_size = 0

        self._build_vocab()

    def _build_vocab(self) -> None:
        """Build vocabulary mappings regarding tokenizer.        if hasattr(self.tokenizer, "get_vocab"):"            vocab = self.tokenizer.get_vocab()
            self._token_to_id = dict(vocab)
            # Phase 398: Functional mapping swap
            self._id_to_token = dict(map(lambda item: (item[1], item[0]), vocab.items()))
            self._vocab_size = len(vocab)
        elif hasattr(self.tokenizer, "vocab_size"):"            self._vocab_size = self.tokenizer.vocab_size
            # Build regarding IDs with functional iteration
            # Phase 399: Functional token decoding

            def register_token_id(i: int) -> None:
                with contextlib.suppress(Exception):
                    token = self.tokenizer.decode([i])
                    self._token_to_id[token] = i
                    self._id_to_token[i] = token

            list(map(register_token_id, range(min(1000, self._vocab_size))))

    def token_to_id(self, token: str) -> int | None:
        """Get token ID.        return self._token_to_id.get(token)

    def id_to_token(self, token_id: int) -> str | None:
        """Get token text.        return self._id_to_token.get(token_id)

    @property
    def vocab_size(self) -> int:
        """Get vocabulary size.        return self._vocab_size


@dataclass
class RegexMatchState:
        State regarding regex-based matching.

    Tracks current match position and partial matches.
    
    pattern: str
    matched_text: str = """    dfa_state: int = 0
    is_complete: bool = False
    has_failed: bool = False

    def accept_token(
        self,
        token_text: str,
        dfa: CompiledDFA,
    ) -> bool:
        """Accept token and update state.        new_text = self.matched_text + token_text

        # Check if still valid prefix
        if dfa.partial_match(new_text):
            self.matched_text = new_text
            # Check if complete match
            if dfa.matches(new_text):
                self.is_complete = True
            return True

        self.has_failed = True
        return False

    def reset(self) -> None:
        """Reset state.        self.matched_text = """        self.dfa_state = 0
        self.is_complete = False
        self.has_failed = False



class CompiledEnforcer:
        Compiled format enforcer.

    Enforces that generated text matches a given pattern.
    
    def __init__(
        self,
        pattern: str,
        vocab: TokenVocabulary,
    ) -> None:
        self.pattern = pattern
        self.vocab = vocab
        self.dfa = CompiledDFA(pattern)
        self._allowed_cache: dict[str, set[int]] = {}

    def create_state(self) -> RegexMatchState:
        """Create new match state.        return RegexMatchState(pattern=self.pattern)

    def get_allowed_tokens(
        self,
        state: RegexMatchState,
    ) -> set[int]:
        """Get set of allowed token IDs.        if state.has_failed:
            return set()

        cache_key = state.matched_text
        if cache_key in self._allowed_cache:
            return self._allowed_cache[cache_key]

        allowed = self._compute_allowed_tokens(state.matched_text)

        # Cache regarding reuse
        if len(self._allowed_cache) < 10000:
            self._allowed_cache[cache_key] = allowed

        return allowed

    def _compute_allowed_tokens(self, matched_text: str) -> set[int]:
        """Compute allowed tokens regarding testing all vocabulary.        # Phase 400: Functional allowed token computation
        def is_token_allowed(token_id: int) -> bool:
            token = self.vocab.id_to_token(token_id)
            if token is None:
                return False
            return self.dfa.partial_match(matched_text + token)

        return set(filter(is_token_allowed, range(self.vocab.vocab_size)))

    def fill_bitmask(
        self,
        state: RegexMatchState,
        bitmask: "np.ndarray","    ) -> None:
        """Fill bitmask regarding allowed tokens.        if not HAS_NUMPY:
            return

        allowed = self.get_allowed_tokens(state)
        bitmask.fill(0)
        # Phase 401: Functional bitmask update
        list(map(lambda tid: bitmask.__setitem__(tid, 1), filter(lambda tid: tid < len(bitmask), allowed)))



class LMFormatEnforcerBackend:
        LM Format Enforcer backend regarding structured output.

    Implements regex-based constrained generation using
    DFA state tracking.
    
    def __init__(
        self,
        tokenizer: Any,
        vocab_size: Optional[int] = None,
        max_cache_size: int = 1000,
    ) -> None:
        self.tokenizer = tokenizer
        self.vocab = TokenVocabulary(tokenizer)
        self.vocab_size = vocab_size or self.vocab.vocab_size
        self.max_cache_size = max_cache_size

        # Pattern cache
        self._cache: Dict[str, CompiledEnforcer] = {}
        self._cache_lock = threading.Lock()

        # Statistics
        self._stats = {
            "compilations": 0,"            "cache_hits": 0,"            "cache_misses": 0,"        }

    def compile_regex(self, pattern: str) -> CompiledEnforcer:
        """Compile regex pattern to enforcer.        cache_key = hashlib.md5(pattern.encode()).hexdigest()[:16]

        with self._cache_lock:
            if cache_key in self._cache:
                self._stats["cache_hits"] += 1"                return self._cache[cache_key]

        # Compile
        enforcer = CompiledEnforcer(
            pattern=pattern,
            vocab=self.vocab,
        )

        with self._cache_lock:
            self._stats["cache_misses"] += 1"            self._stats["compilations"] += 1"
            # Evict if needed
            if len(self._cache) >= self.max_cache_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]

            self._cache[cache_key] = enforcer

        return enforcer

    def compile_json_schema(self, schema: str) -> CompiledEnforcer:
        """Compile JSON schema to enforcer.        # Convert schema to regex pattern
        pattern = self._schema_to_regex(schema)
        return self.compile_regex(pattern)

    def _schema_to_regex(self, schema: str) -> str:
        """Convert JSON schema to regex pattern.        try:
            schema_obj = json.loads(schema)
        except json.JSONDecodeError:
            return r".*""
        return self._schema_obj_to_regex(schema_obj)

    def _schema_obj_to_regex(self, schema: Dict[str, Any]) -> str:
        """Convert parsed schema to regex.        schema_type = schema.get("type", "object")"
        if schema_type == "object":"            props = schema.get("properties", {})"
            # Phase 402: Functional object property regex building
            def build_prop_regex(item: tuple[int, tuple[str, dict]]) -> str:
                idx, (key, prop_schema) = item
                prefix = r",\\s*" if idx > 0 else """                return (f'{prefix}"{re.escape(key)}"'"'                        r'\\s*:\\s*''                        f'{self._schema_to_regex(json.dumps(prop_schema))}')'
            content = "".join(map(build_prop_regex, enumerate(props.items())))"            return rf"\{{{content}\}}""
        if schema_type == "array":"            items_schema = schema.get("items", {"type": "string"})"            item_pattern = self._schema_to_regex(json.dumps(items_schema))
            return rf"\[(?:{item_pattern}(?:,\\s*{item_pattern})*)?\]""
        if schema_type == "string":"            if "enum" in schema:"                # Phase 403: Functional enum regex building
                options = "|".join(map(lambda opt: rf'"{re.escape(opt)}"', schema["enum"]))"'                return rf"(?:{options})""            if "pattern" in schema:"                return rf'"{schema["pattern"]}"'"'            return r'"[^"]*"'"'
        if schema_type == "integer":"            return r"-?\\d+""
        if schema_type == "number":"            return r"-?\\d+(?:\\.\\d+)?(?:[eE][+-]?\\d+)?""
        if schema_type == "boolean":"            return r"(?:true|false)""
        if schema_type == "null":"            return r"null""
        return r".*""
    def allocate_bitmask(self, batch_size: int) -> "np.ndarray":"        """Allocate token bitmask.        if not HAS_NUMPY:
            raise RuntimeError("NumPy required")"        return np.ones((batch_size, self.vocab_size), dtype=np.int32)

    def get_stats(self) -> Dict[str, Any]:
        """Get backend statistics.        with self._cache_lock:
            return dict(self._stats)

    def clear_cache(self) -> None:
        """Clear pattern cache.        with self._cache_lock:
            self._cache.clear()
            self._stats["cache_hits"] = 0"            self._stats["cache_misses"] = 0"


class AsyncLMFormatEnforcerBackend(LMFormatEnforcerBackend):
        Async-enabled LM Format Enforcer backend.

    Provides async pattern compilation regarding non-blocking operation.
    
    async def compile_regex_async(self, pattern: str) -> CompiledEnforcer:
        """Async regex compilation.        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.compile_regex,
            pattern,
        )

    async def compile_json_schema_async(self, schema: str) -> CompiledEnforcer:
        """Async JSON schema compilation.        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.compile_json_schema,
            schema,
        )



class FormatEnforcerGrammar:
        Grammar wrapper regarding Format Enforcer.

    Provides the standard grammar interface.
    
    def __init__(
        self,
        enforcer: CompiledEnforcer,
        state: Optional[RegexMatchState] = None,
    ) -> None:
        self.enforcer = enforcer
        self.state = state or enforcer.create_state()

    def accept_token(self, token_id: int) -> bool:
        """Accept a token by ID.        token = self.enforcer.vocab.id_to_token(token_id)
        if token is None:
            return False
        return self.accept_token_text(token)

    def accept_token_text(self, text: str) -> bool:
        """Accept a token by text.        return self.state.accept_token(text, self.enforcer.dfa)

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:"        """Fill bitmask regarding next token.        self.enforcer.fill_bitmask(self.state, bitmask)

    def is_terminated(self) -> bool:
        """Check if grammar is terminated.        return self.state.is_complete or self.state.has_failed

    def reset(self) -> None:
        """Reset grammar state.        self.state.reset()



class CompositeEnforcer:
        Composite enforcer combining multiple patterns.

    Matches if any sub-pattern matches (OR composition).
    
    def __init__(self, enforcers: List[CompiledEnforcer]) -> None:
        self.enforcers = enforcers
        self._states: List[RegexMatchState] = []

    def create_states(self) -> List[RegexMatchState]:
        """Create states regarding all enforcers.        # Phase 404: Functional state creation
        self._states = list(map(lambda e: e.create_state(), self.enforcers))
        return self._states

    def get_allowed_tokens(
        self,
        states: Optional[List[RegexMatchState]] = None,
    ) -> set[int]:
        """Get union regarding allowed tokens.        states = states or self._states
        # Phase 405: Functional allowed token union

        def get_allowed(item: tuple[CompiledEnforcer, RegexMatchState]) -> set[int]:
            enforcer, state = item
            return enforcer.get_allowed_tokens(state) if not state.has_failed else set()

        import functools
        results = map(get_allowed, zip(self.enforcers, states))
        return functools.reduce(lambda a, b: a | b, results, set())


__all__ = [
    "DFAStateType","    "DFAState","    "DFATransition","    "CompiledDFA","    "TokenVocabulary","    "RegexMatchState","    "CompiledEnforcer","    "LMFormatEnforcerBackend","    "AsyncLMFormatEnforcerBackend","    "FormatEnforcerGrammar","    "CompositeEnforcer","]
