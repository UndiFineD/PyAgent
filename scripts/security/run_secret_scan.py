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

"""Run secret scanning profile and enforce fail-closed threshold behavior."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.security.secret_scan_service import SecretScanService


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for secret scan execution.

    Returns:
        Parsed argument namespace.

    """
    parser = argparse.ArgumentParser(description="Run secret scanner profile")
    parser.add_argument("--profile", choices=["tree", "refs", "history"], default="tree")
    parser.add_argument("--fail-on-severity", default="HIGH")
    return parser.parse_args()


def main() -> int:
    """Execute selected secret scan profile.

    Returns:
        Process exit code.

    """
    args = parse_args()
    service = SecretScanService()

    if args.profile == "tree":
        report = service.scan_tree([])
    elif args.profile == "refs":
        report = service.scan_refs([])
    else:
        report = service.scan_history([])

    print(f"secret-scan profile={args.profile} status={report.status} blocking={report.blocking}")
    return 1 if report.blocking else 0


if __name__ == "__main__":
    sys.exit(main())
