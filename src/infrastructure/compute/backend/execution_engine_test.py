#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from infrastructure.compute.backend.execution_engine import clear_response_cache, get_metrics, reset_metrics, validate_response_content, estimate_tokens, estimate_cost, configure_timeout_per_backend, llm_chat_via_github_models, llm_chat_via_ollama, llm_chat_via_lmstudio, llm_chat_via_copilot_cli, run_subagent, get_backend_status, describe_backends


def test_clear_response_cache_basic():
    assert callable(clear_response_cache)


def test_get_metrics_basic():
    assert callable(get_metrics)


def test_reset_metrics_basic():
    assert callable(reset_metrics)


def test_validate_response_content_basic():
    assert callable(validate_response_content)


def test_estimate_tokens_basic():
    assert callable(estimate_tokens)


def test_estimate_cost_basic():
    assert callable(estimate_cost)


def test_configure_timeout_per_backend_basic():
    assert callable(configure_timeout_per_backend)


def test_llm_chat_via_github_models_basic():
    assert callable(llm_chat_via_github_models)


def test_llm_chat_via_ollama_basic():
    assert callable(llm_chat_via_ollama)


def test_llm_chat_via_lmstudio_basic():
    assert callable(llm_chat_via_lmstudio)


def test_llm_chat_via_copilot_cli_basic():
    assert callable(llm_chat_via_copilot_cli)


def test_run_subagent_basic():
    assert callable(run_subagent)


def test_get_backend_status_basic():
    assert callable(get_backend_status)


def test_describe_backends_basic():
    assert callable(describe_backends)
