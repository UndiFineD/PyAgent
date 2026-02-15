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
Fleet Loop Analysis Tool

A command-line utility for analyzing loop anti-patterns across PyAgent fleet projects.
Uses the reusable LoopAnalyzer module for consistent analysis across all projects.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.specialists.loop_analyzer import LoopAnalyzer, LoopAnalysisConfig, print_analysis_report


def main():
    """Main CLI entry point for fleet loop analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="PyAgent Fleet Loop Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python loop_analysis.py src/                                    # Analyze src directory
  python loop_analysis.py . --min-loc 100 --min-loops 2          # Custom thresholds
  python loop_analysis.py src/ --exclude .venv __pycache__ node_modules
  python loop_analysis.py .external/automem-ai-memory/           # Analyze specific repo
        """
    )

    parser.add_argument(
        "directory",
        help="Directory to analyze (use '.' for current directory)"
    )

    parser.add_argument(
        "--min-loc",
        type=int,
        default=200,
        help="Minimum lines of code threshold (default: 200)"
    )

    parser.add_argument(
        "--min-loops",
        type=int,
        default=3,
        help="Minimum loop count threshold (default: 3)"
    )

    parser.add_argument(
        "--exclude",
        nargs='*',
        default=['.venv', '__pycache__', 'node_modules', '.git', 'target', 'build'],
        help="Directories to exclude (default: .venv __pycache__ node_modules .git target build)"
    )

    parser.add_argument(
        "--format",
        choices=['summary', 'detailed', 'json'],
        default='summary',
        help="Output format (default: summary)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file for results (optional)"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)

    # Create configuration
    config = LoopAnalysisConfig(
        min_loc_threshold=args.min_loc,
        min_loop_threshold=args.min_loops,
        exclude_dirs=set(args.exclude)
    )

    # Run analysis
    analyzer = LoopAnalyzer(config)

    if not args.quiet:
        print(f"🔍 Analyzing directory: {args.directory}")
        print(f"📊 Configuration: min_loc={args.min_loc}, min_loops={args.min_loops}")
        print(f"🚫 Excluding: {', '.join(args.exclude)}")
        print("⏳ Scanning files... (this may take a moment)")

    try:
        if args.format == 'detailed':
            analysis = analyzer.analyze_directory(args.directory)
            candidates = analysis['candidates']
            all_files = analysis['all_files']
        else:
            candidates = analyzer.find_candidates(args.directory)
            all_files = None

        # Output results
        if args.format == 'json':
            import json
            results = {
                'candidates': [
                    {
                        'file_path': r.file_path,
                        'lines_of_code': r.lines_of_code,
                        'loop_count': r.loop_count,
                        'complexity_score': r.complexity_score,
                        'loop_density': r.loop_density,
                        'has_nested_loops': r.has_nested_loops,
                        'has_deep_nesting': r.has_deep_nesting,
                        'has_large_loops': r.has_large_loops
                    } for r in candidates
                ]
            }
            output = json.dumps(results, indent=2)
        else:
            # Capture print output for file writing
            from io import StringIO
            import contextlib

            output_buffer = StringIO()
            with contextlib.redirect_stdout(output_buffer):
                print_analysis_report(candidates, "🚨 High Priority Loop Candidates")

                if args.format == 'detailed' and all_files:
                    print_analysis_report(all_files[:10], "📈 Top 10 Files by Complexity Score")

            output = output_buffer.getvalue()

        # Print to console
        print(output)

        # Write to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"💾 Results saved to: {args.output}")

    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()