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
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Guided Decoding for vLLM.

Provides structured output generation through:
- JSON schema constraints
- Regex pattern matching
- Choice/enum constraints
- Grammar-based generation

Inspired by vLLM's guided decoding and outlines integration.
"""

from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
)

# Check vLLM availability
try:
    from vllm import SamplingParams
    from vllm import LLM
    
    HAS_VLLM = True
except ImportError:
    HAS_VLLM = False
    SamplingParams = None
    LLM = None

# Check outlines availability (optional enhanced grammar support)
try:
    import outlines
    
    HAS_OUTLINES = True
except ImportError:
    HAS_OUTLINES = False

T = TypeVar('T')


class GuidedMode(Enum):
    """Mode of guided decoding."""
    NONE = auto()
    JSON = auto()
    JSON_OBJECT = auto()
    REGEX = auto()
    CHOICE = auto()
    GRAMMAR = auto()


@dataclass
class GuidedConfig:
    """Configuration for guided decoding."""
    
    mode: GuidedMode = GuidedMode.NONE
    
    # JSON mode
    json_schema: Optional[Dict[str, Any]] = None
    json_object: bool = False  # Simple JSON object mode
    
    # Regex mode
    regex_pattern: Optional[str] = None
    
    # Choice mode
    choices: Optional[List[str]] = None
    
    # Grammar mode (EBNF/CFG)
    grammar: Optional[str] = None
    
    # Advanced options
    whitespace_pattern: Optional[str] = None
    strict: bool = True  # Fail on constraint violations
    
    def to_sampling_params_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs for SamplingParams."""
        kwargs = {}
        
        if self.mode == GuidedMode.JSON and self.json_schema:
            kwargs["guided_json"] = self.json_schema
        elif self.mode == GuidedMode.JSON_OBJECT:
            kwargs["guided_json"] = {}  # Empty schema = any valid JSON object
        elif self.mode == GuidedMode.REGEX and self.regex_pattern:
            kwargs["guided_regex"] = self.regex_pattern
        elif self.mode == GuidedMode.CHOICE and self.choices:
            kwargs["guided_choice"] = self.choices
        elif self.mode == GuidedMode.GRAMMAR and self.grammar:
            kwargs["guided_grammar"] = self.grammar
        
        if self.whitespace_pattern:
            kwargs["guided_whitespace_pattern"] = self.whitespace_pattern
        
        return kwargs


