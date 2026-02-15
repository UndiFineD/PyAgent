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
Utils.py - Stats Agent CLI entry point

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- As a CLI: python src/agent_stats.py --files src/*.py --format json
- To export results: python src/agent_stats.py --files src/*.py --export json csv --coverage coverage.xml
- To compare against baseline: python src/agent_stats.py --files src/*.py --baseline baseline_stats.json

WHAT IT DOES:
- Parses CLI arguments to drive the StatsAgent for reporting file update and code metrics.
- Supports multiple output formats (text, json, csv), optional coverage tracking, exporting, baseline comparison, and optional visualization when available.
- Sets up logging verbosity and handles common I/O and JSON errors with clear exit codes.

WHAT IT SHOULD DO BETTER:
- Move CLI wiring into a dedicated lightweight CLI module and keep utils.py limited to pure utility functions; reduce side effects at import.
- Add unit tests around argument parsing and error paths, and validate file globs earlier with clearer user-facing messages.
- Replace broad exception handling with more specific exceptions and ensure visualization import errors are explicitly logged at debug level rather than silently suppressed.

FILE CONTENT SUMMARY:
Utils.py module.
"""

# you may not use this file except in compliance with the License.
# you may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import sys

from src.core.base.lifecycle.version import VERSION

from .stats_agent import StatsAgent

__version__ = VERSION


def main() -> None:
    """CLI entry point for the Stats Agent."""
    parser = argparse.ArgumentParser(
        description="Stats Agent: Reports file update statistics",
        epilog="Example: python src/agent_stats.py --files src/*.py",
    )
    parser.add_argument("--files", nargs="+", required=True, help="List of files to analyze")
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format",
    )
    parser.add_argument("--coverage", help="Path to code coverage report")
    parser.add_argument("--export", nargs="+", help="Export formats (json, csv, html, sqlite)")
    parser.add_argument("--baseline", help="Path to baseline stats for comparison")
    parser.add_argument("--verbose", default="normal", help="Verbosity level")
    parser.add_argument("--no-cascade", action="store_true", help="Unused, for compatibility")
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
            with open(args.baseline, encoding='utf-8') as baseline_file:
                baseline_stats = json.load(baseline_file)
            agent.generate_comparison_report(baseline_stats)
        agent.report_stats(output_format=args.format)

        # Visualize only if requested and available
        with contextlib.suppress(ImportError):
            agent.visualize_stats()
    except (OSError, json.JSONDecodeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
