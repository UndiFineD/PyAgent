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

"""Smoke tests for ProcessTransactionManager module contract.

Full behavioural tests are in tests/test_transaction_managers.py.
"""

from src.core.ProcessTransactionManager import ProcessTransaction, validate


def test_module_contract() -> None:
    assert validate() is True
    assert ProcessTransaction is not None
