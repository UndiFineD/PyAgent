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
from infrastructure.engine.conversation.context.manager import ContextManager, get_context_manager, create_context, merge_contexts, restore_context


def test_contextmanager_basic():
    assert ContextManager is not None


def test_get_context_manager_basic():
    assert callable(get_context_manager)


def test_create_context_basic():
    assert callable(create_context)


def test_merge_contexts_basic():
    assert callable(merge_contexts)


def test_restore_context_basic():
    assert callable(restore_context)
