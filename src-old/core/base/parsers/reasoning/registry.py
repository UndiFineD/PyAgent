# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/registry.description.md

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
## Source: src-old/core/base/parsers/reasoning/registry.improvements.md

# Improvements for registry

**File**: `src\core\base\parsers\reasoning\registry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 100 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `registry_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import importlib
import logging
from typing import Any, ClassVar, Callable, Type
from .base import ReasoningParser

logger = logging.getLogger(__name__)


class ReasoningParserManager:
    """
    Central registry for ReasoningParser implementations.
    """

    reasoning_parsers: ClassVar[dict[str, Type[ReasoningParser]]] = {}
    lazy_parsers: ClassVar[dict[str, tuple[str, str]]] = {}  # name -> (module, class)

    @classmethod
    def register_module(cls, name: str, parser_class: Type[ReasoningParser]) -> None:
        """
        Register a parser class.
        """
        cls.reasoning_parsers[name] = parser_class
        logger.debug(f"Registered reasoning parser: {name}")

    @classmethod
    def register_lazy_module(
        cls,
        name: str,
        module_path: str,
        class_name: str,
    ) -> None:
        """
        Register a parser for lazy loading.
        """
        cls.lazy_parsers[name] = (module_path, class_name)
        logger.debug(
            f"Registered lazy reasoning parser: {name} -> {module_path}.{class_name}"
        )

    @classmethod
    def get_reasoning_parser(cls, name: str) -> Type[ReasoningParser]:
        """
        Retrieve a registered parser class.
        """
        if name in cls.reasoning_parsers:
            return cls.reasoning_parsers[name]

        if name in cls.lazy_parsers:
            return cls._load_lazy_parser(name)

        available = cls.list_registered()
        raise KeyError(
            f"Reasoning parser '{name}' not found. "
            f"Available parsers: {', '.join(available)}"
        )

    @classmethod
    def _load_lazy_parser(cls, name: str) -> Type[ReasoningParser]:
        """Import and cache a lazily registered parser."""
        module_path, class_name = cls.lazy_parsers[name]

        module = importlib.import_module(module_path)
        parser_class = getattr(module, class_name)

        # Cache for future access
        cls.reasoning_parsers[name] = parser_class

        logger.debug(f"Loaded lazy reasoning parser: {name}")
        return parser_class

    @classmethod
    def list_registered(cls) -> list[str]:
        """Get names of all registered parsers."""
        return sorted(set(cls.reasoning_parsers.keys()) | set(cls.lazy_parsers.keys()))

    @classmethod
    def create_parser(
        cls,
        name: str,
        tokenizer: Any = None,
        **kwargs: Any,
    ) -> ReasoningParser:
        """
        Create a parser instance.
        """
        parser_cls = cls.get_reasoning_parser(name)
        return parser_cls(tokenizer, **kwargs)


def reasoning_parser(
    name: str,
) -> Callable[[Type[ReasoningParser]], Type[ReasoningParser]]:
    """
    Decorator to register a reasoning parser.
    """

    def decorator(cls: Type[ReasoningParser]) -> Type[ReasoningParser]:
        ReasoningParserManager.register_module(name, cls)
        return cls

    return decorator
