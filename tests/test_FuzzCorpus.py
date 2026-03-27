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

"""Per-module red tests for the FuzzCorpus contract module."""

from __future__ import annotations

from tests.test_fuzzing_core import _require_symbol


def test_fuzz_corpus_exposes_indexed_bytes_entries() -> None:
    """Verify FuzzCorpus stores and retrieves bytes payloads deterministically."""
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    corpus = corpus_cls(entries=["one", b"two"])
    assert corpus.get(0) == b"one"
    assert corpus.get(1) == b"two"
