#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/reports/report_generator_cli.description.md

# Description: src/observability/reports/report_generator_cli.py

Module overview:
- CLI entrypoint for running `ReportGenerator` and exporting the dashboard.
- Adds project root to `sys.path` for ease of invocation.

Primary functions:
- `main()`: parses arguments and writes `report.html` and `PROGRESS_DASHBOARD.md` to the output directory.

Notes:
- Includes a small helper `_sha256_text` used by legacy tests.
## Source: src-old/observability/reports/report_generator_cli.improvements.md

# Improvements: src/observability/reports/report_generator_cli.py

Suggested improvements (automatically generated):
- Add unit tests covering core behavior and edge cases.
- Break large modules into smaller, testable components.
- Avoid heavy imports at module import time; import lazily where appropriate.
- Add type hints and explicit return types for public functions.
- Add logging and better error handling for file and IO operations.
- Consider dependency injection for filesystem and environment interactions.

LLM_CONTEXT_END
"""

from __future__ import annotations

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


from argparse import Namespace
import sys
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.observability.reports.export_format import ExportFormat
from src.observability.reports.report_exporter import ReportExporter
from src.observability.reports.report_generator import ReportGenerator

root: Path = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

__version__: str = VERSION

"""
Report generator cli.py module.
"""


def _sha256_text(text: str) -> str:
    """Helper for legacy tests."""
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ReportGeneratorCli:
    """Minimal CLI wrapper used by the package and tests.

    Provides a small programmatic interface for generating and exporting
    reports without executing top-level CLI behavior at import time.
    """

    def __init__(self, directory: str = ".", output: str = "reports") -> None:
        self.directory = directory
        self.output = output

    def run(self) -> str:
        generator = ReportGenerator(self.directory)
        report: str = generator.generate_full_report()

        output_dir = Path(self.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        exporter = ReportExporter()
        exporter.export(report, ExportFormat.HTML, output_dir / "report.html")
        (output_dir / "PROGRESS_DASHBOARD.md").write_text(report, encoding="utf-8")

        return str(output_dir)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate Agent Reports")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    parser.add_argument("--output", default="reports", help="Output directory")
    args: Namespace = parser.parse_args()

    cli = ReportGeneratorCli(directory=args.dir, output=args.output)
    out = cli.run()
    print(f"Reports generated in {out}")


if __name__ == "__main__":
    main()
