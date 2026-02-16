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
Dedicated CLI manager for PyAgent Download System.
"""

import sys
import argparse
from pathlib import Path

from src.tools.download_agent.core import DownloadAgent
from src.tools.download_agent.models import DownloadConfig


def main():
    parser = argparse.ArgumentParser(
        description="PyAgent Download Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('url', nargs='?', help='URL to download (direct mode)')
    parser.add_argument('--file', '-f', help='File containing URLs to process')
    parser.add_argument('--output', '-o', default='temp/downloads.json', help='Path to save results')
    parser.add_argument('--dry-run', action='store_true', help='Simulate without downloading')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    config = DownloadConfig(
        urls_file=args.file or "docs/download/urls.txt",
        dry_run=args.dry_run,
        verbose=args.verbose,
        base_dir="."
    )

    agent = DownloadAgent(config)

    if args.url:
        print(f"🚀 Downloading single target: {args.url}")
        result = agent.process_url(args.url)
        agent.save_results([result], args.output)
    elif args.file or Path(config.urls_file).exists():
        print(f"📂 Processing batch file: {config.urls_file}")
        results = agent.process_urls_file()
        agent.save_results(results, args.output)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
