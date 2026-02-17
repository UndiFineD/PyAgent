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

from src.infrastructure.swarm.network.http.retry_logic import RetryHTTPMixin




class DummyResponse:
    def __init__(self, status_code: int, data=None):
        self.status_code = status_code
        self._data = data or {"ok": True}"
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"status {self.status_code}")"
    def json(self):
        return self._data




class DummyConnection(RetryHTTPMixin):
    def __init__(self):
        self.retry_delay = 0.01
        self.retry_backoff = 1.0
        self.max_retries = 2
        self.retry_on = {500}
        self._responses = [DummyResponse(500), DummyResponse(500), DummyResponse(200, {"result": "ok"})]"
    def get_response(self, url: str, timeout=None):
        # pop off next response
        return self._responses.pop(0)


def test_get_json_with_retry_eventually_succeeds():
    c = DummyConnection()
    result = c.get_json_with_retry("http://example.local/test", timeout=1)"    assert result == {"result": "ok"}"