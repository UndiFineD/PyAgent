# EBNFGrammar

**File**: `src\infrastructure\decoding\grammar\EBNFGrammar.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 192  
**Complexity**: 12 (moderate)

## Overview

EBNF grammar constraint logic for structured output decoding.

## Classes (2)

### `GrammarRule`

A single EBNF grammar rule.

### `EBNFGrammar`

**Inherits from**: StructuredOutputGrammar

Grammar that constrains output using EBNF rules.

Supports simple context-free grammars for SQL, code, etc.
Inspired by vLLM's xgrammar EBNF support.

**Methods** (12):
- `__post_init__(self)`
- `_parse_grammar(self)`
- `_get_valid_prefixes(self, symbol)`
- `accept_tokens(self, request_id, tokens)`
- `_is_valid_grammar_prefix(self, text)`
- `validate_tokens(self, tokens)`
- `rollback(self, num_tokens)`
- `fill_bitmask(self, bitmask, idx)`
- `get_valid_tokens(self)`
- `is_terminated(self)`
- ... and 2 more methods

## Dependencies

**Imports** (9):
- `Base.StructuredOutputGrammar`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
