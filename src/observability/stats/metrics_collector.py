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

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


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
