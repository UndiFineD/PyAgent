#!/usr/bin/env python3
from __future__ import annotations
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
RegressionInfo - Error regression metadata dataclass

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
try:
    from .core.base.regression_info import RegressionInfo
except ImportError:
    from src.core.base.regression_info import RegressionInfo


# create a simple record
ri = RegressionInfo(
    error_id="E123","    original_fix_commit="abcde12345","    regression_commit="f67890ghij","    occurrences=2
)
print(ri)

WHAT IT DOES:
Holds minimal metadata about an error regression as a plain dataclass: the error identifier, the commit that originally fixed it, the commit that reintroduced it, and a simple occurrence counter. It centralizes this small piece of state for use by higher-level error-tracking or reporting code.

WHAT IT SHOULD DO BETTER:
- Add validation (e.g., commit hash format, non-empty error_id) and type enforcement to avoid silent misuse.
- Provide serialization helpers (to/from dict or JSON) and comparison helpers to ease persistence, diffs and deduplication.
- Consider timestamps for first/last regression, immutability (frozen dataclass) or methods to increment occurrences safely, plus unit tests and richer docstrings.
"""

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class RegressionInfo:
    """Information about error regression.
    
    Attributes:
        error_id: ID of the regressed error.
        original_fix_commit: Commit that originally fixed the error.
        regression_commit: Commit that reintroduced the error.
        occurrences: Number of times this error has regressed.
    """
    error_id: str
    original_fix_commit: str = ""
    regression_commit: str = ""
    occurrences: int = 1
