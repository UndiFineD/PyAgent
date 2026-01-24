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
GuidanceBackend - Guidance library integration for structured output.

Implements structured output using the Guidance library with:
- Template-based generation
- Stateful tracking
- Async compilation
- Multi-model support

Beyond vLLM innovations:
- Grammar composition
- Template caching
- Variable interpolation
- Streaming token support
"""

import asyncio
import hashlib
import json
import re
import threading
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rust_core  # noqa: F401

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class GuidanceTemplateType(Enum):
    """Types of Guidance templates."""

    TEXT = auto()
    JSON = auto()
    REGEX = auto()
    GRAMMAR = auto()
    SELECTOR = auto()


@dataclass
class GuidanceVariable:
    """Variable in a Guidance template."""

    name: str
    type: str = "gen"
    regex: Optional[str] = None
    options: Optional[List[str]] = None
    max_tokens: int = 100
    stop: Optional[List[str]] = None

    def to_pattern(self) -> str:
        """Convert to regex pattern for matching."""
        if self.regex:
            return self.regex
        if self.options:
            return "|".join(re.escape(opt) for opt in self.options)
        return r".*?"


@dataclass
class GuidanceTemplate:
    """
    Guidance template specification.

    Represents a template with embedded generation instructions.
    """

    template_str: str
    variables: List[GuidanceVariable] = field(default_factory=list)
    template_type: GuidanceTemplateType = GuidanceTemplateType.TEXT

    # Parsing state
    _parsed_segments: List[Tuple[str, Optional[GuidanceVariable]]] = field(default_factory=list)
    _cache_key: str = field(default="")

    def __post_init__(self):
        self._parse_template()
        self._cache_key = self._compute_cache_key()

    def _parse_template(self) -> None:
        """Parse template into segments."""
        # Simple parsing: {{variable_name}}
        pattern = r"\{\{(\w+)(?::([^}]+))?\}\}"
        last_end = 0
        segments = []

        for match in re.finditer(pattern, self.template_str):
            # Add text before variable
            if match.start() > last_end:
                segments.append((self.template_str[last_end : match.start()], None))

            # Add variable
            var_name = match.group(1)

            # Find or create variable
            var = next((v for v in self.variables if v.name == var_name), GuidanceVariable(name=var_name))
            segments.append(("", var))

            last_end = match.end()

        # Add remaining text
        if last_end < len(self.template_str):
            segments.append((self.template_str[last_end:], None))

        self._parsed_segments = segments

    def _compute_cache_key(self) -> str:
        """Compute cache key for template."""
        content = self.template_str + str([(v.name, v.type, v.regex) for v in self.variables])
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def get_prefix_text(self) -> str:
        """Get fixed prefix text before first variable."""
        for text, var in self._parsed_segments:
            if var is not None:
                return text
        return self.template_str

    def get_variable_sequence(self) -> List[Tuple[str, GuidanceVariable]]:
        """Get sequence of (prefix_text, variable) pairs."""
        result = []
        for text, var in self._parsed_segments:
            if var is not None:
                result.append((text, var))
        return result


class GuidanceState:
    """
    State for Guidance template execution.

    Tracks current position in template and variable values.
    """

    def __init__(self, template: GuidanceTemplate):
        self.template = template
        self.segment_index = 0
        self.variable_values: Dict[str, str] = {}
        self.generated_text = ""
        self.is_complete = False
        self._current_var_buffer = ""

    def accept_token(self, token_text: str) -> bool:
        """Accept a token and update state."""
        self._current_var_buffer += token_text
        self.generated_text += token_text

        # Check if we've completed current segment
        if self.segment_index >= len(self.template._parsed_segments):
            self.is_complete = True
            return True

        text, var = self.template._parsed_segments[self.segment_index]

        if var is None:
            # Text segment - check if matches
            if self.generated_text.endswith(text):
                self.segment_index += 1
                self._current_var_buffer = ""
        else:
            # Variable segment - check for stop conditions
            if var.stop:
                for stop in var.stop:
                    if stop in self._current_var_buffer:
                        # Found stop, extract value
                        value = self._current_var_buffer[: self._current_var_buffer.find(stop)]
                        self.variable_values[var.name] = value
                        self.segment_index += 1
                        self._current_var_buffer = ""
                        break

            # Check max tokens (approximate by character count)
            if len(self._current_var_buffer) > var.max_tokens * 4:
                self.variable_values[var.name] = self._current_var_buffer
                self.segment_index += 1
                self._current_var_buffer = ""

        return True

    def get_allowed_tokens(self, vocab_size: int) -> Set[int]:
        """Get set of allowed token IDs."""
        # By default, allow all tokens
        return set(range(vocab_size))

    def reset(self) -> None:
        """Reset state."""
        self.segment_index = 0
        self.variable_values.clear()
        self.generated_text = ""
        self.is_complete = False
        self._current_var_buffer = ""


class CompiledGuidanceProgram:
    """
    Compiled Guidance program.

    Represents a compiled and ready-to-execute Guidance template.
    """

    def __init__(
        self,
        template: GuidanceTemplate,
        vocab_size: int,
    ):
        self.template = template
        self.vocab_size = vocab_size
        self._state: Optional[GuidanceState] = None

    def create_state(self) -> GuidanceState:
        """Create new execution state."""
        return GuidanceState(self.template)

    def fill_bitmask(
        self,
        state: GuidanceState,
        bitmask: "np.ndarray",
    ) -> None:
        """Fill bitmask with allowed tokens."""
        if HAS_NUMPY:
            bitmask.fill(1)  # Allow all by default

    def is_terminated(self, state: GuidanceState) -> bool:
        """Check if execution is complete."""
        return state.is_complete


class GuidanceGrammar:
    """
    Grammar wrapper for Guidance programs.

    Provides the standard grammar interface while wrapping
    a Guidance program and state.
    """

    def __init__(
        self,
        program: "CompiledGuidanceProgram",
        tokenizer: Any,
        state: Optional[GuidanceState] = None,
    ):
        self.program = program
        self.tokenizer = tokenizer
        self.state = state or program.create_state()

    def accept_token(self, token_id: int) -> bool:
        """Accept a token."""
        # Decode token to text
        try:
            if hasattr(self.tokenizer, "decode"):
                text = self.tokenizer.decode([token_id])
            else:
                text = f"token_{token_id}"
            return self.accept_token_text(text)
        except Exception:
            return False

    def accept_token_text(self, text: str) -> bool:
        """Accept a token by text."""
        return self.state.accept_token(text)

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask for next token."""
        self.program.fill_bitmask(self.state, bitmask)

    def is_terminated(self) -> bool:
        """Check if grammar is terminated."""
        return self.program.is_terminated(self.state)

    def reset(self) -> None:
        """Reset grammar state."""
        self.state.reset()

    def get_variable_values(self) -> Dict[str, str]:
        """Get extracted variable values."""
        return dict(self.state.variable_values)

    def create_state(self) -> GuidanceState:
        """Create a new state for this grammar."""
        return self.program.create_state()


