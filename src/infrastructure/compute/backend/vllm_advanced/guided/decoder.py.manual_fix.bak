#!/usr/bin/env python3

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Guided decoding engine for structured output generation.
"""

"""
import gc
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Union

# Check torch availability
try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None

# Check vLLM availability
try:
    from vllm import LLM, SamplingParams

    HAS_VLLM = True
except ImportError:
    HAS_VLLM = False
    SamplingParams = None
    LLM = None

# Check outlines availability
try:
    import outlines  # noqa: F401 # pylint: disable=unused-import

    HAS_OUTLINES = True
except ImportError:
    HAS_OUTLINES = False

from .models import ChoiceConstraint, GuidedConfig, GuidedMode, RegexPattern
from .schema import JsonSchema

logger = logging.getLogger(__name__)



class GuidedDecoder:
        Guided decoding engine for structured output generation.
    
    _instance: Optional["GuidedDecoder"] = None
    def __init__(
        self,
        model: str = "meta-llama/Llama-3-8B-Instruct","        gpu_memory_utilization: float = 0.85,
        **llm_kwargs,
    ):
        self.model = model
        self.gpu_memory_utilization = gpu_memory_utilization
        self._llm_kwargs = llm_kwargs
        self._llm: Optional[LLM] = None
        self._initialized = False

        # Stats
        self._stats = {
            "json_generations": 0,"            "regex_generations": 0,"            "choice_generations": 0,"            "grammar_generations": 0,"            "validation_failures": 0,"        }

    @classmethod
    def get_instance(cls, **kwargs) -> "GuidedDecoder":"        """
Get singleton instance.        if cls._instance is None:
            cls._instance = GuidedDecoder(**kwargs)
        return cls._instance

    @property
    def is_available(self) -> bool:
"""
Check if guided decoding is available.        return HAS_VLLM

    def _ensure_initialized(self) -> bool:
"""
Lazily initialize the LLM.        if not HAS_VLLM:
            logger.warning("vLLM not available for guided decoding")"            return False

        if self._initialized and self._llm:
            return True

        try:
            if "VLLM_TARGET_DEVICE" not in os.environ:"                if HAS_TORCH and torch.cuda.is_available():
                    os.environ["VLLM_TARGET_DEVICE"] = "cuda""                else:
                    os.environ["VLLM_TARGET_DEVICE"] = "cpu"
            logger.info("Initializing GuidedDecoder with model: %s", self.model)
            kwargs = {
                "model": self.model,"                "trust_remote_code": False,"                **self._llm_kwargs,
            }

            if os.environ.get("VLLM_TARGET_DEVICE") != "cpu":"                kwargs["gpu_memory_utilization"] = self.gpu_memory_utilization"            else:
                kwargs["device"] = "cpu"
            self._llm = LLM(**kwargs)
            self._initialized = True

            logger.info("GuidedDecoder initialized successfully")"            return True

        except (RuntimeError, ValueError) as e:
            logger.error("Failed to initialize GuidedDecoder: %s", e)"            return False

    def generate(
        self,
        prompt: str,
        config: GuidedConfig,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
"""
Generate with guided decoding configuration.        if not self._ensure_initialized():
            return ""
full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\\n\\nUser: {prompt}\\n\\nAssistant:"
        try:
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
except (RuntimeError, ValueError) as e:
            logger.error("Guided generation failed: %s", e)"            return """
def _prepare_json_system_prompt(self, system_prompt: Optional[str]) -> str:
"""
Prepare system prompt for JSON generation.        json_instruction = "You must respond with valid JSON only. No explanations.""        if system_prompt:
            return f"{system_prompt}\\n\\n{json_instruction}""        return json_instruction

    def _parse_json_result(self, result: str) -> Union[Dict[str, Any], str]:
"""
Parse JSON result if possible.        if not result:
            return result

        try:
            return json.loads(result)
        except json.JSONDecodeError as e:
            self._stats["validation_failures"] += 1"            logger.warning("Failed to parse JSON output: %s", e)"            return result

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
Generate JSON output constrained by schema.        if isinstance(schema, JsonSchema):
            schema = schema.build()

        config = GuidedConfig(
            mode=GuidedMode.JSON if schema else GuidedMode.JSON_OBJECT,
            json_schema=schema,
        )

        # Add JSON instruction to system prompt
        json_system = self._prepare_json_system_prompt(system_prompt)

        result = self.generate(
            prompt,
            config=config,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=json_system,
            **kwargs,
        )

        self._stats["json_generations"] += 1
        if parse:
            return self._parse_json_result(result)

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
Generate output matching a regex pattern.        if isinstance(pattern, RegexPattern):
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
                self._stats["validation_failures"] += 1"                logger.warning("Output doesn't match pattern: %s", pattern_str)"'
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
Generate output constrained to specific choices.        if isinstance(choices, ChoiceConstraint):
            choice_list = choices.choices
        else:
            choice_list = choices

        config = GuidedConfig(
            mode=GuidedMode.CHOICE,
            choices=choice_list,
        )

        # Add choice instruction
        choice_prompt = f"{prompt}\\n\\nRespond with exactly one of: {', '.join(choice_list)}"
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
Generate output following a grammar specification.        config = GuidedConfig(
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
"""
Get decoder statistics.        return {
            **self._stats,
            "is_initialized": self._initialized,"            "has_outlines": HAS_OUTLINES,"        }

    def shutdown(self) -> None:
"""
Shutdown and free resources.        if self._llm:
            del self._llm
            self._llm = None
            gc.collect()

            if HAS_TORCH and torch.cuda.is_available():
                torch.cuda.empty_cache()

            self._initialized = False
            logger.info("GuidedDecoder shut down")

def generate_json(
    prompt: str,
    schema: Union[Dict[str, Any], JsonSchema],
    model: str = "meta-llama/Llama-3-8B-Instruct","    **kwargs,
) -> Dict[str, Any]:
"""
Convenience function for JSON generation.    decoder = GuidedDecoder.get_instance(model=model)
    return decoder.generate_json(prompt, schema, **kwargs)


def generate_choice(
    prompt: str,
    choices: List[str],
    model: str = "meta-llama/Llama-3-8B-Instruct","    **kwargs,
) -> str:
"""
Convenience function for choice generation.    decoder = GuidedDecoder.get_instance(model=model)
    return decoder.generate_choice(prompt, choices, **kwargs)