@dataclass
class JsonSchema:
    """
    JSON Schema builder for guided decoding.
    
    Provides a fluent API for constructing JSON schemas.
    
    Example:
        schema = (JsonSchema()
            .add_property("name", "string", required=True)
            .add_property("age", "integer", minimum=0)
            .add_property("tags", "array", items={"type": "string"})
            .build())
    """
    
    title: Optional[str] = None
    description: Optional[str] = None
    properties: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    additional_properties: bool = False
    
    def add_property(
        self,
        name: str,
        prop_type: str,
        required: bool = False,
        description: Optional[str] = None,
        enum: Optional[List[Any]] = None,
        minimum: Optional[Union[int, float]] = None,
        maximum: Optional[Union[int, float]] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        items: Optional[Dict[str, Any]] = None,
        default: Optional[Any] = None,
        **kwargs,
    ) -> "JsonSchema":
        """Add a property to the schema."""
        prop: Dict[str, Any] = {"type": prop_type}
        
        if description:
            prop["description"] = description
        if enum is not None:
            prop["enum"] = enum
        if minimum is not None:
            prop["minimum"] = minimum
        if maximum is not None:
            prop["maximum"] = maximum
        if min_length is not None:
            prop["minLength"] = min_length
        if max_length is not None:
            prop["maxLength"] = max_length
        if pattern:
            prop["pattern"] = pattern
        if items:
            prop["items"] = items
        if default is not None:
            prop["default"] = default
        
        prop.update(kwargs)
        
        self.properties[name] = prop
        
        if required and name not in self.required:
            self.required.append(name)
        
        return self
    
    def add_string(
        self,
        name: str,
        required: bool = False,
        **kwargs,
    ) -> "JsonSchema":
        """Add a string property."""
        return self.add_property(name, "string", required=required, **kwargs)
    
    def add_integer(
        self,
        name: str,
        required: bool = False,
        **kwargs,
    ) -> "JsonSchema":
        """Add an integer property."""
        return self.add_property(name, "integer", required=required, **kwargs)
    
    def add_number(
        self,
        name: str,
        required: bool = False,
        **kwargs,
    ) -> "JsonSchema":
        """Add a number property."""
        return self.add_property(name, "number", required=required, **kwargs)
    
    def add_boolean(
        self,
        name: str,
        required: bool = False,
        **kwargs,
    ) -> "JsonSchema":
        """Add a boolean property."""
        return self.add_property(name, "boolean", required=required, **kwargs)
    
    def add_array(
        self,
        name: str,
        items_type: str = "string",
        required: bool = False,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        **kwargs,
    ) -> "JsonSchema":
        """Add an array property."""
        items = {"type": items_type}
        extra = {}
        if min_items is not None:
            extra["minItems"] = min_items
        if max_items is not None:
            extra["maxItems"] = max_items
        
        return self.add_property(
            name, "array", required=required, items=items, **extra, **kwargs
        )
    
    def add_object(
        self,
        name: str,
        nested_schema: "JsonSchema",
        required: bool = False,
    ) -> "JsonSchema":
        """Add a nested object property."""
        self.properties[name] = nested_schema.build()
        if required and name not in self.required:
            self.required.append(name)
        return self
    
    def add_enum(
        self,
        name: str,
        values: List[Any],
        required: bool = False,
        **kwargs,
    ) -> "JsonSchema":
        """Add an enum property."""
        # Infer type from first value
        if values:
            first = values[0]
            if isinstance(first, str):
                prop_type = "string"
            elif isinstance(first, bool):
                prop_type = "boolean"
            elif isinstance(first, int):
                prop_type = "integer"
            elif isinstance(first, float):
                prop_type = "number"
            else:
                prop_type = "string"
        else:
            prop_type = "string"
        
        return self.add_property(
            name, prop_type, required=required, enum=values, **kwargs
        )
    
    def build(self) -> Dict[str, Any]:
        """Build the JSON schema dictionary."""
        schema: Dict[str, Any] = {
            "type": "object",
            "properties": self.properties,
        }
        
        if self.title:
            schema["title"] = self.title
        if self.description:
            schema["description"] = self.description
        if self.required:
            schema["required"] = self.required
        if not self.additional_properties:
            schema["additionalProperties"] = False
        
        return schema
    
    def to_guided_config(self) -> GuidedConfig:
        """Convert to GuidedConfig for use with decoder."""
        return GuidedConfig(
            mode=GuidedMode.JSON,
            json_schema=self.build(),
        )


