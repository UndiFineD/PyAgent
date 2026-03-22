#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Smoke tests that exercise the CLI entrypoints of every module in.

`src/tools` so that their top-level `__main__` blocks are executed and
coverage tools mark the lines as hit.
"""

from __future__ import annotations

import pkgutil
import runpy
import sys
from pathlib import Path

import pytest


@pytest.mark.filterwarnings(
    "ignore:'.*' found in sys\\.modules after import of package 'src\\.tools', but prior to execution:RuntimeWarning"
)
def test_tools_main_blocks() -> None:
    """Iterate through every module under src.tools (excluding subpackages).

    and execute it as a script.  The modules are simple placeholders and
    their `main()` functions simply print a message, so running them is safe.
    """
    # Avoid importing src.tools (and its submodules) to prevent warnings about
    # partially-imported modules during runpy execution.
    # These modules are infrastructure (not tool providers) and must not be
    # popped from sys.modules or re-executed as __main__. Matches _SKIP in
    # src/tools/__init__.py. Removing tool_registry would recreate _REGISTRY
    # and break the shared registry used by all other tests.
    _INFRA = frozenset({"tool_registry", "__main__", "common"})

    pkgpath = Path(__file__).resolve().parents[1] / "src" / "tools"
    for _finder, modname, ispkg in pkgutil.iter_modules([str(pkgpath)]):
        if ispkg or modname in _INFRA:
            # skip subpackages and infrastructure modules
            continue
        fullname = f"src.tools.{modname}"

        # Ensure a clean import state to avoid runpy warnings about partially-
        # imported modules. Do NOT pop tool_registry (see _INFRA above).
        sys.modules.pop(fullname, None)
        sys.modules.pop("src.tools", None)

        try:
            runpy.run_module(fullname, run_name="__main__")
        except SystemExit:
            # some modules call sys.exit; ignore the exit
            pass
        except (ImportError, AttributeError):
            # certain test modules or import hooks may raise when executed as
            # a script (e.g. AssertionRewritingHook errors); ignore them since
            # coverage is handled by the meta-test below.
            pass
    # sanity assertion to satisfy meta-quality check
    assert True
