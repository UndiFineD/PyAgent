# registry

**File**: `src\core\base\parsers\reasoning\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 7 imports  
**Lines**: 100  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for registry.

## Classes (1)

### `ReasoningParserManager`

Central registry for ReasoningParser implementations.

**Methods** (6):
- `register_module(cls, name, parser_class)`
- `register_lazy_module(cls, name, module_path, class_name)`
- `get_reasoning_parser(cls, name)`
- `_load_lazy_parser(cls, name)`
- `list_registered(cls)`
- `create_parser(cls, name, tokenizer)`

## Functions (1)

### `reasoning_parser(name)`

Decorator to register a reasoning parser.

## Dependencies

**Imports** (7):
- `base.ReasoningParser`
- `importlib`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.ClassVar`
- `typing.type`

---
*Auto-generated documentation*
