#!/usr/bin/env python3
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

try:
    import pytest
"""
except ImportError:

"""
import pytest

try:
    from .lazy import get_eagle_proposer, get_arc_offload_manager, get_tool_parser_registry, get_reasoning_engine, get_paged_attention_engine, get_mooncake_connector, get_nixl_connector, get_prefill_worker, get_decode_worker, get_pp_transfer, get_tp_transfer
except ImportError:
    from .lazy import get_eagle_proposer, get_arc_offload_manager, get_tool_parser_registry, get_reasoning_engine, get_paged_attention_engine, get_mooncake_connector, get_nixl_connector, get_prefill_worker, get_decode_worker, get_pp_transfer, get_tp_transfer



def test_get_eagle_proposer_basic():
    assert callable(get_eagle_proposer)


def test_get_arc_offload_manager_basic():
    assert callable(get_arc_offload_manager)


def test_get_tool_parser_registry_basic():
    assert callable(get_tool_parser_registry)


def test_get_reasoning_engine_basic():
    assert callable(get_reasoning_engine)


def test_get_paged_attention_engine_basic():
    assert callable(get_paged_attention_engine)


def test_get_mooncake_connector_basic():
    assert callable(get_mooncake_connector)


def test_get_nixl_connector_basic():
    assert callable(get_nixl_connector)


def test_get_prefill_worker_basic():
    assert callable(get_prefill_worker)


def test_get_decode_worker_basic():
    assert callable(get_decode_worker)


def test_get_pp_transfer_basic():
    assert callable(get_pp_transfer)


def test_get_tp_transfer_basic():
    assert callable(get_tp_transfer)