@dataclass
class RegexPattern:
    """
    Regex pattern builder for guided decoding.
    
    Provides common patterns and composition utilities.
    """
    
    pattern: str
    name: Optional[str] = None
    description: Optional[str] = None
    
    # Common patterns
    EMAIL = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    PHONE_US = r"\d{3}-\d{3}-\d{4}"
    URL = r"https?://[^\s]+"
    IPV4 = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    DATE_ISO = r"\d{4}-\d{2}-\d{2}"
    TIME_24H = r"[0-2][0-9]:[0-5][0-9]"
    HEX_COLOR = r"#[0-9A-Fa-f]{6}"
    UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    
    # Programming patterns
    IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"
    PYTHON_VARIABLE = r"[a-z_][a-z0-9_]*"
    CLASS_NAME = r"[A-Z][a-zA-Z0-9]*"
    
    def __post_init__(self):
        # Validate regex
        try:
            re.compile(self.pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    
    def to_guided_config(self) -> GuidedConfig:
        """Convert to GuidedConfig for use with decoder."""
        return GuidedConfig(
            mode=GuidedMode.REGEX,
            regex_pattern=self.pattern,
        )
    
    @classmethod
    def email(cls) -> "RegexPattern":
        """Create email pattern."""
        return cls(pattern=cls.EMAIL, name="email")
    
    @classmethod
    def phone_us(cls) -> "RegexPattern":
        """Create US phone pattern."""
        return cls(pattern=cls.PHONE_US, name="phone_us")
    
    @classmethod
    def url(cls) -> "RegexPattern":
        """Create URL pattern."""
        return cls(pattern=cls.URL, name="url")
    
    @classmethod
    def date_iso(cls) -> "RegexPattern":
        """Create ISO date pattern."""
        return cls(pattern=cls.DATE_ISO, name="date_iso")
    
    @classmethod
    def one_of(cls, *patterns: str) -> "RegexPattern":
        """Create pattern matching any of the given patterns."""
        combined = "|".join(f"({p})" for p in patterns)
        return cls(pattern=combined, name="one_of")
    
    @classmethod
    def sequence(cls, *patterns: str, separator: str = "") -> "RegexPattern":
        """Create pattern matching sequence of patterns."""
        combined = separator.join(patterns)
        return cls(pattern=combined, name="sequence")


@dataclass
class ChoiceConstraint:
    """
    Choice constraint for limiting output to specific options.
    
    Example:
        constraint = ChoiceConstraint(["yes", "no", "maybe"])
        config = constraint.to_guided_config()
    """
    
    choices: List[str]
    case_sensitive: bool = True
    
    def __post_init__(self):
        if not self.choices:
            raise ValueError("At least one choice is required")
    
    def to_guided_config(self) -> GuidedConfig:
        """Convert to GuidedConfig for use with decoder."""
        return GuidedConfig(
            mode=GuidedMode.CHOICE,
            choices=self.choices,
        )
    
    @classmethod
    def yes_no(cls) -> "ChoiceConstraint":
        """Create yes/no constraint."""
        return cls(["yes", "no"])
    
    @classmethod
    def true_false(cls) -> "ChoiceConstraint":
        """Create true/false constraint."""
        return cls(["true", "false"])
    
    @classmethod
    def sentiment(cls) -> "ChoiceConstraint":
        """Create sentiment constraint."""
        return cls(["positive", "negative", "neutral"])
    
    @classmethod
    def rating(cls, min_val: int = 1, max_val: int = 5) -> "ChoiceConstraint":
        """Create numeric rating constraint."""
        return cls([str(i) for i in range(min_val, max_val + 1)])


class GuidedDecoder:
    """
    Guided decoding engine for structured output generation.
    
    Provides:
    - JSON schema-constrained generation
    - Regex pattern matching
    - Choice/enum constraints
    - Grammar-based generation
    
    Example:
        decoder = GuidedDecoder(model="meta-llama/Llama-3-8B")
        
        # JSON output
        schema = (JsonSchema()
            .add_string("name", required=True)
            .add_integer("age", minimum=0)
            .build())
        
        result = decoder.generate_json(
            "Extract person info from: John is 25 years old.",
            schema=schema,
        )
        # {"name": "John", "age": 25}
        
        # Choice constraint
        result = decoder.generate_choice(
            "Is this sentiment positive or negative: I love this!",
            choices=["positive", "negative"],
        )
        # "positive"
    """
    
    _instance: Optional["GuidedDecoder"] = None
    
    def __init__(
        self,
        model: str = "meta-llama/Llama-3-8B-Instruct",
        gpu_memory_utilization: float = 0.85,
        **llm_kwargs,
    ):
        self.model = model
        self.gpu_memory_utilization = gpu_memory_utilization
        self._llm_kwargs = llm_kwargs
        self._llm: Optional[LLM] = None
        self._initialized = False
        
        # Stats
        self._stats = {
            "json_generations": 0,
            "regex_generations": 0,
            "choice_generations": 0,
            "grammar_generations": 0,
            "validation_failures": 0,
        }
    
    @classmethod
    def get_instance(cls, **kwargs) -> "GuidedDecoder":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = GuidedDecoder(**kwargs)
        return cls._instance
    
    @property
    def is_available(self) -> bool:
        """Check if guided decoding is available."""
        return HAS_VLLM
    
    def _ensure_initialized(self) -> bool:
        """Lazily initialize the LLM."""
        if not HAS_VLLM:
            logging.warning("vLLM not available for guided decoding")
            return False
        
        if self._initialized and self._llm:
            return True
        
        try:
            import os
            import torch
            
            if "VLLM_TARGET_DEVICE" not in os.environ:
                if torch.cuda.is_available():
                    os.environ["VLLM_TARGET_DEVICE"] = "cuda"
                else:
                    os.environ["VLLM_TARGET_DEVICE"] = "cpu"
            
            logging.info(f"Initializing GuidedDecoder with model: {self.model}")
            
            kwargs = {
                "model": self.model,
                "trust_remote_code": True,
                **self._llm_kwargs,
            }
            
            if os.environ.get("VLLM_TARGET_DEVICE") != "cpu":
                kwargs["gpu_memory_utilization"] = self.gpu_memory_utilization
            else:
                kwargs["device"] = "cpu"
            
            self._llm = LLM(**kwargs)
            self._initialized = True
            
            logging.info("GuidedDecoder initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize GuidedDecoder: {e}")
            return False
    
    def generate(
        self,
        prompt: str,
        config: GuidedConfig,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate with guided decoding configuration.
        
        Args:
            prompt: Input prompt
            config: Guided decoding configuration
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            
        Returns:
            Generated text constrained by the configuration
        """
        if not self._ensure_initialized():
            return ""
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        
        try:
            # Build sampling params with guided decoding kwargs
            guided_kwargs = config.to_sampling_params_kwargs()
            
            sampling_params = SamplingParams(
                temperature=temperature,
                max_tokens=max_tokens,
                **guided_kwargs,
                **kwargs,
            )
            
            outputs = self._llm.generate(
                [full_prompt],
                sampling_params,
                use_tqdm=False,
            )
            
            if outputs and outputs[0].outputs:
                return outputs[0].outputs[0].text
            
            return ""
            
        except Exception as e:
            logging.error(f"Guided generation failed: {e}")
            return ""
    
    def generate_json(
        self,
        prompt: str,
        schema: Optional[Union[Dict[str, Any], JsonSchema]] = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        parse: bool = True,
        **kwargs,
    ) -> Union[Dict[str, Any], str]:
        """
        Generate JSON output constrained by schema.
        
        Args:
            prompt: Input prompt
            schema: JSON schema (dict or JsonSchema object)
            temperature: Sampling temperature (lower for structured)
            max_tokens: Maximum tokens
            system_prompt: Optional system prompt
            parse: Whether to parse and return dict (True) or raw string
            
        Returns:
            Parsed JSON dict if parse=True, else raw JSON string
        """
        if isinstance(schema, JsonSchema):
            schema = schema.build()
        
        config = GuidedConfig(
            mode=GuidedMode.JSON if schema else GuidedMode.JSON_OBJECT,
            json_schema=schema,
        )
        
        # Add JSON instruction to system prompt
        json_system = "You must respond with valid JSON only. No explanations."
        if system_prompt:
            json_system = f"{system_prompt}\n\n{json_system}"
        
        result = self.generate(
            prompt,
            config=config,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=json_system,
            **kwargs,
        )
        
        self._stats["json_generations"] += 1
        
        if parse and result:
            try:
                return json.loads(result)
            except json.JSONDecodeError as e:
                self._stats["validation_failures"] += 1
                logging.warning(f"Failed to parse JSON output: {e}")
                return result
        
        return result
    
    def generate_regex(
        self,
        prompt: str,
        pattern: Union[str, RegexPattern],
        temperature: float = 0.5,
        max_tokens: int = 256,
        system_prompt: Optional[str] = None,
        validate: bool = True,
        **kwargs,
    ) -> str:
        """
        Generate output matching a regex pattern.
        
        Args:
            prompt: Input prompt
            pattern: Regex pattern (string or RegexPattern)
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            system_prompt: Optional system prompt
            validate: Whether to validate output against pattern
            
        Returns:
            Generated text matching the pattern
        """
        if isinstance(pattern, RegexPattern):
            pattern_str = pattern.pattern
        else:
            pattern_str = pattern
        
        config = GuidedConfig(
            mode=GuidedMode.REGEX,
            regex_pattern=pattern_str,
        )
        
        result = self.generate(
            prompt,
            config=config,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            **kwargs,
        )
        
        self._stats["regex_generations"] += 1
        
        if validate and result:
            if not re.match(pattern_str, result):
                self._stats["validation_failures"] += 1
                logging.warning(f"Output doesn't match pattern: {pattern_str}")
        
        return result
    
    def generate_choice(
        self,
        prompt: str,
        choices: Union[List[str], ChoiceConstraint],
        temperature: float = 0.0,  # Deterministic for choices
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate output constrained to specific choices.
        
        Args:
            prompt: Input prompt
            choices: List of allowed choices or ChoiceConstraint
            temperature: Sampling temperature (0 for deterministic)
            system_prompt: Optional system prompt
            
        Returns:
            One of the specified choices
        """
        if isinstance(choices, ChoiceConstraint):
            choice_list = choices.choices
        else:
            choice_list = choices
        
        config = GuidedConfig(
            mode=GuidedMode.CHOICE,
            choices=choice_list,
        )
        
        # Add choice instruction
        choice_prompt = f"{prompt}\n\nRespond with exactly one of: {', '.join(choice_list)}"
        
        result = self.generate(
            choice_prompt,
            config=config,
            temperature=temperature,
            max_tokens=len(max(choice_list, key=len)) + 5,
            system_prompt=system_prompt,
            **kwargs,
        )
        
        self._stats["choice_generations"] += 1
        
        return result.strip()
    
    def generate_grammar(
        self,
        prompt: str,
        grammar: str,
        temperature: float = 0.5,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate output following a grammar specification.
        
        Args:
            prompt: Input prompt
            grammar: Grammar specification (EBNF/CFG format)
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            system_prompt: Optional system prompt
            
        Returns:
            Generated text following the grammar
        """
        config = GuidedConfig(
            mode=GuidedMode.GRAMMAR,
            grammar=grammar,
        )
        
        result = self.generate(
            prompt,
            config=config,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            **kwargs,
        )
        
        self._stats["grammar_generations"] += 1
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get decoder statistics."""
        return {
            **self._stats,
            "is_initialized": self._initialized,
            "has_outlines": HAS_OUTLINES,
        }
    
    def shutdown(self) -> None:
        """Shutdown and free resources."""
        if self._llm:
            import gc
            del self._llm
            self._llm = None
            gc.collect()
            
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except ImportError:
                pass
            
            self._initialized = False
            logging.info("GuidedDecoder shut down")


# Convenience functions
def generate_json(
    prompt: str,
    schema: Union[Dict[str, Any], JsonSchema],
    model: str = "meta-llama/Llama-3-8B-Instruct",
    **kwargs,
) -> Dict[str, Any]:
    """Convenience function for JSON generation."""
    decoder = GuidedDecoder.get_instance(model=model)
    return decoder.generate_json(prompt, schema, **kwargs)


def generate_choice(
    prompt: str,
    choices: List[str],
    model: str = "meta-llama/Llama-3-8B-Instruct",
    **kwargs,
) -> str:
    """Convenience function for choice generation."""
    decoder = GuidedDecoder.get_instance(model=model)
    return decoder.generate_choice(prompt, choices, **kwargs)
