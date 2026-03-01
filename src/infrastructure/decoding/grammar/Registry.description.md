# Registry

**File**: `src\infrastructure\decoding\grammar\Registry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 2 functions, 16 imports  
**Lines**: 234  
**Complexity**: 10 (moderate)

## Overview

Backend selection and dispatching logic for structured output grammars.

## Classes (2)

### `GrammarCompiler`

Compiles grammar specifications into grammar objects.

Inspired by vLLM's structured output backends.

**Methods** (2):
- `__init__(self, vocab_size, token_to_string)`
- `compile(self, params)`

### `StructuredOutputManager`

Manages grammar compilation and lifecycle.

Inspired by vLLM's StructuredOutputManager.

**Methods** (6):
- `__init__(self, vocab_size, token_to_string)`
- `init_grammar(self, request_id, params)`
- `get_grammar(self, request_id)`
- `remove_grammar(self, request_id)`
- `accept_tokens(self, request_id, tokens)`
- `fill_bitmasks(self, request_ids, bitmask)`

## Functions (2)

### `compile_grammar(params, vocab_size, token_to_string)`

Compile structured output parameters into a grammar.

Args:
    params: Structured output parameters.
    vocab_size: Vocabulary size.
    token_to_string: Function to convert token ID to string.

Returns:
    Compiled grammar, or None if no constraints.

### `validate_structured_output_params(params)`

Validate structured output parameters.

Args:
    params: Parameters to validate.

Returns:
    List of validation error messages (empty if valid).

## Dependencies

**Imports** (16):
- `Base.StructuredOutputGrammar`
- `Base.StructuredOutputOptions`
- `Base.StructuredOutputsParams`
- `EBNFGrammar.EBNFGrammar`
- `JsonConstraint.JSONSchemaGrammar`
- `RegexConstraint.ChoiceGrammar`
- `RegexConstraint.RegexGrammar`
- `__future__.annotations`
- `json`
- `logging`
- `numpy`
- `re`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 1 more

---
*Auto-generated documentation*
