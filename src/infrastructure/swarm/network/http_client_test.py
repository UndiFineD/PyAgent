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

import pytest
from infrastructure.swarm.network.http_client import HTTPClient, AsyncHTTPClient, RetryableHTTPClient, get_bytes, get_text, get_json


def test_httpclient_basic():
    assert HTTPClient is not None


def test_asynchttpclient_basic():
    assert AsyncHTTPClient is not None


def test_retryablehttpclient_basic():
    assert RetryableHTTPClient is not None


def test_get_bytes_basic():
    assert callable(get_bytes)


def test_get_text_basic():
    assert callable(get_text)


def test_get_json_basic():
    assert callable(get_json)
