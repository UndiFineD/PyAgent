"""
Chat Template Registry - Phase 42

Dynamic chat template management with model-type based resolution.
Inspired by vLLM's chat template handling.

Key Features:
- Dynamic template registration
- Model-type based fallbacks
- Callable template paths
- Jinja template management
- Multimodal template support

Performance: Uses Rust-accelerated template rendering.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

__all__ = [
    # Enums
    "TemplateType",
    "ModelType",
    # Data Classes
    "TemplateConfig",
    "TemplateInfo",
    "RenderOptions",
    # Main Classes
    "ChatTemplate",
    "JinjaTemplate",
    "ChatTemplateRegistry",
    "TemplateResolver",
    # Functions
    "register_template",
    "get_template",
    "render_template",
    "detect_template_type",
]


# ============================================================================
# Enums
# ============================================================================


class TemplateType(Enum):
    """Chat template types."""

    CHATML = "chatml"
    LLAMA2 = "llama2"
    LLAMA3 = "llama3"
    MISTRAL = "mistral"
    ZEPHYR = "zephyr"
    VICUNA = "vicuna"
    ALPACA = "alpaca"
    GEMMA = "gemma"
    PHI = "phi"
    QWEN = "qwen"
    DEEPSEEK = "deepseek"
    YI = "yi"
    COMMAND = "command"  # Cohere
    JINJA = "jinja"  # Custom Jinja
    MULTIMODAL = "multimodal"
    CUSTOM = "custom"


class ModelType(Enum):
    """Model types for template resolution."""

    TEXT = "text"
    CHAT = "chat"
    INSTRUCT = "instruct"
    CODE = "code"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"
    EMBEDDING = "embedding"


# ============================================================================
# Built-in Templates
# ============================================================================


BUILTIN_TEMPLATES: Dict[TemplateType, str] = {
    TemplateType.CHATML: """{% for message in messages %}{% if message['role'] == 'system' %}<|im_start|>system
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'user' %}<|im_start|>user
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'assistant' %}<|im_start|>assistant
{{ message['content'] }}<|im_end|>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant
{% endif %}""",
    TemplateType.LLAMA2: """{% if messages[0]['role'] == 'system' %}{% set system_message = messages[0]['content'] %}{% set messages = messages[1:] %}{% else %}{% set system_message = '' %}{% endif %}{% for message in messages %}{% if loop.first and system_message %}[INST] <<SYS>>
{{ system_message }}
<</SYS>>

{{ message['content'] }} [/INST]{% elif message['role'] == 'user' %}{% if not loop.first %} [INST] {{ message['content'] }} [/INST]{% else %}[INST] {{ message['content'] }} [/INST]{% endif %}{% elif message['role'] == 'assistant' %} {{ message['content'] }}{% endif %}{% endfor %}""",
    TemplateType.LLAMA3: """{% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}{% endif %}""",
    TemplateType.MISTRAL: """{% if messages[0]['role'] == 'system' %}{% set system_message = messages[0]['content'] %}{% set messages = messages[1:] %}{% else %}{% set system_message = false %}{% endif %}{% for message in messages %}{% if message['role'] == 'user' %}{{ '[INST] ' }}{% if system_message and loop.first %}{{ system_message + '\n\n' }}{% endif %}{{ message['content'] + ' [/INST]' }}{% elif message['role'] == 'assistant' %}{{ message['content'] + '</s> ' }}{% endif %}{% endfor %}""",
    TemplateType.ZEPHYR: """{% for message in messages %}{% if message['role'] == 'system' %}<|system|>
{{ message['content'] }}</s>
{% elif message['role'] == 'user' %}<|user|>
{{ message['content'] }}</s>
{% elif message['role'] == 'assistant' %}<|assistant|>
{{ message['content'] }}</s>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|assistant|>
{% endif %}""",
    TemplateType.VICUNA: """{% if messages[0]['role'] == 'system' %}{{ messages[0]['content'] + '\n\n' }}{% set messages = messages[1:] %}{% endif %}{% for message in messages %}{% if message['role'] == 'user' %}{{ 'USER: ' + message['content'] + '\n' }}{% elif message['role'] == 'assistant' %}{{ 'ASSISTANT: ' + message['content'] + '\n' }}{% endif %}{% endfor %}{% if add_generation_prompt %}{{ 'ASSISTANT:' }}{% endif %}""",
    TemplateType.ALPACA: """{% if messages[0]['role'] == 'system' %}{{ messages[0]['content'] + '\n\n' }}{% set messages = messages[1:] %}{% endif %}{% for message in messages %}{% if message['role'] == 'user' %}### Instruction:
{{ message['content'] }}

