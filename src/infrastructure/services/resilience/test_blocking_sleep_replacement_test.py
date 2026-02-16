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

import pytest
from infrastructure.services.resilience.test_blocking_sleep_replacement import test_retry_strategy_uses_injected_sleep, test_tokenbucket_blocking_uses_injected_sleep, test_multiproc_monitor_interruptible


def test_test_retry_strategy_uses_injected_sleep_basic():
    assert callable(test_retry_strategy_uses_injected_sleep)


def test_test_tokenbucket_blocking_uses_injected_sleep_basic():
    assert callable(test_tokenbucket_blocking_uses_injected_sleep)


def test_test_multiproc_monitor_interruptible_basic():
    assert callable(test_multiproc_monitor_interruptible)
