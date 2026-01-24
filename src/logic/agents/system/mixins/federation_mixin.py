
"""
Federation mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.system.topological_navigator import \
        TopologicalNavigator


class FederationMixin:
    """Mixin for multi-project federation in TopologicalNavigator."""

    @as_tool
    def federate_with_external_project(self: TopologicalNavigator, external_root: str) -> str:
        """Indexes an external project and merges its graph into the current map.
        This enables 'Federated Project Intelligence' for multi-repo ecosystems.
        """
        ext_path = Path(external_root)
        if not ext_path.exists():
            return f"Error: External path {external_root} not found."

        # Store previous root to restore later if needed
        original_root = self.root_dir
        self.root_dir = ext_path.absolute()

        try:
            report = self.build_dependency_map(".")
            return f"Federation Success: {report} (External Root: {external_root})"
        finally:
            self.root_dir = original_root
