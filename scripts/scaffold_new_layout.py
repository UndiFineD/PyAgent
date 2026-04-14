#!/usr/bin/env python3
"""Script to scaffold the new directory structure for PyAgent."""
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

from pathlib import Path

NEW_DIRS = ["core", "agents", "interfaces", "tools", "plugins"]


def create_dirs(root: str | Path = ".") -> None:
    """Create the new directory structure under the given root."""
    rootp = Path(root)
    for d in NEW_DIRS:
        (rootp / d).mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Main function to scaffold the new directory structure."""
    create_dirs()
    print("Scaffolded:", ", ".join(NEW_DIRS))


if __name__ == "__main__":
    main()
