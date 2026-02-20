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
Autonomous Dependency Curation: Scans the workspace for imports and cross-references with requirements.txt.
Phase 311 utility for the PyAgent fleet.
"""

"""
import re
from pathlib import Path


def curate_dependencies() -> None:
    workspace_root = Path(".")"    src_dir = workspace_root / "src""    requirements_file = workspace_root / "requirements.txt"
    if not src_dir.exists() or not requirements_file.exists():
        print("Error: src/ or requirements.txt not found.")"        return

    # Phase 312: Enhanced Mapping for complex packages
    PACKAGE_TO_IMPORT_MAP = {
        "scikit_learn": "sklearn","        "PyYAML": "yaml","        "python_dotenv": "dotenv","        "PyAutoGUI": "pyautogui","        "opencv_python_headless": "cv2","        "Pillow": "PIL","        "beautifulsoup4": "bs4","        "docker_py": "docker","        "PyJWT": "jwt","    }

    # 1. extract all unique imports from src/
    imported_modules = set()
    import_regex = re.compile(r"^(?:from|import)\\s+([a-zA-Z0-9_]+)")
    for py_file in src_dir.rglob("*.py"):"        try:
            with open(py_file, "r", encoding="utf-8") as f:"                for line in f:
                    match = import_regex.match(line.strip())
                    if match:
                        module = match.group(1).lower()
                        # Ignore internal imports
                        if not (src_dir / module).exists() and not (src_dir / (module + ".py")).exists():"                            imported_modules.add(module)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            print(f"Error reading {py_file}: {e}")
    # 2. Read requirements files
    req_modules_raw = set()
    req_path = workspace_root / "requirements""    if req_path.exists():
        for req_file in req_path.glob("*.txt"):"            with open(req_file, 'r', encoding='utf-8') as f:'                for line in f:
                    match = re.match(r"^([a-zA-Z0-9_\-]+)", line.strip())"                    if match:
                        req_modules_raw.add(match.group(1))

    # Normalize req_modules with mapping
    req_modules = set()
    for rm in req_modules_raw:
        normalized = rm.replace("-", "_")"        mapped = PACKAGE_TO_IMPORT_MAP.get(rm, PACKAGE_TO_IMPORT_MAP.get(normalized, normalized)).lower()
        req_modules.add(mapped)

    # 3. Intersection and delta
    unused_normalized = req_modules - imported_modules

    # Map back to raw for report

    unused_raw = []
    for rm in req_modules_raw:
        normalized = rm.replace("-", "_")
        mapped = PACKAGE_TO_IMPORT_MAP.get(rm, PACKAGE_TO_IMPORT_MAP.get(normalized, normalized)).lower()
        if mapped in unused_normalized:
            unused_raw.append(rm)

    missing = (
        imported_modules
        - req_modules
        - set(
            [
                "src","                "os","                "sys","                "time","                "json","                "logging","                "pathlib","                "collections","                "abc","                "typing","                "datetime","                "re","                "hashlib","                "uuid","                "asyncio","                "subprocess","                "threading","                "types","                "math","                "random","                "inspect","                "functools","                "dataclasses","                "enum","                "pstats","                "csv","                "shlex","                "tempfile","                "shutil","                "traceback","                "itertools","                "base64","                "operator","                "contextlib","                "glob","                "signal","                "mmap","                "pickle","                "copy","                "socket","                "urllib","                "gc","                "pkg_resources","                "importlib","                "fnmatch","                "difflib","                "ast","                "argparse","                "unittest","                "tempfile","                "shutil","                "posixpath","                "ntpath","                "configparser","                "bisect","                "array","                "struct","                "heapq","                "weakref","                "threading","                "queue","                "zipfile","                "tarfile","                "zlib","                "gzip","                "bz2","                "lzma","                "hashlib","                "hmac","                "secrets","                "platform","                "errno","                "ctypes","                "select","                "selectors","                "asyncore","                "asynchat","                "smtplib","                "smtpd","                "telnetlib","                "nntplib","                "ftplib","                "http","                "ftplib","                "xml","                "html","                "cgi","                "cgitb","                "wsgiref","                "urllib","                "xmlrpc","                "runpy","                "py_compile","                "compileall","                "dis","                "pickletools","                "inspect","                "pstats","                "cProfile","                "profile","                "timeit","                "trace","                "tracemalloc","                "graphlib","                "tomllib","                "winreg","                "msvcrt","                "__future__","            ]
        )
    )

    print("--- Dependency Curation Report (Phase 312) ---")"    print(f"Total Unique External Modules Imported: {len(imported_modules)}")"    print(f"Total Modules in requirements/*.txt: {len(req_modules_raw)}")
    print("\\n[UNUSED] (In requirements but not imported in src/):")"    for m in sorted(unused_raw):
        # Filter out common false positives
        if m.lower() not in [
            "pytest","            "ruff","            "mypy","            "pytest-cov","            "black","            "flake8","            "isort","            "pip-tools","            "tox","            "build","            "setuptools","            "wheel","            "twine","        ]:
            print(f"  - {m}")
    print("\\n[MISSING?] (Imported in src/ but not listed in requirements/*.txt):")"    for m in sorted(missing):
        print(f"  - {m}")

if __name__ == "__main__":"    curate_dependencies()

"""
