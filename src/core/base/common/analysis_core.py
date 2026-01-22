<<<<<<< HEAD
<<<<<<< HEAD
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""Unified code analysis and AST inspection core."""

import ast
import re
from pathlib import Path
<<<<<<< HEAD
<<<<<<< HEAD
from typing import List, Set
=======
from typing import List, Set, Optional
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import List, Set, Optional
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class AnalysisCore:
    """
    Standardized tools for analyzing Python source code without execution.
    """

    @staticmethod
    def calculate_complexity(source: str) -> int:
        """Calculate cyclomatic complexity (Rust accelerated)."""
<<<<<<< HEAD
<<<<<<< HEAD
        if rc and hasattr(rc, "calculate_complexity_rust"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.calculate_complexity_rust(source)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if rc and hasattr(rc, "analyze_complexity_rust"):
            try:
                return rc.analyze_complexity_rust(source)
            except Exception:
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                pass
        # Fallback to simple count of control flow keywords
        keywords = ["if", "for", "while", "except", "with", "and", "or"]
        count = 1
        for kw in keywords:
            count += len(re.findall(rf"\b{kw}\b", source))
        return count

    @staticmethod
<<<<<<< HEAD
<<<<<<< HEAD
    def get_imports(source_or_path: str | Path) -> List[str]:  # pylint: disable=too-many-branches
        """Extract all top-level imports from source or a file (Rust accelerated)."""
        if rc and hasattr(rc, "get_imports_rust"):  # pylint: disable=no-member
            try:
                if isinstance(source_or_path, Path):
                    content = source_or_path.read_text(encoding="utf-8")
                    # pylint: disable=no-member
                    return rc.get_imports_rust(content)  # type: ignore
                # pylint: disable=no-member
                return rc.get_imports_rust(source_or_path)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def get_imports(source_or_path: str | Path) -> List[str]:
        """Extract all top-level imports from source or a file (Rust accelerated)."""
        if rc and hasattr(rc, "get_imports_rust"):
            if isinstance(source_or_path, Path):
                return rc.get_imports_rust(source_or_path.read_text(encoding="utf-8"))
            return rc.get_imports_rust(source_or_path)
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

        try:
            if isinstance(source_or_path, Path):
                tree = ast.parse(source_or_path.read_text(encoding="utf-8"), feature_version=(3, 11))
            else:
                tree = ast.parse(source_or_path, feature_version=(3, 11))
<<<<<<< HEAD
<<<<<<< HEAD
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
=======
        except Exception:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        except Exception:
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return []

        imports: List[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        # Unique imports in order
        seen: Set[str] = set()
        unique_imports: List[str] = []
        for imp in imports:
            if imp not in seen:
                seen.add(imp)
                unique_imports.append(imp)
        return unique_imports

    @staticmethod
    def is_pytest_file(path: Path) -> bool:
        """Heuristic check for pytest files."""
        return path.name.startswith("test_") and path.name.endswith(".py")

    @staticmethod
    def has_main_block(source: str) -> bool:
        """Detect if 'if __name__ == "__main__":' exists."""
        return bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']\s*:', source))

    @staticmethod
    def detect_library_usage(source: str, library_name: str) -> bool:
        """Check if a library is likely used in the source."""
        # Simple string check for now, can be expanded to AST check
        return library_name in source