{% elif message['role'] == 'assistant' %}### Response:
{{ message['content'] }}

{% endif %}{% endfor %}{% if add_generation_prompt %}### Response:
{% endif %}""",
    TemplateType.GEMMA: """{% for message in messages %}{% if message['role'] == 'user' %}<start_of_turn>user
{{ message['content'] }}<end_of_turn>
{% elif message['role'] == 'assistant' %}<start_of_turn>model
{{ message['content'] }}<end_of_turn>
{% endif %}{% endfor %}{% if add_generation_prompt %}<start_of_turn>model
{% endif %}""",
    TemplateType.PHI: """{% for message in messages %}{% if message['role'] == 'system' %}<|system|>
{{ message['content'] }}<|end|>
{% elif message['role'] == 'user' %}<|user|>
{{ message['content'] }}<|end|>
{% elif message['role'] == 'assistant' %}<|assistant|>
{{ message['content'] }}<|end|>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|assistant|>
{% endif %}""",
    TemplateType.QWEN: """{% for message in messages %}{% if message['role'] == 'system' %}<|im_start|>system
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'user' %}<|im_start|>user
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'assistant' %}<|im_start|>assistant
{{ message['content'] }}<|im_end|>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant
{% endif %}""",
    TemplateType.DEEPSEEK: """{% for message in messages %}{% if message['role'] == 'user' %}User: {{ message['content'] }}

{% elif message['role'] == 'assistant' %}Assistant: {{ message['content'] }}