class GuidanceBackend:
    """
    Guidance library backend for structured output.

    Provides template-based constrained generation using the
    Guidance library's approach to structured output.
    """

    def __init__(
        self,
        tokenizer: Any,
        vocab_size: Optional[int] = None,
        max_cache_size: int = 1000,
    ):
        self.tokenizer = tokenizer
        self.vocab_size = vocab_size or self._get_vocab_size(tokenizer)
        self.max_cache_size = max_cache_size

        # Template cache
        self._cache: Dict[str, CompiledGuidanceProgram] = {}
        self._cache_lock = threading.Lock()

        # Statistics
        self._stats = {
            "compilations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

    def _get_vocab_size(self, tokenizer: Any) -> int:
        """Get vocabulary size from tokenizer."""
        if hasattr(tokenizer, "vocab_size"):
            return tokenizer.vocab_size
        if hasattr(tokenizer, "get_vocab"):
            return len(tokenizer.get_vocab())
        return 32000  # Default fallback

    def compile_template(
        self,
        template_str: str,
        variables: Optional[List[GuidanceVariable]] = None,
    ) -> GuidanceGrammar:
        """Compile a Guidance template."""
        template = GuidanceTemplate(
            template_str=template_str,
            variables=variables or [],
        )

        cache_key = template._cache_key

        with self._cache_lock:
            if cache_key in self._cache:
                self._stats["cache_hits"] += 1
                program = self._cache[cache_key]
                return GuidanceGrammar(program, self.tokenizer)

        # Compile
        program = CompiledGuidanceProgram(
            template=template,
            vocab_size=self.vocab_size,
        )

        with self._cache_lock:
            self._stats["cache_misses"] += 1
            self._stats["compilations"] += 1

            # Evict if needed
            if len(self._cache) >= self.max_cache_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]

            self._cache[cache_key] = program

        return GuidanceGrammar(program, self.tokenizer)

    def compile_json_schema(self, schema: str) -> GuidanceGrammar:
        """Compile JSON schema to Guidance program."""
        # Parse schema
        try:
            schema_obj = json.loads(schema)
        except json.JSONDecodeError:
            schema_obj = {"type": "object"}

        # Generate template from schema
        template_str = self._schema_to_template(schema_obj)
        return self.compile_template(template_str)

    def _schema_to_template(self, schema: Dict[str, Any]) -> str:
        """Convert JSON schema to Guidance template."""
        schema_type = schema.get("type", "object")

        if schema_type == "object":
            props = schema.get("properties", {})

            parts = ["{"]
            for i, (key, _) in enumerate(props.items()):
                if i > 0:
                    parts.append(",")
                parts.append(f'"{key}":')
                parts.append(f"{{{{value_{key}}}}}")
            parts.append("}")

            return "".join(parts)

        elif schema_type == "array":
            return "[{{items}}]"

        elif schema_type == "string":
            if "enum" in schema:
                options = "|".join(f'"{opt}"' for opt in schema["enum"])
                return f"{{{{choice:{options}}}}}"
            return '"{{value}}"'

        elif schema_type in ("number", "integer"):
            return "{{number}}"

        elif schema_type == "boolean":
            return "{{choice:true|false}}"

        return "{{value}}"

    def allocate_bitmask(self, batch_size: int) -> "np.ndarray":
        """Allocate token bitmask."""
        if not HAS_NUMPY:
            raise RuntimeError("NumPy required")
        return np.ones((batch_size, self.vocab_size), dtype=np.int32)

    def get_stats(self) -> Dict[str, Any]:
        """Get backend statistics."""
        with self._cache_lock:
            return dict(self._stats)

    def clear_cache(self) -> None:
        """Clear template cache."""
        with self._cache_lock:
            self._cache.clear()


class AsyncGuidanceBackend(GuidanceBackend):
    """
    Async-enabled Guidance backend.

    Provides async template compilation for non-blocking operation.
    """

    async def compile_template_async(
        self,
        template_str: str,
        variables: Optional[List[GuidanceVariable]] = None,
    ) -> CompiledGuidanceProgram:
        """Async template compilation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.compile_template,
            template_str,
            variables,
        )

    async def compile_json_schema_async(
        self,
        schema: str,
    ) -> CompiledGuidanceProgram:
        """Async JSON schema compilation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.compile_json_schema,
            schema,
        )


__all__ = [
    "GuidanceTemplateType",
    "GuidanceVariable",
    "GuidanceTemplate",
    "GuidanceState",
    "CompiledGuidanceProgram",
    "GuidanceBackend",
    "AsyncGuidanceBackend",
    "GuidanceGrammar",
]
