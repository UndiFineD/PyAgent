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
Duplicate code detection logic for CoderCore.
"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


class CoderDuplicationMixin:
    """Mixin for identifying duplicate code."""

    def find_duplicate_code(self, content: str, min_lines: int = 4) -> List[Dict[str, Any]]:
        """Find duplicate code blocks using hashing."""
        # Rust-accelerated sliding window hash
        try:
            import rust_core as rc

            rust_result = rc.find_duplicate_code_rust(content, min_lines)  # type: ignore[attr-defined]
            # Convert Rust output format to expected dicts
            duplicates: List[Dict[str, Any]] = []
            for hash_val, line_nums in rust_result.items():
                if len(line_nums) > 1:
                    lines = content.split("\n")
                    preview_start = line_nums[0] - 1
                    duplicates.append(
                        {
                            "hash": hash_val,
                            "occurrences": len(line_nums),
                            "lines": line_nums,
                            "preview": "\n".join(lines[preview_start : preview_start + min_lines])[:100],
                        }
                    )
            return duplicates
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
            pass

        return self._find_duplicate_code_fallback(content, min_lines)

    def _find_duplicate_code_fallback(self, content: str, min_lines: int) -> List[Dict[str, Any]]:
        """Non-Rust fallback for duplicate detection."""
        lines = content.split("\n")
        duplicates = []
        hashes: Dict[str, List[int]] = {}

        for i in range(len(lines) - min_lines + 1):
            block = "\n".join(lines[i : i + min_lines])
            normalized = re.sub(r"\s+", " ", block.strip())
            if len(normalized) < 20:
                continue

            block_hash = hashlib.md5(normalized.encode()).hexdigest()
            if block_hash not in hashes:
                hashes[block_hash] = []
            hashes[block_hash].append(i + 1)

        for block_hash, line_numbers in hashes.items():
            if len(line_numbers) > 1:
                duplicates.append(
                    {
                        "hash": block_hash,
                        "occurrences": len(line_numbers),
                        "lines": line_numbers,
                        "preview": "\n".join(lines[line_numbers[0] - 1 : line_numbers[0] - 1 + min_lines])[:100],
                    }
                )
        return duplicates
