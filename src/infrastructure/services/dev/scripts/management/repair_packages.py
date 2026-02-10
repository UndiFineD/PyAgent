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
Repair packages.py module.
"""


from __future__ import annotations

import os
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def create_inits(root_dir: str) -> None:
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in root:
            continue

        if "__init__.py" not in files:
            print(f"Adding __init__.py to {root}")
            with open(os.path.join(root, "__init__.py"), "w") as f:
                f.write('"""Package initialization."""\n')


def fix_imports(file_path: str) -> bool:
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, encoding="latin-1") as f:
                content = f.read()
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return False

    original = content
    # Fix 'from src.'
    content = content.replace("from src.", "from src.")
    content = content.replace("import src.", "import src.")

    # Fix 'from agent.' or 'from fleet.' that might be in tests
    # But ONLY in files in the tests/ directory or at root (if any left)
    if "tests" in str(file_path):
        content = content.replace("from fleet.", "from src.infrastructure.swarm.fleet.")

        content = content.replace("from orchestration.", "from src.infrastructure.swarm.orchestration.")
        content = content.replace("from agents.", "from src.logic.agents.")
        content = content.replace("from base_agent.", "from src.core.base.")

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    return False


def main() -> None:
    """Execute the package and import repair workflow."""
    workspace = Path(".")
    src = workspace / "src"
    tests = workspace / "tests"

    print("Fixing __init__.py files...")
    create_inits(src)
    create_inits(tests)

    print(f"Fixing imports in all Python files in {workspace.absolute()}...")

    count = 0
    for p in workspace.rglob("*.py"):
        if "__pycache__" in str(p) or "repair_packages.py" in str(p):
            continue
        # print(f"Checking {p}")
        if fix_imports(p):
            print(f"Updated {p}")
            count += 1
    print(f"Updated imports in {count} files.")

    # Specific fix for CircuitBreaker
    cb_path = src / "backend" / "CircuitBreaker.py"
    if cb_path.exists():
        print("Fixing src/backend/CircuitBreaker.py...")

        with open(cb_path, encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        skip_to_class = False

        for line in lines:
            if "from src.agent.CircuitBreakerCore import CircuitBreakerCore" in line:
                new_lines.append(
                    "from src.core.base.CircuitBreaker import CircuitBreaker as CircuitBreakerImpl\n"
                )
                continue
            if "self.core = CircuitBreakerCore()" in line:
                new_lines.append(
                    "        self.impl = CircuitBreakerImpl(\n"
                    "            name=name, failure_threshold=failure_threshold, recovery_timeout=recovery_timeout\n"
                    "        )\n"
                )
                continue
            if "def is_open(self, encoding='utf-8') -> bool:" in line:
                new_lines.append("    def is_open(self, encoding='utf-8') -> bool:\n")
                new_lines.append('        return self.impl.state == "OPEN"\n')
                skip_to_class = True  # Simplified implementation
                break
            new_lines.append(line)

        if skip_to_class:
            # We already added the simplified methods, just close the class roughly
            pass

        with open(cb_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    # Remove the blocking src/agent.py if it exists
    agent_py = src / "agent.py"
    if agent_py.exists():
        print("Moving src/agent.py to src/agent_deprecated.py to avoid namespace conflict")
        if (src / "agent_deprecated.py").exists():
            agent_py.unlink()
        else:
            agent_py.rename(src / "agent_deprecated.py")


if __name__ == "__main__":
    main()
