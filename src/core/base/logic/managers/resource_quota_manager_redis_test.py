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
Integration tests for ResourceQuotaManager with Redis backend.

NOTE: These tests require a Redis instance running locally.
Set REDIS_URL environment variable to run these tests:
    export REDIS_URL=redis://localhost:6379
    pytest tests/unit/test_resource_quota_manager_redis.py -v
"""

import asyncio
import os
import pytest

# Skip all tests if Redis not available
try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from src.core.base.logic.managers.resource_quota_manager import (
    DistributedTokenBucket,
    ResourceQuotaManager,
)

# ...existing code...
