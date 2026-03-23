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

"""Abstract base for all transaction managers."""
from __future__ import annotations

import abc


class BaseTransaction(abc.ABC):  # noqa: B024
    """Minimal ABC for all transaction managers.

    Concrete managers do NOT inherit this (Python forbids both def commit and async def commit).
    This exists for isinstance checks and documentation only.
    Duck-typed interface: commit(), rollback(), __enter__, __exit__, __aenter__, __aexit__
    """

    pass
