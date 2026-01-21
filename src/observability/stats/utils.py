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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import argparse
import json
import logging
import sys
import contextlib
from .stats_agent import StatsAgent

__version__ = VERSION


def main() -> None:
    """CLI entry point for the Stats Agent."""
    parser = argparse.ArgumentParser(
        description="Stats Agent: Reports file update statistics",
        epilog="Example: python src/agent_stats.py --files src/*.py",
    )
    parser.add_argument(
        "--files", nargs="+", required=True, help="List of files to analyze"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format",
    )
    parser.add_argument("--coverage", help="Path to code coverage report")
    parser.add_argument(
        "--export", nargs="+", help="Export formats (json, csv, html, sqlite)"
    )
    parser.add_argument("--baseline", help="Path to baseline stats for comparison")
    parser.add_argument("--verbose", default="normal", help="Verbosity level")
    parser.add_argument(
        "--no-cascade", action="store_true", help="Unused, for compatibility"
    )
    args = parser.parse_args()

    # Setup logging
    levels = {
        "quiet": logging.ERROR,
        "minimal": logging.WARNING,
        "normal": logging.INFO,
        "elaborate": logging.DEBUG,
    }
    level = levels.get(args.verbose.lower(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        agent = StatsAgent(args.files)
        if args.coverage:
            agent.track_code_coverage(args.coverage)
        if args.export:
            agent.export_stats("stats_output", args.export)
        if args.baseline:
            with open(args.baseline) as baseline_file:
                baseline_stats = json.load(baseline_file)
            agent.generate_comparison_report(baseline_stats)
        agent.report_stats(output_format=args.format)
        
        # Visualize only if requested and available
        with contextlib.suppress(ImportError):
            import matplotlib
            agent.visualize_stats()
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
