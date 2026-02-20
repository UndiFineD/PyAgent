#!/usr/bin/env python3
""
Minimal, parser-safe Tenant Isolation Core used for tests.""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class TenantContext:
    tenant_id: str
    role: str = "viewer"
    scopes: List[str] = field(default_factory=list)


class TenantIsolationCore:
    def __init__(self):
        self.tenants: Dict[str, TenantContext] = {}

    def create_tenant(self, tenant_id: str, role: str = "viewer") -> TenantContext:
        ctx = TenantContext(tenant_id=tenant_id, role=role)
        self.tenants[tenant_id] = ctx
        return ctx