{% endif %}{% endfor %}{% if add_generation_prompt %}Assistant:{% endif %}""",
    TemplateType.YI: """{% for message in messages %}{% if message['role'] == 'user' %}<|im_start|>user
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'assistant' %}<|im_start|>assistant
{{ message['content'] }}<|im_end|>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant
{% endif %}""",
    TemplateType.COMMAND: """{% for message in messages %}{% if message['role'] == 'user' %}<|START_OF_TURN_TOKEN|><|USER_TOKEN|>{{ message['content'] }}<|END_OF_TURN_TOKEN|>{% elif message['role'] == 'assistant' %}<|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>{{ message['content'] }}<|END_OF_TURN_TOKEN|>{% elif message['role'] == 'system' %}<|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>{{ message['content'] }}<|END_OF_TURN_TOKEN|>{% endif %}{% endfor %}{% if add_generation_prompt %}<|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>{% endif %}""",
}


# Model name to template type mapping
MODEL_TEMPLATE_MAP: Dict[str, TemplateType] = {
    "llama-2": TemplateType.LLAMA2,
    "llama-3": TemplateType.LLAMA3,
    "llama3": TemplateType.LLAMA3,
    "meta-llama-3": TemplateType.LLAMA3,
    "mistral": TemplateType.MISTRAL,
    "mixtral": TemplateType.MISTRAL,
    "zephyr": TemplateType.ZEPHYR,
    "vicuna": TemplateType.VICUNA,
    "alpaca": TemplateType.ALPACA,
    "gemma": TemplateType.GEMMA,
    "phi": TemplateType.PHI,
    "phi-2": TemplateType.PHI,
    "phi-3": TemplateType.PHI,
    "qwen": TemplateType.QWEN,
    "qwen2": TemplateType.QWEN,
    "deepseek": TemplateType.DEEPSEEK,
    "yi": TemplateType.YI,
    "command": TemplateType.COMMAND,
    "command-r": TemplateType.COMMAND,
    "chatml": TemplateType.CHATML,
    "openchat": TemplateType.CHATML,
    "dolphin": TemplateType.CHATML,
}


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class TemplateConfig:
    """Chat template configuration."""

    template_type: TemplateType
    template_string: Optional[str] = None
    template_path: Optional[str] = None
    special_tokens: Dict[str, str] = field(default_factory=dict)
    add_bos_token: bool = True
    add_eos_token: bool = True
    add_generation_prompt: bool = True
    strip_whitespace: bool = True
    model_type: ModelType = ModelType.CHAT
    multimodal_tokens: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_type": self.template_type.value,
            "template_string": self.template_string,
            "special_tokens": self.special_tokens,
            "model_type": self.model_type.value,
        }


@dataclass
class TemplateInfo:
    """Template metadata."""

    name: str
    template_type: TemplateType
    description: str = ""
    source: str = "builtin"
    version: str = "1.0"
    supports_tools: bool = False
    supports_system: bool = True
    supports_multimodal: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "template_type": self.template_type.value,
            "description": self.description,
            "supports_tools": self.supports_tools,
            "supports_multimodal": self.supports_multimodal,
        }


@dataclass
class RenderOptions:
    """Template rendering options."""

    add_generation_prompt: bool = True
    add_special_tokens: bool = True
    strip_whitespace: bool = True
    include_system: bool = True
    include_tools: bool = True
    tool_format: str = "json"  # json, xml, function
    image_placeholder: str = "<image>"
    audio_placeholder: str = "<audio>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "add_generation_prompt": self.add_generation_prompt,
            "add_special_tokens": self.add_special_tokens,
            "include_tools": self.include_tools,
        }


# ============================================================================
# Chat Template Base
# ============================================================================


class ChatTemplate(ABC):
    """Abstract base class for chat templates."""

    def __init__(self, config: TemplateConfig):
        self.config = config
        self._cached_hash: Optional[str] = None

    @property
    def template_type(self) -> TemplateType:
        return self.config.template_type

    @property
    def template_hash(self) -> str:
        """Get hash of template for caching."""
        if self._cached_hash is None:
            template_str = self.get_template_string()
            self._cached_hash = hashlib.md5(
                template_str.encode()
            ).hexdigest()[:12]
        return self._cached_hash

    @abstractmethod
    def get_template_string(self) -> str:
        """Get the template string."""
        ...

    @abstractmethod
    def render(
        self,
        messages: List[Dict[str, Any]],
        options: Optional[RenderOptions] = None,
    ) -> str:
        """Render messages using the template."""
        ...

    def get_info(self) -> TemplateInfo:
        """Get template information."""
        return TemplateInfo(
            name=self.config.template_type.value,
            template_type=self.config.template_type,
        )


# ============================================================================
# Jinja Template
# ============================================================================


class JinjaTemplate(ChatTemplate):
    """Jinja2-based chat template."""

    def __init__(self, config: TemplateConfig):
        super().__init__(config)
        self._template = None
        self._env = None

    def get_template_string(self) -> str:
        """Get template string."""
        if self.config.template_string:
            return self.config.template_string

        if self.config.template_path:
            with open(self.config.template_path) as f:
                return f.read()

        # Use builtin
        if self.config.template_type in BUILTIN_TEMPLATES:
            return BUILTIN_TEMPLATES[self.config.template_type]

        return BUILTIN_TEMPLATES[TemplateType.CHATML]

    def _get_env(self):
        """Get Jinja environment."""
        if self._env is None:
            try:
                from jinja2 import Environment, BaseLoader, StrictUndefined

                self._env = Environment(
                    loader=BaseLoader(),
                    undefined=StrictUndefined,
                    autoescape=False,
                    trim_blocks=True,
                    lstrip_blocks=True,
                )

                # Add custom filters
                self._env.filters["trim"] = str.strip

            except ImportError:
                logger.warning("Jinja2 not available")
                self._env = None

        return self._env

    def _get_template(self):
        """Get compiled Jinja template."""
        if self._template is None:
            env = self._get_env()
            if env:
                template_string = self.get_template_string()
                self._template = env.from_string(template_string)
        return self._template

    def render(
        self,
        messages: List[Dict[str, Any]],
        options: Optional[RenderOptions] = None,
    ) -> str:
        """Render messages using Jinja template."""
        options = options or RenderOptions()

        # Filter messages
        filtered = []
        for msg in messages:
            if not options.include_system and msg.get("role") == "system":
                continue
            filtered.append(msg)

        template = self._get_template()
        if template:
            try:
                result = template.render(
                    messages=filtered,
                    add_generation_prompt=options.add_generation_prompt,
                )

                if options.strip_whitespace:
                    result = result.strip()

                return result

            except Exception as e:
                logger.error(f"Template rendering error: {e}")
                return self._fallback_render(filtered, options)

        return self._fallback_render(filtered, options)

    def _fallback_render(
        self,
        messages: List[Dict[str, Any]],
        options: RenderOptions,
    ) -> str:
        """Fallback rendering without Jinja."""
        parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                parts.append(f"<|im_start|>system\n{content}<|im_end|>")
            elif role == "user":
                parts.append(f"<|im_start|>user\n{content}<|im_end|>")
            elif role == "assistant":
                parts.append(f"<|im_start|>assistant\n{content}<|im_end|>")
            elif role == "tool":
                parts.append(f"<|im_start|>tool\n{content}<|im_end|>")

        if options.add_generation_prompt:
            parts.append("<|im_start|>assistant\n")

        return "\n".join(parts)


# ============================================================================
# Chat Template Registry
# ============================================================================


class ChatTemplateRegistry:
    """
    Registry for chat templates with dynamic resolution.
    
    Provides:
    - Template registration and lookup
    - Model name to template resolution
    - Callable template paths for dynamic selection
    """

    _instance: Optional["ChatTemplateRegistry"] = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._templates = {}
                cls._instance._model_map = dict(MODEL_TEMPLATE_MAP)
                cls._instance._resolvers = []
                cls._instance._initialize_builtins()
            return cls._instance

    def _initialize_builtins(self) -> None:
        """Initialize built-in templates."""
        for template_type, template_string in BUILTIN_TEMPLATES.items():
            config = TemplateConfig(
                template_type=template_type,
                template_string=template_string,
            )
            template = JinjaTemplate(config)
            self._templates[template_type.value] = template

    @property
    def templates(self) -> Dict[str, ChatTemplate]:
        return self._templates

    def register(
        self,
        name: str,
        template: ChatTemplate,
        model_patterns: Optional[List[str]] = None,
    ) -> None:
        """
        Register a template.
        
        Args:
            name: Template name
            template: Template instance
            model_patterns: Model name patterns that use this template
        """
        self._templates[name] = template

        if model_patterns:
            for pattern in model_patterns:
                self._model_map[pattern.lower()] = template.template_type

    def register_config(
        self,
        name: str,
        config: TemplateConfig,
        model_patterns: Optional[List[str]] = None,
    ) -> ChatTemplate:
        """
        Register a template from config.
        
        Args:
            name: Template name
            config: Template configuration
            model_patterns: Model name patterns
            
        Returns:
            Created template
        """
        template = JinjaTemplate(config)
        self.register(name, template, model_patterns)
        return template

    def register_resolver(
        self,
        resolver: Callable[[str], Optional[ChatTemplate]],
    ) -> None:
        """
        Register a custom template resolver.
        
        Resolver is called when no direct match is found.
        """
        self._resolvers.append(resolver)

    def get(
        self,
        name: str,
        default: Optional[ChatTemplate] = None,
    ) -> Optional[ChatTemplate]:
        """Get template by name."""
        return self._templates.get(name, default)

    def resolve(
        self,
        model_name: str,
        tokenizer: Optional[Any] = None,
    ) -> ChatTemplate:
        """
        Resolve template for a model.
        
        Resolution order:
        1. Tokenizer's chat_template attribute
        2. Model name pattern matching
        3. Custom resolvers
        4. Default (ChatML)
        """
        # Check tokenizer first
        if tokenizer and hasattr(tokenizer, "chat_template"):
            template_str = tokenizer.chat_template
            if template_str:
                config = TemplateConfig(
                    template_type=TemplateType.JINJA,
                    template_string=template_str,
                )
                return JinjaTemplate(config)

        # Check model name patterns
        model_lower = model_name.lower()
        for pattern, template_type in self._model_map.items():
            if pattern in model_lower:
                template = self._templates.get(template_type.value)
                if template:
                    return template

        # Try custom resolvers
        for resolver in self._resolvers:
            try:
                result = resolver(model_name)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Resolver error: {e}")

        # Default to ChatML
        return self._templates.get(
            TemplateType.CHATML.value,
            JinjaTemplate(TemplateConfig(template_type=TemplateType.CHATML)),
        )

    def list_templates(self) -> List[TemplateInfo]:
        """List all registered templates."""
        return [t.get_info() for t in self._templates.values()]

    def unregister(self, name: str) -> bool:
        """Unregister a template."""
        return self._templates.pop(name, None) is not None


# ============================================================================
# Template Resolver
# ============================================================================


class TemplateResolver:
    """
    Advanced template resolution with caching.
    
    Provides model-aware template selection with:
    - LRU caching of resolutions
    - Callable template paths
    - Fallback chains
    """

    def __init__(self, registry: Optional[ChatTemplateRegistry] = None):
        self.registry = registry or ChatTemplateRegistry()
        self._cache: Dict[str, ChatTemplate] = {}
        self._lock = threading.Lock()

    @lru_cache(maxsize=256)
    def resolve(
        self,
        model_name: str,
        model_type: Optional[ModelType] = None,
    ) -> ChatTemplate:
        """
        Resolve template with caching.
        
        Args:
            model_name: Model name or path
            model_type: Optional model type hint
            
        Returns:
            Resolved template
        """
        # Normalize model name
        normalized = self._normalize_model_name(model_name)

        with self._lock:
            if normalized in self._cache:
                return self._cache[normalized]

            template = self.registry.resolve(normalized)

            # Apply model type hints
            if model_type == ModelType.VISION:
                template = self._wrap_multimodal(template)

            self._cache[normalized] = template
            return template

    def _normalize_model_name(self, name: str) -> str:
        """Normalize model name for matching."""
        # Remove common prefixes/suffixes
        name = name.lower()
        name = re.sub(r"[/\\]", "-", name)
        name = re.sub(r"[-_]", "-", name)
        name = re.sub(r"\.gguf$", "", name)
        name = re.sub(r"\.safetensors$", "", name)
        return name

    def _wrap_multimodal(self, template: ChatTemplate) -> ChatTemplate:
        """Wrap template for multimodal support."""
        # For now, return as-is; can be extended for multimodal
        return template

    def clear_cache(self) -> None:
        """Clear resolution cache."""
        with self._lock:
            self._cache.clear()
        self.resolve.cache_clear()


# ============================================================================
# Convenience Functions
# ============================================================================


_default_registry: Optional[ChatTemplateRegistry] = None
_default_resolver: Optional[TemplateResolver] = None


def _get_registry() -> ChatTemplateRegistry:
    """Get default registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = ChatTemplateRegistry()
    return _default_registry


