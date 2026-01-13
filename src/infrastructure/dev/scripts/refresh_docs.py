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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Documentation refresh and regeneration utility.

Automatically regenerates project documentation based on current codebase state,
including API docs, architecture diagrams, and status reports.
"""
from __future__ import annotations
from src.core.base.version import VERSION
import logging
import sys
import os
from src.observability.reports.ReportGenerator import ReportGenerator
from pathlib import Path

os.environ["PYTHONPATH"] = "."
__version__ = VERSION

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s: %(message)s")

def main() -> None:
    agent_dir = Path("src")
    output_dir = Path("docs/autodoc")
    
    print(f"Refreshing autodoc: {agent_dir} -> {output_dir}")
    generator = ReportGenerator(agent_dir=agent_dir, output_dir=output_dir)
    results = generator.process_all_files()
    print(f"\nResults: {results}")

if __name__ == "__main__":
    main()