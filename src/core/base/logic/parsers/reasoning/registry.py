# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import importlib
import logging
from typing import Any, ClassVar, Callable, Type
from .base import ReasoningParser

logger = logging.getLogger(__name__)


class ReasoningParserManager:
    """
    Central registry for ReasoningParser implementations.
    """
    
    reasoning_parsers: ClassVar[dict[str, type[ReasoningParser]]] = {}
    lazy_parsers: ClassVar[dict[str, tuple[str, str]]] = {}  # name -> (module, class)
    
    @classmethod
    def register_module(cls, name: str, parser_class: type[ReasoningParser]) -> None:
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
        logger.debug(f"Registered lazy reasoning parser: {name} -> {module_path}.{class_name}")
    
    @classmethod
    def get_reasoning_parser(cls, name: str) -> type[ReasoningParser]:
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
    def _load_lazy_parser(cls, name: str) -> type[ReasoningParser]:
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
        return sorted(
            set(cls.reasoning_parsers.keys()) | set(cls.lazy_parsers.keys())
        )
    
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


def reasoning_parser(name: str) -> Callable[[type[ReasoningParser]], type[ReasoningParser]]:
    """
    Decorator to register a reasoning parser.
    """
    def decorator(cls: type[ReasoningParser]) -> type[ReasoningParser]:
        ReasoningParserManager.register_module(name, cls)
        return cls
    return decorator
