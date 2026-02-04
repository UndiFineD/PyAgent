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
Fix Headers Agent for PyAgent.

This agent ensures all Python files have proper Apache 2.0 license headers
and copyright notices. It can process individual files or entire directory
trees, making it useful for maintaining code quality across the PyAgent fleet.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Set


class FixHeadersAgent:
    """
    Agent for fixing and standardizing license headers in Python files.

    This agent ensures all Python files in the PyAgent codebase have consistent
    Apache 2.0 license headers with proper copyright notices. It can process
    individual files, directories, or entire project trees.
    """

    # Standard Apache 2.0 header for PyAgent
    HEADER_TEMPLATE = """#!/usr/bin/env python3
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

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """
        Initialize the FixHeadersAgent.

        Args:
            dry_run: If True, only show what would be changed without modifying files
            verbose: If True, provide detailed output for each file processed
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.files_processed = 0
        self.files_updated = 0
        self.files_skipped = 0

    def has_proper_header(self, content: str) -> bool:
        """
        Check if a file already has the proper PyAgent header.

        Args:
            content: The file content to check

        Returns:
            True if the file has the proper header, False otherwise
        """
        return (
            "Copyright 2026 PyAgent Authors" in content and
            "Licensed under the Apache License" in content and
            "http://www.apache.org/licenses/LICENSE-2.0" in content
        )

    def clean_existing_headers(self, content: str) -> str:
        """
        Remove existing shebang and copyright headers from content.

        Args:
            content: The original file content

        Returns:
            Content with existing headers removed
        """
        # Remove existing shebang
        content = re.sub(r'^#!.*?\n', '', content, flags=re.MULTILINE)

        # Remove existing copyright/license headers (multi-line)
        content = re.sub(
            r'^# Copyright.*?(?:\n#(?!#).*?)*?\n',
            '',
            content,
            flags=re.MULTILINE
        )

        # Remove any leading empty lines
        content = content.lstrip()

        return content

    def add_header(self, content: str) -> str:
        """
        Add the standard PyAgent header to file content.

        Args:
            content: The original file content

        Returns:
            Content with the proper header added
        """
        # Clean existing headers first
        cleaned_content = self.clean_existing_headers(content)

        # Add the new header
        return self.HEADER_TEMPLATE + "\n" + cleaned_content

    def process_file(self, filepath: Path) -> bool:
        """
        Process a single Python file to fix its header.

        Args:
            filepath: Path to the Python file to process

        Returns:
            True if the file was updated, False if it was skipped
        """
        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if header is already correct
            if self.has_proper_header(content):
                if self.verbose:
                    print(f"✓ {filepath} - already has proper header")
                self.files_skipped += 1
                return False

            # Generate new content with proper header
            new_content = self.add_header(content)

            if self.dry_run:
                if self.verbose:
                    print(f"🔍 {filepath} - would be updated (dry run)")
                self.files_updated += 1
                return True
            else:
                # Write the updated content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                if self.verbose:
                    print(f"✏️  {filepath} - header updated")
                self.files_updated += 1
                return True

        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return False

    def process_directory(self, directory: Path, exclude_patterns: Set[str] = None) -> None:
        """
        Process all Python files in a directory tree.

        Args:
            directory: Root directory to process
            exclude_patterns: Set of directory names to exclude (e.g., {'__pycache__', '.git'})
        """
        if exclude_patterns is None:
            exclude_patterns = {'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'}

        for root, dirs, files in os.walk(directory):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_patterns]

            for file in files:
                if file.endswith('.py'):
                    filepath = Path(root) / file
                    self.process_file(filepath)
                    self.files_processed += 1

    def get_summary(self) -> str:
        """
        Get a summary of the processing results.

        Returns:
            A formatted summary string
        """
        return f"""
Header Fix Summary:
==================
Files processed: {self.files_processed}
Files updated:    {self.files_updated}
Files skipped:    {self.files_skipped}
Mode:             {'DRY RUN' if self.dry_run else 'LIVE'}
"""

    def run(self, target: str | Path, exclude_patterns: Set[str] = None) -> None:
        """
        Run the header fixing process on a target.

        Args:
            target: File or directory path to process
            exclude_patterns: Directory patterns to exclude
        """
        target_path = Path(target)

        if target_path.is_file():
            if target_path.suffix == '.py':
                self.process_file(target_path)
                self.files_processed = 1
            else:
                print(f"❌ {target} is not a Python file")
                return
        elif target_path.is_dir():
            self.process_directory(target_path, exclude_patterns)
        else:
            print(f"❌ {target} does not exist")
            return

        print(self.get_summary())


def main():
    """CLI entry point for the Fix Headers Agent."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fix Apache 2.0 headers in Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.maintenance.fix_headers_agent src/logic/agents/
  python -m src.maintenance.fix_headers_agent --dry-run --verbose src/
  python -m src.maintenance.fix_headers_agent single_file.py

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