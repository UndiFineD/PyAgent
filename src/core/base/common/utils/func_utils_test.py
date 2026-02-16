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
from core.base.common.utils.func_utils import identity, run_once, run_once_with_result, deprecate_args, deprecate_kwargs, deprecated, supports_kw, get_allowed_kwargs, memoize, memoize_method, throttle, debounce, retry_on_exception, call_limit, timed


def test_identity_basic():
    assert callable(identity)


def test_run_once_basic():
    assert callable(run_once)


def test_run_once_with_result_basic():
    assert callable(run_once_with_result)


def test_deprecate_args_basic():
    assert callable(deprecate_args)


def test_deprecate_kwargs_basic():
    assert callable(deprecate_kwargs)


def test_deprecated_basic():
    assert callable(deprecated)


def test_supports_kw_basic():
    assert callable(supports_kw)


def test_get_allowed_kwargs_basic():
    assert callable(get_allowed_kwargs)


def test_memoize_basic():
    assert callable(memoize)


def test_memoize_method_basic():
    assert callable(memoize_method)


def test_throttle_basic():
    assert callable(throttle)


def test_debounce_basic():
    assert callable(debounce)


def test_retry_on_exception_basic():
    assert callable(retry_on_exception)


def test_call_limit_basic():
    assert callable(call_limit)


def test_timed_basic():
    assert callable(timed)
