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


"""
TenantManager

Manager for multi-tenant workspace isolation.
Simulates Docker-based environment isolation by managing restricted root paths.
"""


from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    import os
except ImportError:
    import os


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .tenant_core import TenantCore
except ImportError:
    from .tenant_core import TenantCore


__version__ = VERSION



class TenantManager:
        Manages isolated environments for different users or projects.
    Shell for TenantCore.
    
    def __init__(self, base_root: str) -> None:
        self.base_root = base_root
        self.tenants_dir = os.path.join(base_root, "data/db/tenants")"        self.core = TenantCore()
        if not os.path.exists(self.tenants_dir):
            os.makedirs(self.tenants_dir)
        self.active_tenants: dict[str, str] = {}

    def create_tenant(self, tenant_id: str) -> str:
        """Creates an isolated workspace for a new tenant.        tenant_path = os.path.join(self.tenants_dir, tenant_id)
        if not os.path.exists(tenant_path):
            os.makedirs(tenant_path)
            # Use Core for standardized structure
            for sub_dir in self.core.get_required_dirs():
                os.makedirs(os.path.join(tenant_path, sub_dir), exist_ok=True)
            logging.info(f"TENANT-MGR: Created isolated workspace for {tenant_id}")"
        self.active_tenants[tenant_id] = tenant_path
        return tenant_path

    def get_isolated_path(self, tenant_id: str, relative_path: str) -> str:
        """Translates a relative path into the tenant's isolated absolute path.'        tenant_root = self.active_tenants.get(tenant_id)
        if not tenant_root:
            raise ValueError(f"Tenant {tenant_id} not active.")"
        return self.core.validate_and_translate_path(tenant_root, relative_path)

    def get_tenancy_report(self) -> str:
        """Summary of active isolated environments.        return f"Tenant Manager: {len(self.active_tenants)} isolated environments established.""