#!/usr/bin/env python3
"""Session Lock Core - minimal parser-safe stub for tests."""
from __future__ import annotations

import os
import secrets
from typing import Dict, Any, Optional
from datetime import datetime


class SessionLockCore:
    def __init__(self, storage_path: str = "data/sessions"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.locks: Dict[str, Dict[str, Any]] = {}

    async def acquire_lock(self, session_id: str, tenant_id: str, ttl: int = 3600) -> Optional[str]:
        lock_key = f"{tenant_id}:{session_id}"
        if lock_key in self.locks:
            if datetime.now().timestamp() < self.locks[lock_key]["expires"]:
                return None
        token = secrets.token_hex(16)
        self.locks[lock_key] = {
            "token": token,
            "expires": datetime.now().timestamp() + ttl,
            "tenant_id": tenant_id,
        }
        return token

    async def release_lock(self, session_id: str, tenant_id: str, token: str) -> bool:
        lock_key = f"{tenant_id}:{session_id}"
        if lock_key in self.locks and self.locks[lock_key]["token"] == token:
            del self.locks[lock_key]
            return True
        return False

    def validate_space(self, tenant_id: str, space_id: str) -> bool:
        # Placeholder validation
        return True
