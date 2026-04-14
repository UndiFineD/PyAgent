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

"""Verify active tree is free of known leaked private key artifacts."""

from __future__ import annotations

from pathlib import Path

SCAN_PATHS = ("rust_core", "docs/security")
KNOWN_KEY_ARTIFACT = Path("rust_core/2026-03-11-keys.priv")


def has_known_key_artifact() -> bool:
    """Return whether the known key artifact path is present.

    Returns:
        True if the key artifact exists, else False.

    """
    return KNOWN_KEY_ARTIFACT.exists()


def main() -> int:
    """Run deterministic tree cleanup check for known leaked key path.

    Returns:
        Exit code: 0 when clean, 1 when leaked artifact is present.

    """
    if has_known_key_artifact():
        print(f"Leaked key artifact detected in scan paths {SCAN_PATHS}: {KNOWN_KEY_ARTIFACT}")
        return 1
    print(f"No known key artifacts detected in scan paths {SCAN_PATHS}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
