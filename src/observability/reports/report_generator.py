#!/usr/bin/env python3
from __future__ import annotations
# Copyright (c) 2025 PyAgent contributors

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports

































from src.core.base.version import VERSION
__version__ = VERSION

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.observability.reports import *

def _sha256_text(text: str) -> str:
    """Helper for legacy tests."""
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Generate Agent Reports')
    parser.add_argument('--dir', default='.', help='Directory to scan')
    parser.add_argument('--output', default='reports', help='Output directory')
    args = parser.parse_args()
    
    generator = ReportGenerator(args.dir)
    report = generator.generate_full_report()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    exporter = ReportExporter()
    # Export as HTML to the output directory
    exporter.export(report, ExportFormat.HTML, output_dir / "report.html")
    # Also save the markdown version as the progress dashboard
    (output_dir / "PROGRESS_DASHBOARD.md").write_text(report, encoding="utf-8")
    
    print(f"Reports generated in {args.output}")

if __name__ == '__main__':
    main()
