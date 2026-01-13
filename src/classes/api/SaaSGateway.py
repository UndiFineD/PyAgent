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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Gateway for managing multi-tenant SaaS access, API keys, and usage quotas."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import time
import uuid
from typing import Dict, List, Any
from src.infrastructure.api.core.GatewayCore import GatewayCore

__version__ = VERSION

class SaaSGateway:
    """Provides usage control and authentication for the fleet as a service.
    Integrated with GatewayCore for external SaaS orchestration.
    """
    
    def __init__(self) -> None:
        self.api_keys: Dict[str, Dict[str, Any]] = {} # key -> {tenant, quota}
        self.usage_logs: List[Dict[str, Any]] = []
        self.rate_limits: Dict[str, List[float]] = {} # key -> [timestamps]
        self.core = GatewayCore()

    def call_external_saas(self, api_key: str, service: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Proxies a request to an external SaaS service (Jira/Slack/Trello).
        """
        if not self.validate_request(api_key):
             return {"error": "unauthorized"}
             
        endpoint = self.core.get_service_endpoint(service)
        if not endpoint:
            return {"error": f"Service {service} not registered"}
            
        request_obj = self.core.format_saas_request(service, action, params)
        logging.info(f"SaaSGateway: Forwarding to {endpoint}{action}...")
        
        # Simulated response
        return {
            "status": "success",
            "service": service,
            "data": f"Simulated response from {service} for action {action}"
        }

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