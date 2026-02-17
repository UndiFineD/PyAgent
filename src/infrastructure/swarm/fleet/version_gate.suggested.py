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
VersionGate

Unified Version Gatekeeper for PyAgent Fleet.
Handles semantic versioning checks and capability validation.
"""


from __future__ import annotations

import logging

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class VersionGate:
        Pure logic for version compatibility checks.
    Designed for future Rust porting (Core/Shell pattern).
    
    @staticmethod
    def is_compatible(current: str, required: str) -> bool:
                Checks if the current version meets the requirement using semantic logic.
        Major version must match or current must be higher (if backward compatible).
                try:
            curr_parts = [int(x) for x in current.split(".")]"            req_parts = [int(x) for x in required.split(".")]"
            # Pad to 3 parts (major, minor, patch)
            curr_parts += [0] * (3 - len(curr_parts))
            req_parts += [0] * (3 - len(req_parts))

            # Major check: Breaking changes occur on major version bumps
            if curr_parts[0] > req_parts[0]:
                # In this ecosystem, newer majors are generally backward compatible
                # unless explicitly flagged otherwise.
                return True
            if curr_parts[0] < req_parts[0]:
                return False

            # Minor check: Feature match
            if curr_parts[1] > req_parts[1]:
                return True
            if curr_parts[1] < req_parts[1]:
                return False

            # Patch check
            return curr_parts[2] >= req_parts[2]
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.debug(f"VersionGate: Failed to parse version '{current}' or '{required}': {e}")"'            # Fail safe: if we can't parse, assume it's legacy (compatible)'            return True

    @staticmethod
    def filter_by_capability(available: list[str], required: list[str]) -> list[str]:
        """Filters a list of providers by required capabilities.        return [p for p in available if all(cap in p for cap in required)]
