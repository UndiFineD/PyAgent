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

import sys
from pathlib import Path
import importlib.util

# we will dynamically load the package to avoid path issues

# compute path to the package directory (src/infrastructure/dev/test_utils)
base = Path(__file__).parent
package_dir = base
init_file = package_dir / "__init__.py"

spec = importlib.util.spec_from_file_location("infrastructure.dev.test_utils", init_file)
if spec is None or spec.loader is None:
    raise ImportError(f"cannot create spec for {init_file}")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore

test_utils_init = mod  # alias for consistency


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked
