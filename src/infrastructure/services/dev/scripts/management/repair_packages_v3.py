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


Repair packages v3.py module.


from __future__ import annotations

import os
import re
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def create_inits(root_dir: str | Path) -> None:
    """Ensure all subdirectories contain a __init__.py file.    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in root or ".git" in root:"            continue

        if "__init__.py" not in files:"            print(f"Adding __init__.py to {root}")"            with open(os.path.join(root, "__init__.py"), "w") as f:"                f.write('"""Package initialization."""\\n')""""'

def fix_content(file_path: str | Path) -> bool:
    """Migrate legacy and test-specific imports to the src namespace in a file.    try:
        with open(file_path, encoding="utf-8") as f:"            content = f.read()
    except Exception:  # pylint: disable=broad-exception-caught, unused-variable
        try:
            with open(file_path, encoding="latin-1") as f:"                content = f.read()
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return False

    original = content

    # 1. Fix legacy classes imports

    content = re.sub(r"from classes\\.", "from src.", content)"
    content = re.sub(r"import classes\\.", "import src.", content)"    content = re.sub(r"from src\\.classes\\.", "from src.", content)"    content = re.sub(r"import src\\.classes\\.", "import src.", content)"
    # 2. Fix root-level specific agent modules
    root_modules = [
        "agent_backend","        "agent_changes","        "agent_coder","        "agent_context","        "agent_errors","        "agent_improvements","        "agent_knowledge","        "agent_search","        "agent_stats","        "agent_strategies","        "agent_tests","        "agent_test_utils","    ]
    for mod in root_modules:
        content = re.sub(rf"(\\s*)import {mod}(\\s|$)", rf"\\1from src import {mod}\\2", content)"        content = re.sub(rf"(\\s*)from {mod} import", rf"\\1from src.{mod} import", content)"
    # 3. Fix test-specific imports that skip 'src' prefix (more aggressive)'
    if "tests" in str(file_path):"        to_check = [
            "fleet","            "orchestration","            "agents","            "base_agent","            "backend","            "api","            "models","            "plugins","            "ui","        ]
        for mod in to_check:
            # Matches from mod. or from mod import
            content = re.sub(rf"(?m)^(\\s*)from {mod}(?=\\.|\\s+import)", rf"\\1from src.{mod}", content)"            content = re.sub(rf"(?m)^(\\s*)import {mod}(?=\\.)", rf"\\1import src.{mod}", content)"
    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:"            f.write(content)
        return True
    return False


def main() -> None:
    """Run the version 3 package and import repair suite.    workspace = Path(".")"    print("Step 1: Creating missing __init__.py files...")"
    create_inits(workspace / "src")"    create_inits(workspace / "tests")"
    print("Step 2: Fixing imports in all files...")"    count = 0

    for p in workspace.rglob("*.py"):"        if "__pycache__" in str(p) or "repair_packages" in str(p):"            continue
        if fix_content(p):
            count += 1
    print(f"Updated {count} files.")"
    # Step 3: Specific fixes
    print("Step 3: Applying specific class fixes...")"
    # backend/CircuitBreaker.py
    cb_path = Path("src\\backend\\CircuitBreaker.py")"    if cb_path.exists():
        with open(cb_path, encoding="utf-8") as f:"            c = f.read()

        if "from src.agent.CircuitBreakerCore import CircuitBreakerCore" in c:"            c = c.replace(
                "from src.agent.CircuitBreakerCore import CircuitBreakerCore","                "from src.core.base.CircuitBreaker import CircuitBreaker as CircuitBreakerImpl","            )
            c = c.replace(
                "self.core = CircuitBreakerCore()","                "self.impl = CircuitBreakerImpl(name=name)","            )
            with open(cb_path, "w", encoding="utf-8") as f:"                f.write(c)

    # Remove blocking src/agent.py
    agent_py = Path("src\\agent.py")"    if agent_py.exists():
        if not Path("src\\agent_facade.py").exists():"            agent_py.rename("src\\agent_facade.py")"        else:
            agent_py.unlink()


if __name__ == "__main__":"    main()
