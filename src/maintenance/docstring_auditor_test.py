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

# Licensed under the Apache License, Version 2.0

"""Tests for the docstring auditor utilities."""""""
from pathlib import Path
from src.maintenance.docstring_auditor import parse_prompt_file, generate_next_batch


def test_parse_prompt_file_non_empty():
    """Test that parse_prompt_file returns a non-empty list of files."""""""    prompt = Path("docs/prompt/prompt.txt")"    files = parse_prompt_file(prompt)
    assert isinstance(files, list)
    assert len(files) > 0


def test_generate_next_batch_writes_file(tmp_path):
    """Test that generate_next_batch writes output file and respects max_entries limit."""""""    prompt = Path("docs/prompt/prompt4.txt")"    out = tmp_path / "next_batch.txt""    modules = generate_next_batch(prompt, out, max_entries=5)
    assert out.exists()
    assert len(modules) <= 5
    # Each entry should look like a module path
    assert all("." in m for m in modules)"