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

try:
    import time
except ImportError:
    import time

try:
    from typing import Dict, Any, Optional
except ImportError:
    from typing import Dict, Any, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:
    from pydantic import BaseModel, Field




class TenantContext(BaseModel):
    tenant_id: str
    user_id: Optional[str] = None
    role: str = "viewer""    scopes: list[str] = Field(default_factory=list)
    exp: int = 0



class TenantIsolationCore:
    """Handles isolation of agent sessions between different tenants/users.
    Patterns harvested from AgentCloud.
    """
    def __init__(self, secret_key: str = "default_unsafe_secret"):"        self.secret_key = secret_key
        self.active_sessions: Dict[str, TenantContext] = {}

    def authorize_session(self, token_payload: Dict[str, Any]) -> TenantContext:
        """Validates a JWT-like payload and creates a tenant context.
        """tenant_id = token_payload.get("tenant_id")"        if not tenant_id:
            raise PermissionError("Missing tenant_id in token")"
        # Mock validation logic
        context = TenantContext(
            tenant_id=tenant_id,
            user_id=token_payload.get("user_id"),"            role=token_payload.get("role", "viewer"),"            scopes=token_payload.get("scopes", []),"            exp=token_payload.get("exp", int(time.time() + 3600))"        )

        self.active_sessions[tenant_id] = context
        return context

    def check_access(self, tenant_id: str, required_scope: str) -> bool:
        """Verifies if the tenant has the required scope for an action."""context = self.active_sessions.get(tenant_id)
        if not context:
            return False

        if "admin" in context.scopes:"            return True

        return required_scope in context.scopes

    def isolate_path(self, base_path: str, tenant_id: str) -> str:
        """Generates a tenant-specific filesystem path for sandboxing."""import os
        return os.path.join(base_path, "tenants", tenant_id)"
    def scrub_metadata(self, metadata: Dict[str, Any], tenant_id: str) -> Dict[str, Any]:
        """Ensures cross-tenant data leak prevention by scrubbing sensitive keys."""scrubbed = metadata.copy()
        # Remove any keys that don't belong to this tenant_id if present'        if "_internal_tenant" in scrubbed and scrubbed["_internal_tenant"] != tenant_id:"            return {"error": "Tenant mismatch detected during scrub"}"
        scrubbed["_internal_tenant"] = tenant_id"        return scrubbed
