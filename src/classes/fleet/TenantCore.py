#!/usr/bin/env python3

"""
TenantCore logic for workspace isolation.
Pure logic for path translation and security boundary enforcement.
"""

import os
from typing import List, Optional

class TenantCore:
    def __init__(self) -> None:
        pass

    def validate_and_translate_path(self, tenant_root: str, relative_path: str) -> str:
        """
        Pure logic to ensure a path stays within the tenant's boundaries.
        Returns the absolute path if valid, raises PermissionError otherwise.
        """
        tenant_root_abs = os.path.abspath(tenant_root)
        target_path_abs = os.path.abspath(os.path.join(tenant_root_abs, relative_path))
        
        # Security Boundary Check: Must start with tenant root
        if not target_path_abs.startswith(tenant_root_abs):
            raise PermissionError(f"Security Breach: Path {relative_path} escaped isolation boundary.")
            
        return target_path_abs

    def get_required_dirs(self) -> List[str]:
        """Standardised tenant folder structure."""
        return ["src", "data", "logs", "config"]
