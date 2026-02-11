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
import os
import site

print("Python Executable:", sys.executable)
print("Sys Path:", sys.path)
print("User Site:", site.USER_SITE)
print("Enable User Site:", site.ENABLE_USER_SITE)

try:
    import pip
    print("Pip imported successfully:", pip.__file__)
except ImportError as e:
    print("Failed to import pip:", e)
except Exception as e:
    print("Error importing pip:", e)

# Check writability of site-packages
for path in sys.path:
    if 'site-packages' in path:
        is_writable = os.access(path, os.W_OK)
        print(f"Site-package path: {path} | Writable: {is_writable}")

        # Check for stale locks
        # pip sometimes leaves .lock files
        try:
            files = os.listdir(path)
            for f in files:
                if f.endswith('.lock'):
                    print(f"WARNING: Lock file found: {os.path.join(path, f)}")
        except Exception:
            pass
