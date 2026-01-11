#!/usr/bin/env python3
from __future__ import annotations
# Copyright (c) 2025 PyAgent contributors


































from src.core.base.version import VERSION
__version__ = VERSION

"""Agent specializing in collecting and reporting project development statistics."""

import sys
import argparse
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.observability.stats import *
from src.observability.stats.StatsAgent import StatsAgent

def main() -> None:
    parser = argparse.ArgumentParser(description='Stats Agent: Reports statistics on file update progress')
    parser.add_argument('--files', nargs='+', help='List of files to analyze')
    parser.add_argument('--dir', help='Directory to analyze (recursive)')
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text', help='Output format')
    args = parser.parse_args()
    
    files = args.files or []
    if args.dir:
        # Avoid including hidden folders or common ignored directories
        path = Path(args.dir)
        for p in path.rglob('*'):
            if p.is_file() and not any(part.startswith('.') or part in ['__pycache__', 'venv'] for part in p.parts):
                files.append(str(p))
                
    if not files:
        # Fallback to simple scan of current dir if no input
        files = [str(p) for p in Path('.').glob('*.py')]
        
    agent = StatsAgent(files)
    agent.report_stats(output_format=args.format)

if __name__ == '__main__':
    main()
