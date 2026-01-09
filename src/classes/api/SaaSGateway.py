#!/usr/bin/env python3

"""Gateway for managing multi-tenant SaaS access, API keys, and usage quotas."""

import logging
import time
import uuid
from typing import Dict, List, Any, Optional

class SaaSGateway:
    """Provides usage control and authentication for the fleet as a service."""
    
    def __init__(self) -> None:
        self.api_keys: Dict[str, Dict[str, Any]] = {} # key -> {tenant, quota}
        self.usage_logs: List[Dict[str, Any]] = []
        self.rate_limits: Dict[str, List[float]] = {} # key -> [timestamps]

    def create_api_key(self, tenant_id: str, daily_quota: int = 1000) -> str:
        """Generates a new API key for a tenant."""
        key = f"pa-{uuid.uuid4().hex}"
        self.api_keys[key] = {
            "tenant_id": tenant_id,
            "daily_quota": daily_quota,
            "used_today": 0,
            "created_at": time.time()
        }
        self.rate_limits[key] = []
        return key

    def validate_request(self, api_key: str, cost: int = 1) -> bool:
        """Checks if a request is authorized and within quota/rate limits."""
        if api_key not in self.api_keys:
            logging.warning(f"SAAS: Unauthorized access attempt with key {api_key}")
            return False
            
        # Rate Limiting (Simple Token Bucket: max 5 requests per second)
        now = time.time()
        self.rate_limits[api_key] = [t for t in self.rate_limits[api_key] if now - t < 1.0]
        if len(self.rate_limits[api_key]) >= 5:
            logging.warning(f"SAAS: Rate limit exceeded for key {api_key}")
            return False

        tenant_info = self.api_keys[api_key]
        if tenant_info["used_today"] + cost > tenant_info["daily_quota"]:
            logging.warning(f"SAAS: Quota exceeded for tenant {tenant_info['tenant_id']}")
            return False
            
        # Record successful request
        self.rate_limits[api_key].append(now)
        tenant_info["used_today"] += cost
        self.usage_logs.append({
            "key": api_key,
            "timestamp": now,
            "tenant": tenant_info["tenant_id"]
        })
        return True

    def get_quota_status(self, api_key: str) -> Dict[str, Any]:
        """Returns the current quota status for a key."""
        return self.api_keys.get(api_key, {"error": "Invalid API Key"})
