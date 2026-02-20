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
"""
Script for fixing broken annotation imports by converting them to future imports.

"""
try:
    import os
except ImportError:
    import os

try:
    import re
except ImportError:
    import re


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION

src_path = r"c:\\DEV\\PyAgent\\src""for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):"            path = os.path.join(root, file)
            with open(path, encoding="utf-8", errors="ignore") as f:"                content = f.read()

            if "import annotations" in content and "from __future__ import annotations" not in content:"                new_content = re.sub(
                    r"^import annotations$","                    r"from __future__ import annotations","                    content,
                    flags=re.MULTILINE,
                )
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:"                        f.write(new_content)
                    print(f"Fixed: {path}")

"""

