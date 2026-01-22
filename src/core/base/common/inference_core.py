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

from __future__ import annotations
import logging
from typing import Any, Dict, Optional, List
from .base_core import BaseCore
from src.core.base.common.models.communication_models import PromptTemplate
from src.infrastructure.engine.tokenization.utils import estimate_token_count, get_tokenizer

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.inference")

class InferenceCore(BaseCore):
    """
    Unified Inference and Model Utilities Core.
    Handles tokenization, prompt rendering, and LoRA adapter management.
    """

    def __init__(self, name: str = "InferenceCore", root_path: Optional[str] = None) -> None:
        super().__init__(name=name, root_path=root_path)
        self.templates: Dict[str, PromptTemplate] = {}

    def register_template(self, template: PromptTemplate) -> None:
        """Register a prompt template for easy access."""
        self.templates[template.name] = template

    def render(self, template_name: str, **kwargs: Any) -> str:
        """Render a registered template by name."""
        if template_name in self.templates:
            return self.templates[template_name].render(**kwargs)
        
        # Fallback: check if it's a raw template string
        if "{" in template_name and "}" in template_name:
            return template_name.format(**kwargs)
        
        raise ValueError(f"Template '{template_name}' not found.")

    def count_tokens(self, text: str, model_name: Optional[str] = None) -> int:
        """Consistent token counting across the fleet (Rust-accelerated)."""
        if rc and hasattr(rc, "count_tokens_rust"):
            try:
                return rc.count_tokens_rust(text, model_name)
            except Exception:
                pass
        return estimate_token_count(text, model_name)

    def get_tokenizer(self, model_name: str) -> Any:
        """Get the appropriate tokenizer instance."""
        return get_tokenizer(model_name)

    # --- Adapter Management (Rust Acceleration Target) ---

    def apply_lora_adapters(self, base_model: Any, adapters: List[str]) -> Any:
        """
        Applies LoRA adapters to a base model.
        Hot path for Rust migration (rc.apply_lora_rust).
        """
        if rc and hasattr(rc, "apply_lora_rust"):
            try:
                return rc.apply_lora_rust(base_model, adapters)
            except Exception as e:
                logger.error(f"Rust LoRA application failed: {e}")
        
        # Python fallback (placeholder for actual linear algebra)
        return base_model
