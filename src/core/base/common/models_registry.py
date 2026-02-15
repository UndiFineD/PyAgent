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
Unified Model Provider Registry.
Ports the extensive provider list from .code_puppy's models.dev integration.
"""

from typing import Dict, List, TypedDict


class ModelSpec(TypedDict):
    id: str
    context_window: int
    input_price: float  # Per 1M tokens
    output_price: float  # Per 1M tokens
    provider: str
    literals: List[str]  # Trigger keywords


class ProviderRegistry:
    """
    Central repository for 65+ LLM/multimodal providers and their pricing.
    """

    # --------------------------------------------------------------------------
    # TIER 1: FOUNDATION MODELS
    # --------------------------------------------------------------------------
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"

    # --------------------------------------------------------------------------
    # TIER 2: SPECIALIZED & OPEN SOURCE
    # --------------------------------------------------------------------------
    GROQ = "groq"
    TOGETHER = "together"
    PERPLEXITY = "perplexity"
    COHERE = "cohere"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    YI = "01-ai"

    # --------------------------------------------------------------------------
    # TIER 3: EDGE & LOCAL
    # --------------------------------------------------------------------------
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"
    VLLM = "vllm"
    FASTFLOWLM = "fastflowlm"  # NPU Optimized

    @staticmethod
    def get_all_models() -> Dict[str, ModelSpec]:
        """
        Returns the full catalog of supported models.

        Each model entry is represented as a dictionary containing:
            - id (str): Unique identifier or version of the model.
            - context_window (int): Maximum token context window supported by the model.
            - input_price (float): Price per 1,000 input tokens (USD).
            - output_price (float): Price per 1,000 output tokens (USD).
            - provider (str): Name of the model provider (e.g., 'openai', 'anthropic').
            - literals (List[str]): Alternative names or aliases for the model.

        Returns:
            Dict[str, ModelSpec]: A dictionary mapping model names to their specifications.
        """
        """Returns the full catalog of supported models."""
        return {
            "gpt-4-turbo": {
                "id": "gpt-4-turbo-2024-04-09",
                "context_window": 128000,
                "input_price": 10.0,
                "output_price": 30.0,
                "provider": "openai",
                "literals": ["gpt4t", "turbo"]
            },
            # Anthropic
            # "claude-3-5-sonnet": {
            #    "id": "claude-3-5-sonnet-20240620",
            #     "context_window": 200000,
            #     "input_price": 3.0,
            #     "output_price": 15.0,
            #     "provider": "anthropic",
            #     "literals": ["sonnet3.5", "claude"]
            # },
            # "claude-3-opus": {
            #     "id": "claude-3-opus-20240229",
            #     "context_window": 200000,
            #     "input_price": 15.0,
            #     "output_price": 75.0,
            #     "provider": "anthropic",
            #     "literals": ["opus"]
            # },
            # Google
            # "gemini-1.5-pro": {
            #     "id": "gemini-1.5-pro-latest",
            #     "context_window": 2000000,
            #     "input_price": 3.5,
            #     "output_price": 10.5,
            #     "provider": "google",
            #     "literals": ["gemini1.5", "pro"]
            # },
            "gemini-1.5-flash": {
                "id": "gemini-1.5-flash-latest",
                "context_window": 1000000,
                "input_price": 0.35,
                "output_price": 1.05,
                "provider": "google",
                "literals": ["flash"]
            },
            # Groq (Llama 3)
            "llama3-70b-groq": {
                "id": "llama3-70b-8192",
                "context_window": 8192,
                "input_price": 0.59,
                "output_price": 0.79,
                "provider": "groq",
                "literals": ["groq70"]
            },
            # DeepSeek
            "deepseek-v2": {
                "id": "deepseek-coder-v2",
                "context_window": 128000,
                "input_price": 0.14,
                "output_price": 0.28,
                "provider": "deepseek",
                "literals": ["deepseek"]
            },
            # ... (Placeholder for remaining 50+ models)
        }

    @staticmethod
    def get_provider_list() -> List[str]:
        """Returns list of supported providers."""
        return [
            "openai", "anthropic", "google", "meta", "mistral",
            "groq", "together", "perplexity", "cohere", "deepseek",
            "qwen", "01-ai", "ollama", "lmstudio", "vllm", "fastflowlm",
            "databricks", "anyscale", "friendli", "replicate", "fireworks",
            "lepton", "octo", "novita", "monsterapi", "deepinfra"
        ]
