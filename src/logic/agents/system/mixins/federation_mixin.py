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
FederationMixin - Index and merge external project graphs

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
from src.logic.agents.system.topological_navigator import TopologicalNavigator
nav = TopologicalNavigator(root_dir="C:\\DEV\\MyRepo")
nav.federate_with_external_project("C:\\path\\to\\external_repo")

WHAT IT DOES:
- Provides a simple mixin (FederationMixin) for TopologicalNavigator to index an external project root and merge its dependency/graph map into the current navigator's context.
- Temporarily switches the navigator's root_dir to the external path, calls build_dependency_map("."), and returns a human-readable success or error message.
- Restores the original root_dir in a finally block to ensure the navigator's state is preserved after the operation.

WHAT IT SHOULD DO BETTER:
- Validate and normalize external_root (resolve symlinks, expand ~, convert to absolute consistently), and provide clearer error codes rather than plain strings.
- Merge strategy and conflict resolution must be explicit: currently it returns a report string but does not describe how nodes/edges are reconciled, so implement configurable merge policies (overwrite, namespace, prefixing).
- Add robust logging, permission checks, concurrency safety (avoid race conditions when multiple federations run), progress reporting for large projects, and comprehensive unit/integration tests; also consider asynchronous indexing and cancellation support.
- Improve typing (return structured result object instead of raw str), surface metrics about what changed, and handle nested or nested-workspace repositories more robustly.

FILE CONTENT SUMMARY:
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
""""Mixin for multi-project federation in TopologicalNavigator."""

    @as_tool
    def federate_with_external_project(self: TopologicalNavigator, external_root: str) -> str:
        "Indexes an external project and merges its graph into the current map.
        This enables 'Federated Project Intelligence' for multi-repo ecosystems.
"""
        ext_path = Path(external_root)
        if not ext_path.exists():
#             return fError: External path {external_root} not found.

        # Store previous root to restore later if needed
        original_root = self.root_dir
        self.root_dir = ext_path.absolute()

        try:
            report = self.build_dependency_map(".")
#             return fFederation Success: {report} (External Root: {external_root})
        finally:
            self.root_dir = original_root
"""
# Copyright 2026 "PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.system.topological_navigator import \
        TopologicalNavigator


class FederationMixin:
""""Mixin for multi-project federation in TopologicalNavigator."""

    @as_tool
    def federate_with_external_project(self: TopologicalNavigator, external_root: str) -> str:
        "Indexes an external project and merges its graph "into the current map.
        This enables 'Federated Project Intelligence' for multi-repo ecosystems.
"""
        ext_path = Path(external_root)
        if not ext_path.exists():
#             return fError: External path {external_root} not found.

        # Store previous root to restore later if needed
        original_root = self.root_dir
        self.root_dir = ext_path.absolute()

        try:
            report = self.build_dependency_map(".")
#             return fFederation Success: {report} (External Root: {external_root})
        finally:
            self.root_dir = original_root
