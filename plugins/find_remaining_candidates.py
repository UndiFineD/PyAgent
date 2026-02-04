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

"""
Legacy wrapper for loop analysis - now uses the reusable LoopAnalyzer module.
This file is kept for backward compatibility but delegates to the new implementation.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.specialists.loop_analyzer import LoopAnalyzer, LoopAnalysisConfig, print_analysis_report


def find_candidates_legacy(root_dir):
    """Legacy interface - now uses LoopAnalyzer."""
    config = LoopAnalysisConfig(
        min_loc_threshold=200,
        min_loop_threshold=3,
        exclude_dirs={'.venv', '__pycache__', 'node_modules'}
    )

    analyzer = LoopAnalyzer(config)
    results = analyzer.find_candidates(root_dir)

    # Convert to legacy format for backward compatibility
    candidates = []
    for result in results:
        candidates.append((result.file_path, result.lines_of_code, result.loop_count))

    return sorted(candidates, key=lambda x: x[2], reverse=True)


if __name__ == "__main__":
    src_dir = os.path.join(os.getcwd(), 'src')
    candidates = find_candidates_legacy(src_dir)
    print(f"Found {len(candidates)} profiling candidates:")
    for path, loc, loops in candidates:
        print(f"{path}: LOC={loc}, Loops={loops}")

    print("\n💡 Note: This script now uses the reusable LoopAnalyzer module.")
    print("   For more detailed analysis, use: python loop_analysis.py <directory>")
