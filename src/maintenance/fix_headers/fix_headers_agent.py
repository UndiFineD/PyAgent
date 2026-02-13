#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

"""Maintenance: Fix and normalize Python file headers.

Small, well-tested implementation of FixHeadersAgent used by maintenance
scripts to ensure all Python files carry the canonical PyAgent Apache-2.0
header. This file contains a single, correct implementation (no duplicates).
"""


from __future__ import annotations

import os
import re
from pathlib import Path


class FixHeadersAgent:
    """Agent for fixing and standardizing license headers in Python files."""

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
        self.dry_run = dry_run
        self.verbose = verbose
        self.files_processed = 0
        self.files_updated = 0
        self.files_skipped = 0

    def has_proper_header(self, content: str) -> bool:
        return (
            "Copyright 2026 PyAgent Authors" in content and
            "Licensed under the Apache License" in content and
            "http://www.apache.org/licenses/LICENSE-2.0" in content
        )

    def clean_existing_headers(self, content: str) -> str:
        """Safely strip shebang/license headers while preserving encoding comments.

        - Preserves an encoding comment on line 1 or 2 (PEP-263)
        - Handles optional UTF-8 BOM at start
        - Removes only top-of-file comment blocks that look like license/copyright
        """
        if not content:
            return content

        # Remove BOM (remember it so we can re-add if needed)
        has_bom = content.startswith('\ufeff')
        if has_bom:
            content = content.lstrip('\ufeff')

        lines = content.splitlines(keepends=True)

        # Preserve encoding line if present on first or second line
        encoding_line = None
        if lines:
            if re.search(r'coding[:=]', lines[0]):
                encoding_line = lines.pop(0)
            elif len(lines) > 1 and re.search(r'coding[:=]', lines[1]):
                encoding_line = lines.pop(1)

        # Remove shebang if present
        if lines and lines[0].startswith('#!'):
            lines.pop(0)

        # Collect a contiguous top comment block
        top_comment_block = []
        while lines and lines[0].lstrip().startswith('#'):
            top_comment_block.append(lines.pop(0))

        # Drop or filter the top comment block depending on contents
        license_keywords = re.compile(r'copyright|licensed under|apache license', re.I)
        if not any(license_keywords.search(l) for l in top_comment_block):
            # not a license block — keep the whole block
            lines[0:0] = top_comment_block
        else:
            # if mixed, remove only the license-related lines and preserve other comments
            remaining_comments = [l for l in top_comment_block if not license_keywords.search(l)]
            if remaining_comments:
                lines[0:0] = remaining_comments

        cleaned = ''.join(lines).lstrip('\n')
        if encoding_line:
            cleaned = encoding_line + cleaned
        if has_bom:
            cleaned = '\ufeff' + cleaned
        return cleaned

    def add_header(self, content: str) -> str:
        cleaned_content = self.clean_existing_headers(content)
        return self.HEADER_TEMPLATE + "\n" + cleaned_content

    def process_file(self, filepath: Path) -> bool:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if self.has_proper_header(content):
                if self.verbose:
                    print(f"✓ {filepath} - already has proper header")
                self.files_skipped += 1
                return False

            new_content = self.add_header(content)

            if self.dry_run:
                if self.verbose:
                    print(f"🔍 {filepath} - would be updated (dry run)")
                self.files_updated += 1
                return True

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            if self.verbose:
                print(f"✏️  {filepath} - header updated")
            self.files_updated += 1
            return True
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return False

    def process_directory(self, directory: Path, exclude_patterns: set[str] | None = None) -> None:
<<<<<<< HEAD
        if exclude_patterns is None:
"""

from __future__ import annotations

import os
import re
from pathlib import Path


class FixHeadersAgent:
    """Agent for fixing and standardizing license headers in Python files."""

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
        self.dry_run = dry_run
        self.verbose = verbose
        self.files_processed = 0
        self.files_updated = 0
        self.files_skipped = 0

    def has_proper_header(self, content: str) -> bool:
        return (
            "Copyright 2026 PyAgent Authors" in content and
            "Licensed under the Apache License" in content and
            "http://www.apache.org/licenses/LICENSE-2.0" in content
        )

    def clean_existing_headers(self, content: str) -> str:
        """Safely strip shebang/license headers while preserving encoding comments.

        - Preserves an encoding comment on line 1 or 2 (PEP-263)
        - Handles optional UTF-8 BOM at start
        - Removes only top-of-file comment blocks that look like license/copyright
        """
        if not content:
            return content

        # Remove BOM (remember it so we can re-add if needed)
        has_bom = content.startswith('\ufeff')
        if has_bom:
            content = content.lstrip('\ufeff')

        lines = content.splitlines(keepends=True)

        # Preserve encoding line if present on first or second line
        encoding_line = None
        if lines:
            if re.search(r'coding[:=]', lines[0]):
                encoding_line = lines.pop(0)
            elif len(lines) > 1 and re.search(r'coding[:=]', lines[1]):
                encoding_line = lines.pop(1)

        # Remove shebang if present
        if lines and lines[0].startswith('#!'):
            lines.pop(0)

        # Collect a contiguous top comment block
        top_comment_block = []
        while lines and lines[0].lstrip().startswith('#'):
            top_comment_block.append(lines.pop(0))

        # Drop or filter the top comment block depending on contents
        license_keywords = re.compile(r'copyright|licensed under|apache license', re.I)
        if not any(license_keywords.search(l) for l in top_comment_block):
            # not a license block — keep the whole block
            lines[0:0] = top_comment_block
        else:
            # if mixed, remove only the license-related lines and preserve other comments
            remaining_comments = [l for l in top_comment_block if not license_keywords.search(l)]
            if remaining_comments:
                lines[0:0] = remaining_comments

        cleaned = ''.join(lines).lstrip('\n')
        if encoding_line:
            cleaned = encoding_line + cleaned
        if has_bom:
            cleaned = '\ufeff' + cleaned
        return cleaned

    def add_header(self, content: str) -> str:
        cleaned_content = self.clean_existing_headers(content)
        return self.HEADER_TEMPLATE + "\n" + cleaned_content

    def process_file(self, filepath: Path) -> bool:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if self.has_proper_header(content):
                if self.verbose:
                    print(f"✓ {filepath} - already has proper header")
                self.files_skipped += 1
                return False

            new_content = self.add_header(content)

            if self.dry_run:
                if self.verbose:
                    print(f"🔍 {filepath} - would be updated (dry run)")
                self.files_updated += 1
                return True

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            if self.verbose:
                print(f"✏️  {filepath} - header updated")
            self.files_updated += 1
            return True
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return False

    def process_directory(self, directory: Path, exclude_patterns: set[str] | None = None) -> None:
=======
>>>>>>> origin/main
        if exclude_patterns is None:
            exclude_patterns = {'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'}
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in exclude_patterns]
            for file in files:
                if file.endswith('.py'):
                    filepath = Path(root) / file
                    self.process_file(filepath)
                    self.files_processed += 1

    def get_summary(self) -> str:
        return (
            f"\nHeader Fix Summary:\n"\
            f"==================\n"\
            f"Files processed: {self.files_processed}\n"\
            f"Files updated:    {self.files_updated}\n"\
            f"Files skipped:    {self.files_skipped}\n"\
            f"Mode:             {'DRY RUN' if self.dry_run else 'LIVE'}\n"
        )

    def run(self, target: str | Path, exclude_patterns: set[str] | None = None) -> None:
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
