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
except ImportError:
    import pytest

try:
    from .generate_ast_refactor_patches import SubprocessTransformer, load_bandit_results, top_files_from_bandit, create_patch_for_file, main
except ImportError:
    from .generate_ast_refactor_patches import SubprocessTransformer, load_bandit_results, top_files_from_bandit, create_patch_for_file, main



def test_subprocesstransformer_basic():
    assert SubprocessTransformer is not None


def test_load_bandit_results_basic():
    assert callable(load_bandit_results)


def test_top_files_from_bandit_basic():
    assert callable(top_files_from_bandit)


def test_create_patch_for_file_basic():
    assert callable(create_patch_for_file)


def test_main_basic():
    assert callable(main)
