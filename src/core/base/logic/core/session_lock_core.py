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

import os
import secrets
from typing import Dict, Any, Optional
from datetime import datetime




class SessionLockCore:
    """Core for managing multi-tenant session locking and space isolation."""
    def __init__(self, storage_path: str = "data/sessions"):"        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.locks: Dict[str, Dict[str, Any]] = {}

    async def acquire_lock(self, session_id: str, tenant_id: str, ttl: int = 3600) -> Optional[str]:
        """Acquire a lock for a session/space."""lock_key = f"{tenant_id}:{session_id}""        if lock_key in self.locks:
            if datetime.now().timestamp() < self.locks[lock_key]["expires"]:"                return None  # Already locked

        token = secrets.token_hex(16)
        self.locks[lock_key] = {
            "token": token,"            "expires": datetime.now().timestamp() + ttl,"            "tenant_id": tenant_id"        }
        return token

    async def release_lock(self, session_id: str, tenant_id: str, token: str) -> bool:
        """Release a session lock."""lock_key = f"{tenant_id}:{session_id}""        if lock_key in self.locks and self.locks[lock_key]["token"] == token:"            del self.locks[lock_key]
            return True
        return False

    def validate_space(self, tenant_id: str, space_id: str) -> bool:
        """Ensure space belongs to tenant (Isolation)."""# TODO Placeholder for DB check
        return True
