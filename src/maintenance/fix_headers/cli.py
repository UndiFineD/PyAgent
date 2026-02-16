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
Fix Headers CLI - Command-line entry point for fixing Apache 2.0 license headers

[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
python -m src.maintenance.fix_headers.cli <file_or_directory>
python -m src.maintenance.fix_headers.cli --dry-run --verbose <dir>
python -m src.maintenance.fix_headers.cli --exclude tests --exclude vendor single_file.py

WHAT IT DOES:
Provides a small argparse-based CLI that constructs and runs a FixHeadersAgent to
ensure Python files contain the correct Apache 2.0 license header and PyAgent
copyright notice; supports dry-run, verbose output, and simple exclude patterns.

WHAT IT SHOULD DO BETTER:
- Validate and normalize the target path(s) and support multiple targets or glob
  patterns.
- Provide better error handling and exit codes for common failures (permission
  errors, invalid target).
- Allow configurable exclude patterns via a config file or environment variable,
  and support more advanced pattern matching (glob/regex).
- Add unit tests for CLI parsing and integration tests for dry-run vs. write
  modes.
- Improve logging (structured logs, levels) instead of relying solely on verbose
  boolean.

FILE CONTENT SUMMARY:
CLI interface for the Fix Headers Tool.
"""

import argparse

from .fix_headers_agent import FixHeadersAgent


def main():
    """CLI entry point for the Fix Headers Tool."""
    parser = argparse.ArgumentParser(
        description="Fix Apache 2.0 headers in Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.maintenance.fix_headers.cli src/logic/agents/
  python -m src.maintenance.fix_headers.cli --dry-run --verbose src/
  python -m src.maintenance.fix_headers.cli single_file.py

This tool ensures all Python files have proper Apache 2.0 license headers
with PyAgent copyright notices.
        """
    )

    parser.add_argument(
        'target',
        help='File or directory to process'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Provide detailed output for each file'
    )

    parser.add_argument(
        '--exclude',
        action='append',
        help='Directory patterns to exclude (can be used multiple times)'
    )

    args = parser.parse_args()

    exclude_patterns = set(args.exclude or [])
    exclude_patterns.update({'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'})

    agent = FixHeadersAgent(dry_run=args.dry_run, verbose=args.verbose)
    agent.run(args.target, exclude_patterns)


if __name__ == "__main__":
    main()
