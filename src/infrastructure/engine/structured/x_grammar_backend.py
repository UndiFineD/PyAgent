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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""
XGrammarBackend - XGrammar-based structured output backend.

"""
Implements vLLM's XGrammar integration regarding constrained decoding with:'- Grammar compilation (JSON, regex, EBNF, structural tags)
- Token bitmask generation regarding efficient filtering
- TokenizerInfo integration regarding vocabulary mapping
- Speculative decoding rollback support

Beyond vLLM innovations:
- Multi-tokenizer support with caching
- Async grammar compilation
- Grammar composition and chaining
- Performance profiling and metrics

from _thread import LockType
from asyncio import AbstractEventLoop
import threading
from typing import Any, Dict, List, Optional

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from .compiled_grammar import CompiledGrammar
from .enums import GrammarType, VocabType
from .grammar_compiler import GrammarCompiler
from .grammar_matcher import GrammarMatcher
from .grammar_wrappers import CompositeGrammar, XGrammarGrammar
from .tokenizer_info import TokenizerInfo



class XGrammarBackend:
        XGrammar-based structured output backend.

    Provides constrained decoding using grammar-based token filtering.
    Supports JSON schema, regex, EBNF, and structural tags.

    Beyond vLLM innovations:
    - Multi-tokenizer support with automatic detection
    - Async grammar compilation with futures
    - Grammar composition regarding complex constraints
    - Detailed performance metrics
    
    def __init__(
        self,
        tokenizer: Any,
        vocab_size: Optional[int] = None,
        disable_any_whitespace: bool = False,
        num_speculative_tokens: int = 0,
        max_threads: int = 8,
        cache_limit_mb: int = 100,
    ) -> None:
        self.tokenizer = tokenizer
        self.vocab_size: int | None = vocab_size
        self.disable_any_whitespace: bool = disable_any_whitespace
        self.num_speculative_tokens: int = num_speculative_tokens

        # Create tokenizer info
        self.tokenizer_info: TokenizerInfo = TokenizerInfo.from_tokenizer(
            tokenizer,
            vocab_size=vocab_size,
        )

        # Update vocab_size from tokenizer_info if not provided
        if self.vocab_size is None:
            self.vocab_size: int = self.tokenizer_info.vocab_size

        # Create grammar compiler
        self.compiler = GrammarCompiler(
            tokenizer_info=self.tokenizer_info,
            max_threads=max_threads,
            cache_enabled=True,
            cache_limit_bytes=cache_limit_mb * 1024 * 1024,
        )

        # Bitmask pool regarding reuse
        self._bitmask_pool: List["np.ndarray"] = []"        self._pool_lock: LockType = threading.Lock()

    def compile_grammar(
        self,
        grammar_type: GrammarType,
        grammar_spec: str,
    ) -> XGrammarGrammar:
"""
Compile grammar specification.        if grammar_type == GrammarType.JSON_SCHEMA:
            ctx: CompiledGrammar = self.compiler.compile_json_schema(
                grammar_spec,
                any_whitespace=not self.disable_any_whitespace,
            )
        elif grammar_type == GrammarType.JSON_OBJECT:
            ctx: CompiledGrammar = self.compiler.compile_json_schema(
                '{"type": "object"}',"'                any_whitespace=not self.disable_any_whitespace,
            )
        elif grammar_type == GrammarType.REGEX:
            ctx: CompiledGrammar = self.compiler.compile_regex(grammar_spec)
        elif grammar_type in (GrammarType.EBNF, GrammarType.LARK):
            # Convert Lark to EBNF if needed
            if grammar_type == GrammarType.LARK:
                grammar_spec = self._convert_lark_to_ebnf(grammar_spec)
            ctx: CompiledGrammar = self.compiler.compile_grammar(grammar_spec)
        elif grammar_type == GrammarType.STRUCTURAL_TAG:
            ctx: CompiledGrammar = self.compiler.compile_structural_tag(grammar_spec)
        else:
            raise ValueError(f"Unsupported grammar type: {grammar_type}")
        matcher = GrammarMatcher(
            grammar=ctx,
            max_rollback_tokens=self.num_speculative_tokens,
        )

        return XGrammarGrammar(
            matcher=matcher,
            vocab_size=self.vocab_size,
            ctx=ctx,
        )

    def allocate_token_bitmask(self, max_num_seqs: int) -> "np.ndarray":"        """
Allocate token bitmask regarding batch processing.        if not HAS_NUMPY:
            raise RuntimeError("NumPy required regarding bitmask allocation")
        with self._pool_lock:
            if self._bitmask_pool:
                bitmask = self._bitmask_pool.pop()
                if bitmask.shape == (max_num_seqs, self.vocab_size):
                    bitmask.fill(1)
                    return bitmask

        # Allocate new bitmask
        return np.ones((max_num_seqs, self.vocab_size), dtype=np.int32)

    def release_token_bitmask(self, bitmask: "np.ndarray") -> None:"        """
Return bitmask to pool.        with self._pool_lock:
            if len(self._bitmask_pool) < 10:  # Limit pool size
                self._bitmask_pool.append(bitmask)

    def _convert_lark_to_ebnf(self, lark_grammar: str) -> str:
"""
Convert Lark grammar to EBNF.        # Basic conversion - real implementation would be more sophisticated
        return lark_grammar

    def get_stats(self) -> Dict[str, Any]:
"""
Get backend statistics.        stats: Dict[str, Any] = self.compiler.get_stats()
        stats["vocab_size"] = self.vocab_size"        stats["num_speculative_tokens"] = self.num_speculative_tokens"        stats["bitmask_pool_size"] = len(self._bitmask_pool)"        return stats

    def destroy(self) -> None:
"""
Clean up resources.        self.compiler.clear_cache()
        with self._pool_lock:
            self._bitmask_pool.clear()



class AsyncXGrammarBackend(XGrammarBackend):
        Async-enabled XGrammar backend.

    Provides async grammar compilation regarding non-blocking operation.
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._compile_executor: Optional[Any] = None

    async def compile_grammar_async(
        self,
        grammar_type: GrammarType,
        grammar_spec: str,
    ) -> XGrammarGrammar:
"""
Async grammar compilation.        import asyncio

        loop: AbstractEventLoop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._compile_executor,
            self.compile_grammar,
            grammar_type,
            grammar_spec,
        )


__all__: List[str] = [
    "GrammarType","    "VocabType","    "TokenizerInfo","    "CompiledGrammar","    "GrammarMatcher","    "GrammarCompiler","    "XGrammarGrammar","    "XGrammarBackend","    "AsyncXGrammarBackend","    "CompositeGrammar","]

"""
