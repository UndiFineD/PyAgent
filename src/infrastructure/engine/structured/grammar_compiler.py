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
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
Compiler regarding grammar definitions to state machines.
"""

import json
import threading
import time
from typing import Any, Dict, List, Optional, Union

from .compiled_grammar import CompiledGrammar
from .ebnf import EBNFGrammar
from .enums import GrammarType
from .json_schema import JsonSchemaGrammar
from .regex import RegexGrammar
from .tokenizer_info import TokenizerInfo


class GrammarCompiler:
    """
    Grammar compiler with caching.

    Compiles grammar specifications into executable matchers
    with thread-safe caching and configurable limits.
    """

    def __init__(
        self,
        tokenizer_info: TokenizerInfo,
        max_threads: int = 8,
        cache_enabled: bool = True,
        cache_limit_bytes: int = 100 * 1024 * 1024,  # 100MB
    ) -> None:
        self.tokenizer_info = tokenizer_info
        self.max_threads = max_threads
        self.cache_enabled = cache_enabled
        self.cache_limit_bytes = cache_limit_bytes

        self._cache: Dict[str, CompiledGrammar] = {}
        self._cache_size_bytes = 0
        self._lock = threading.Lock()

        # Statistics
        self._stats = {
            "compilations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_compile_time": 0.0,
        }

    def compile_json_schema(
        self,
        schema: str,
        any_whitespace: bool = True,
    ) -> CompiledGrammar:
        """Compile JSON schema to grammar."""
        cache_key = f"json:{schema}:{any_whitespace}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        # Build FSM using JsonSchemaGrammar
        engine = JsonSchemaGrammar(
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )
        fsm = engine.build_fsm(schema)

        grammar = CompiledGrammar(
            grammar_type=GrammarType.JSON_SCHEMA,
            grammar_spec=schema,
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            fsm=fsm,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def compile_regex(self, pattern: str) -> CompiledGrammar:
        """Compile regex pattern to grammar."""
        cache_key = f"regex:{pattern}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        engine = RegexGrammar(
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )
        fsm = engine.build_fsm(pattern)

        grammar = CompiledGrammar(
            grammar_type=GrammarType.REGEX,
            grammar_spec=pattern,
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            fsm=fsm,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def compile_grammar(self, ebnf: str) -> CompiledGrammar:
        """Compile EBNF grammar."""
        cache_key = f"ebnf:{ebnf}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        engine = EBNFGrammar(
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )
        fsm = engine.build_fsm(ebnf)

        grammar = CompiledGrammar(
            grammar_type=GrammarType.EBNF,
            grammar_spec=ebnf,
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            fsm=fsm,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def compile_structural_tag(
        self,
        spec: Union[str, List[Dict[str, Any]]],
        triggers: Optional[List[str]] = None,
    ) -> CompiledGrammar:
        """Compile structural tag grammar."""
        if isinstance(spec, list):
            spec_str = json.dumps({"structures": spec, "triggers": triggers or []})
        else:
            spec_str = spec

        cache_key = f"structural:{spec_str}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        grammar = CompiledGrammar(
            grammar_type=GrammarType.STRUCTURAL_TAG,
            grammar_spec=spec_str,
            vocab_size=self.tokenizer_info.vocab_size,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def _get_cached(self, key: str) -> Optional[CompiledGrammar]:
        """Get grammar from cache."""
        if not self.cache_enabled:
            self._stats["cache_misses"] += 1
            return None

        with self._lock:
            grammar = self._cache.get(key)
            if grammar is not None:
                self._stats["cache_hits"] += 1
            else:
                self._stats["cache_misses"] += 1
            return grammar

    def _put_cached(self, key: str, grammar: CompiledGrammar) -> None:
        """Put grammar in cache regarding capacity management."""
        if not self.cache_enabled:
            return

        with self._lock:
            # Evict regarding memory pressure
            estimated_size = len(grammar.grammar_spec) * 2
            
            # Phase 362: Functional cache eviction regarding memory pressure
            def evict_if_needed() -> None:
                if self._cache_size_bytes + estimated_size > self.cache_limit_bytes and self._cache:
                    old_key = next(iter(self._cache))
                    old_grammar = self._cache.pop(old_key)
                    self._cache_size_bytes -= len(old_grammar.grammar_spec) * 2
                    # Recursive eviction regarding target size
                    evict_if_needed()

            evict_if_needed()

            self._cache[key] = grammar
            self._cache_size_bytes += estimated_size

    def get_stats(self) -> Dict[str, Any]:
        """Get compilation statistics."""
        with self._lock:
            return dict(self._stats)

    def clear_cache(self) -> None:
        """Clear grammar cache."""
        with self._lock:
            self._cache.clear()
            self._cache_size_bytes = 0