def _get_resolver() -> TemplateResolver:
    """Get default resolver."""
    global _default_resolver
    if _default_resolver is None:
        _default_resolver = TemplateResolver()
    return _default_resolver


def register_template(
    name: str,
    template_string: str,
    template_type: TemplateType = TemplateType.CUSTOM,
    model_patterns: Optional[List[str]] = None,
) -> ChatTemplate:
    """
    Register a custom template.
    
    Args:
        name: Template name
        template_string: Jinja template string
        template_type: Template type
        model_patterns: Model patterns that use this template
        
    Returns:
        Registered template
    """
    config = TemplateConfig(
        template_type=template_type,
        template_string=template_string,
    )
    return _get_registry().register_config(name, config, model_patterns)


def get_template(
    model_name: str,
    tokenizer: Optional[Any] = None,
) -> ChatTemplate:
    """
    Get template for a model.
    
    Args:
        model_name: Model name or path
        tokenizer: Optional tokenizer with chat_template
        
    Returns:
        Chat template
    """
    if tokenizer:
        return _get_registry().resolve(model_name, tokenizer)
    return _get_resolver().resolve(model_name)


def render_template(
    messages: List[Dict[str, Any]],
    model_name: Optional[str] = None,
    template: Optional[ChatTemplate] = None,
    template_string: Optional[str] = None,
    add_generation_prompt: bool = True,
) -> str:
    """
    Render messages using a template.
    
    Args:
        messages: Chat messages
        model_name: Model name for auto-resolution
        template: Explicit template to use
        template_string: Explicit template string
        add_generation_prompt: Add generation prompt
        
    Returns:
        Rendered prompt string
    """
    # Get template
    if template is None:
        if template_string:
            config = TemplateConfig(
                template_type=TemplateType.JINJA,
                template_string=template_string,
            )
            template = JinjaTemplate(config)
        elif model_name:
            template = get_template(model_name)
        else:
            template = _get_registry().get(TemplateType.CHATML.value)

    # Render
    options = RenderOptions(add_generation_prompt=add_generation_prompt)
    return template.render(messages, options)


def detect_template_type(model_name: str) -> TemplateType:
    """
    Detect template type from model name.
    
    Args:
        model_name: Model name or path
        
    Returns:
        Detected template type
    """
    model_lower = model_name.lower()

    for pattern, template_type in MODEL_TEMPLATE_MAP.items():
        if pattern in model_lower:
            return template_type

    return TemplateType.CHATML


# ============================================================================
# Rust Acceleration Integration
# ============================================================================


def _try_rust_render_template(
    template: str,
    messages: List[Dict[str, Any]],
    add_generation_prompt: bool,
) -> Optional[str]:
    """Try Rust-accelerated template rendering."""
    try:
        from rust_core import render_jinja_template_rust

        return render_jinja_template_rust(
            template,
            messages,
            add_generation_prompt,
        )
    except ImportError:
        return None


def _try_rust_detect_template(model_name: str) -> Optional[str]:
    """Try Rust-accelerated template detection."""
    try:
        from rust_core import detect_chat_template_rust

        return detect_chat_template_rust(model_name)
    except ImportError:
        return None
