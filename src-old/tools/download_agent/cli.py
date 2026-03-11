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

"""LLM_CONTEXT_START

## Source: src-old/tools/download_agent/cli.description.md

# cli

**File**: `src\tools\\download_agent\\cli.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 6 imports  
**Lines**: 184  
**Complexity**: 2 (simple)

## Overview

CLI interface for the Download Agent.

## Functions (2)

### `print_results_summary(results)`

Print a summary of download results.

### `main()`

Main CLI entry point.

## Dependencies

**Imports** (6):
- `argparse`
- `core.DownloadAgent`
- `models.DownloadConfig`
- `models.DownloadResult`
- `sys`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/tools/download_agent/cli.improvements.md

# Improvements for cli

**File**: `src\tools\\download_agent\\cli.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 184 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `cli_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
CLI interface for the Download Agent.
"""

import argparse
import sys
from typing import List

from .core import DownloadAgent
from .models import DownloadConfig, DownloadResult


def print_results_summary(results: List[DownloadResult]):
    """Print a summary of download results."""
    if not results:
        print("No URLs processed.")
        return

    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    skipped = [r for r in results if r.metadata and r.metadata.get("skipped")]
    dry_run = [r for r in results if r.metadata and r.metadata.get("dry_run")]

    print("\n📊 Download Summary")
    print("=" * 50)
    print(f"Total URLs processed: {len(results)}")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"⏭️  Skipped: {len(skipped)}")
    print(f"🔍 Dry run: {len(dry_run)}")

    if successful:
        total_size = sum(r.size_bytes for r in successful)
        print(f"📦 Total downloaded: {total_size:,} bytes")

    if failed:
        print("\n❌ Failed downloads:")
        for result in failed:
            print(f"  - {result.url}: {result.error_message}")

    # Group by type
    type_counts = {}
    for result in results:
        type_counts[result.file_type] = type_counts.get(result.file_type, 0) + 1

    print("\n📁 Content types:")
    for file_type, count in sorted(type_counts.items()):
        print(f"  - {file_type}: {count}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PyAgent Download Agent - Handle different URL types with appropriate mechanisms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.tools.download_agent.cli                          # Process docs/download/urls.txt
  python -m src.tools.download_agent.cli --dry-run               # Show what would be downloaded
  python -m src.tools.download_agent.cli --verbose               # Detailed output
  python -m src.tools.download_agent.cli --output results.json   # Save results to file
  python -m src.tools.download_agent.cli --urls-file custom.txt  # Use custom URLs file

Supported URL types:
  • GitHub repos: git clone to .external/
  • GitHub gists: git clone to .external/gists/
  • ArXiv papers: download PDF to data/research/
  • Research PDFs: download to data/research/
  • Datasets: download to data/datasets/
  • Documentation: download to docs/external/
  • Web pages: download HTML to data/webpages/
        """,
    )

    parser.add_argument(
        "--urls-file",
        default="docs/download/urls.txt",
        help="Path to URLs file (default: docs/download/urls.txt)",
    )

    parser.add_argument(
        "--base-dir", default=".", help="Base directory for relative paths (default: .)"
    )

    parser.add_argument(
        "--max-retries", type=int, default=3, help="Maximum retry attempts (default: 3)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Download timeout in seconds (default: 30)",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between downloads in seconds (default: 1.0)",
    )

    parser.add_argument("--output", help="Save results to JSON file")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading",
    )

    parser.add_argument(
        "--no-skip-existing",
        action="store_true",
        help="Download even if file/directory already exists",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    config = DownloadConfig(
        urls_file=args.urls_file,
        base_dir=args.base_dir,
        max_retries=args.max_retries,
        timeout_seconds=args.timeout,
        delay_between_downloads=args.delay,
        skip_existing=not args.no_skip_existing,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    agent = DownloadAgent(config)

    print("🚀 PyAgent Download Agent")
    print("=" * 50)
    print(f"URLs file: {config.urls_file}")
    print(f"Base directory: {config.base_dir}")
    print(f"Mode: {'DRY RUN' if config.dry_run else 'LIVE'}")
    print(f"Skip existing: {config.skip_existing}")
    print()

    try:
        results = agent.process_urls_file()
        print_results_summary(results)

        if args.output:
            agent.save_results(results, args.output)

    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
