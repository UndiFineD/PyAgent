# XGrammarBackend

**File**: `src\infrastructure\structured_output\XGrammarBackend.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 25 imports  
**Lines**: 660  
**Complexity**: 43 (complex)

## Overview

XGrammarBackend - XGrammar-based structured output backend.

Implements vLLM's XGrammar integration for constrained decoding with:
- Grammar compilation (JSON, regex, EBNF, structural tags)
- Token bitmask generation for efficient filtering
- TokenizerInfo integration for vocabulary mapping
- Speculative decoding rollback support

Beyond vLLM innovations:
- Multi-tokenizer support with caching
- Async grammar compilation
- Grammar composition and chaining
- Performance profiling and metrics

## Classes (10)

### `GrammarType`

**Inherits from**: Enum

Types of grammar specifications.

### `VocabType`

**Inherits from**: Enum

Vocabulary encoding types.

### `TokenizerInfo`

Tokenizer information for XGrammar.

Encapsulates vocabulary and tokenizer metadata needed for
grammar compilation and bitmask generation.

**Methods** (2):
- `from_tokenizer(cls, tokenizer, vocab_size)`
- `_detect_vocab_type(tokenizer)`

### `CompiledGrammar`

Compiled grammar context.

Holds the compiled grammar state and provides methods for
token acceptance checking and bitmask generation.

**Methods** (7):
- `__post_init__(self)`
- `_compute_cache_key(self)`
- `accept_token(self, token_id)`
- `rollback(self, num_tokens)`
- `reset(self)`
- `is_terminated(self)`
- `fill_bitmask(self, bitmask)`

### `GrammarMatcher`

Grammar matcher with rollback support.

Wraps CompiledGrammar with additional state management
for speculative decoding scenarios.

**Methods** (4):
- `accept_token(self, token_id)`
- `rollback(self, num_tokens)`
- `reset(self)`
- `fill_next_token_bitmask(self, bitmask)`

### `GrammarCompiler`

Grammar compiler with caching.

Compiles grammar specifications into executable matchers
with thread-safe caching and configurable limits.

**Methods** (9):
- `__init__(self, tokenizer_info, max_threads, cache_enabled, cache_limit_bytes)`
- `compile_json_schema(self, schema, any_whitespace)`
- `compile_regex(self, pattern)`
- `compile_grammar(self, ebnf)`
- `compile_structural_tag(self, spec, triggers)`
- `_get_cached(self, key)`
- `_put_cached(self, key, grammar)`
- `get_stats(self)`
- `clear_cache(self)`

### `XGrammarGrammar`

XGrammar grammar wrapper.

Provides the interface expected by the structured output system
while wrapping the internal grammar matcher.

**Methods** (7):
- `__init__(self, matcher, vocab_size, ctx)`
- `accept_token(self, token_id)`
- `rollback(self, num_tokens)`
- `reset(self)`
- `is_terminated(self)`
- `fill_next_token_bitmask(self, bitmask)`
- `jump_forward_string(self)`

### `XGrammarBackend`

XGrammar-based structured output backend.

Provides constrained decoding using grammar-based token filtering.
Supports JSON schema, regex, EBNF, and structural tags.

Beyond vLLM innovations:
- Multi-tokenizer support with automatic detection
- Async grammar compilation with futures
- Grammar composition for complex constraints
- Detailed performance metrics

**Methods** (7):
- `__init__(self, tokenizer, vocab_size, disable_any_whitespace, num_speculative_tokens, max_threads, cache_limit_mb)`
- `compile_grammar(self, grammar_type, grammar_spec)`
- `allocate_token_bitmask(self, max_num_seqs)`
- `release_token_bitmask(self, bitmask)`
- `_convert_lark_to_ebnf(self, lark_grammar)`
- `get_stats(self)`
- `destroy(self)`

### `AsyncXGrammarBackend`

**Inherits from**: XGrammarBackend

Async-enabled XGrammar backend.

Provides async grammar compilation for non-blocking operation.

**Methods** (1):
- `__init__(self)`

### `CompositeGrammar`

Composite grammar for combining multiple constraints.

Beyond vLLM: Allows chaining multiple grammars for complex constraints.

**Methods** (6):
- `__init__(self, grammars)`
- `accept_token(self, token_id)`
- `rollback(self, num_tokens)`
- `reset(self)`
- `is_terminated(self)`
- `fill_next_token_bitmask(self, bitmask)`

## Dependencies

**Imports** (25):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `json`
- `numpy`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- ... and 10 more

---
*Auto-generated documentation*
