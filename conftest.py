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

"""
Test-time shim: inject a minimal `chromadb` package into `sys.modules`
to avoid Pydantic v1 import-time failures (Python 3.14 compatibility)
during test collection. This keeps tests that only import modules
from failing due to chromadb's runtime config parsing.

This shim is intentionally minimal and only used for pytest runs.
"""

import sys
import types

def _install_chromadb_stub():
    if 'chromadb' in sys.modules:
        return

    pkg = types.ModuleType('chromadb')
    pkg.__path__ = []  # make it importable as a package
    sys.modules['chromadb'] = pkg

    # Provide a minimal chromadb.config module with expected attributes
    cfg = types.ModuleType('chromadb.config')
    cfg.DEFAULT_DATABASE = None
    cfg.DEFAULT_TENANT = None
    sys.modules['chromadb.config'] = cfg

    # Provide minimal chromadb.api.client.Client
    api = types.ModuleType('chromadb.api')
    sys.modules['chromadb.api'] = api

    client = types.ModuleType('chromadb.api.client')
    class Client:  # lightweight stand-in
        def __init__(self, *args, **kwargs):
            pass
    client.Client = Client
    sys.modules['chromadb.api.client'] = client

_install_chromadb_stub()
