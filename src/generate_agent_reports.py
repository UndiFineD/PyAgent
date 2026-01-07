#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.classes.reports import *

def _sha256_text(text: str) -> str:
    """Helper for legacy tests."""
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate Agent Reports')
    parser.add_argument('--dir', default='.', help='Directory to scan')
    parser.add_argument('--output', default='reports', help='Output directory')
    args = parser.parse_args()
    
    generator = ReportGenerator(args.dir)
    report = generator.generate_full_report()
    
    exporter = ReportExporter()
    exporter.export(report, args.output)
    print(f"Reports generated in {args.output}")

if __name__ == '__main__':
    main()
