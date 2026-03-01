# engine

**File**: `src\infrastructure\structured_output\manager\engine.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 20 imports  
**Lines**: 267  
**Complexity**: 15 (moderate)

## Overview

Python module containing implementation for engine.

## Classes (2)

### `StructuredOutputManager`

Engine-level manager for structured output constraints.

**Methods** (12):
- `__init__(self, vocab_size, max_batch_size, cache_size, num_compile_workers, enable_async)`
- `register_backend(self, name, backend, grammar_types)`
- `get_backend(self, grammar_type)`
- `compile_grammar(self, grammar_spec, request_id, async_compile)`
- `_do_compile(self, backend, grammar_spec, request_id, cache_key)`
- `_get_from_cache(self, key)`
- `_add_to_cache(self, key, grammar)`
- `_clone_grammar(self, grammar, request_id)`
- `fill_batch_bitmask(self, grammars, bitmask)`
- `validate_and_accept(self, grammar, tokens)`
- ... and 2 more methods

### `SimpleBackend`

**Inherits from**: StructuredOutputBackend

Simple backend implementation for basic grammar types.

**Methods** (3):
- `__init__(self, vocab_size, tokenizer_encode, tokenizer_decode, token_strings)`
- `compile_grammar(self, grammar_spec, request_id)`
- `get_supported_types(self)`

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `base.StructuredOutputBackend`
- `base.StructuredOutputGrammar`
- `concurrent.futures.Future`
- `concurrent.futures.ThreadPoolExecutor`
- `config.GrammarSpec`
- `config.GrammarType`
- `config.ValidationResult`
- `impl.ChoiceGrammar`
- `impl.SimpleRegexGrammar`
- `numpy`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- ... and 5 more

---
*Auto-generated documentation*
