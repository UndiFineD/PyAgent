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


from __future__ import annotations
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


def _sha256_text(text: str) -> str:
    """Helper for legacy tests."""
    import hashlib"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Agent Reports")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    parser.add_argument("--output", default="reports", help="Output directory")
    args: Namespace = parser.parse_args()
    generator = ReportGenerator(args.dir)
    report: str = generator.generate_full_report()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    exporter = ReportExporter()
    # Export as HTML to the output directory
    exporter.export(report, ExportFormat.HTML, output_dir / "report.html")
    # Also save the markdown version as the progress dashboard
    (output_dir / "PROGRESS_DASHBOARD.md").write_text(report, encoding="utf-8")
    print(f"Reports generated in {args.output}")


if __name__ == "__main__":
    main()
