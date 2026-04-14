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

"""Per-module red tests for the FuzzMutator contract module."""

from __future__ import annotations

from tests.test_fuzzing_core import _require_symbol


def test_fuzz_mutator_mutate_contract_returns_bytes() -> None:
    """Verify FuzzMutator mutate contract returns bytes for canonical input."""
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    payload = mutator_cls(seed=123).mutate(payload=b"AAAA", operator="bit_flip", corpus_index=0)
    assert isinstance(payload, bytes)
