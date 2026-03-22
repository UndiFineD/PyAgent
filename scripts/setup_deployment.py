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
"""Bootstrap the PyAgent deployment directory hierarchy.

Usage:
    python scripts/setup_deployment.py [--root PATH] [--dry-run]

Creates the ``Deployment/`` tree used by CI and integration tests. Safe to
re-run on an existing workspace (idempotent).
"""

from __future__ import annotations

import argparse
import os
import sys


#: All deployment paths created under ``root``.
DEPLOYMENT_PATHS = [
    "Deployment/development/servers",
    "Deployment/development/networks",
    "Deployment/development/services",
    "Deployment/staging/servers",
    "Deployment/staging/networks",
    "Deployment/staging/services",
    "Deployment/production/servers",
    "Deployment/production/networks",
    "Deployment/production/services",
    "Deployment/infrastructure/cloud_provider",
    "Deployment/infrastructure/load_balancers",
    "Deployment/infrastructure/databases",
    "Deployment/infrastructure/monitoring",
]


def create_deployment_structure(root: str, dry_run: bool = False) -> None:
    """Create the deployment directory hierarchy under *root*.

    Parameters
    ----------
    root:
        Workspace root path.
    dry_run:
        When True, print what would be created without modifying the filesystem.
    """
    created: list[str] = []
    for p in DEPLOYMENT_PATHS:
        full = os.path.join(root, p)
        if not os.path.isdir(full):
            if not dry_run:
                os.makedirs(full, exist_ok=True)
            created.append(full)

    if dry_run:
        for d in created:
            print(f"[dry-run] mkdir {d}")
    else:
        for d in created:
            print(f"created: {d}")
        if not created:
            print("deployment structure already up-to-date")


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for setup_deployment."""
    parser = argparse.ArgumentParser(
        prog="setup_deployment",
        description="Create the PyAgent deployment directory skeleton.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Workspace root (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without modifying disk",
    )

    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    create_deployment_structure(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

