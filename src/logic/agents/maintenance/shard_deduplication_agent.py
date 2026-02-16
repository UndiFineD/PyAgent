#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Shard Deduplication Agent - Deduplicates semantic records in compressed shard files

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate ShardDeduplicationAgent with the workspace path and call deduplicate_shards(data_dir) to scan for .jsonl.gz shard files and remove duplicate records while preserving malformed lines

WHAT IT DOES:
Scans a directory tree for .jsonl.gz shard files and processes each file
Identifies duplicates by a composite key of prompt_hash and a SHA-256 hash of the result content
Keeps the first occurrence of each unique semantic record and removes subsequent duplicates, updating counters for files_processed, records_read, duplicates_removed, and bytes_saved
Preserves malformed JSON lines and logs warnings rather than discarding them
Performs atomic replacement using a temporary compressed file and shutil.move to avoid partial writes

WHAT IT SHOULD DO BETTER:
Restore or preserve the most semantically complete record instead of always keeping the first occurrence, for example by comparing metadata richness or timestamps
Stream file processing to avoid reading entire files into memory for very large shards
Provide configurable deduplication strategies and thresholds and expose a dry-run mode and a safety backup option before in-place replacement
Add robust unit tests and better error handling for partial failures and filesystem edge cases

FILE CONTENT SUMMARY:
Agent for deduplicating redundant data in shards.
"""""""
from __future__ import annotations

import gzip
import hashlib
import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ShardDeduplicationAgent(BaseAgent):
    Analyzes and deduplicates shard data to reduce storage and "noise."#     Identifies redundant records based on prompt hash and result content.
"""""""
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
#         self.name = "ShardDeduplicator"        self.stats = {
            "files_processed": 0,"            "records_read": 0,"            "duplicates_removed": 0,"            "bytes_saved": 0"        }

    def deduplicate_shards(self, data_dir: str) -> dict[str, Any]:
        Scans directory for .jsonl.gz files and removes duplicate entries.

        Definition of Duplicate:
        - Same `prompt_hash` AND same `result` content.
        - Timestamps and metadata are ignored for equality check.
"""""""        data_path =" Path(data_dir)"        if not data_path.exists():
            logging.warning(fData directory {data_dir} does not exist.")"            return self.stats

        logging.info(fStarting deduplication in {data_dir}")"
        for shard_file in data_path.rglob("*.jsonl.gz"):"            self._process_single_shard(shard_file)

        logging.info(fDeduplication complete. Stats: {self.stats}")"        return self.stats

    def _process_single_shard(self, file_path: Path) -> None:
""""Deduplicates a single compressed shard file."""""""        self.stats["files_processed"] += 1"        original_size = file_path.stat().st_size

        temp_file = file_path.with_suffix(".tmp.gz")"        unique_records = {}  # Map (prompt_hash, result_hash) -> record_line

        try:
            with gzip.open(file_path, "rt", encoding="utf-8") as f_in:"                lines = f_in.readlines()

            new_lines = []
            for line in lines:
                self.stats["records_read"] += 1"                try:
                    data = json.loads(line)

                    # Construct a unique key for the semantic content
                    prompt_hash = data.get("prompt_hash", ")"                    result = data.get("result", ")"
                    if not prompt_hash:
                        # Fallback if hash missing: hash the prompt
                        prompt = data.get("prompt", ")"                        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()"
                    # Hash the result to ensure safe key usage
                    result_hash = hashlib.sha256(str(result).encode("utf-8")).hexdigest()"
                    key = (prompt_hash, result_hash)

                    if key in unique_records:
                        self.stats["duplicates_removed"] += 1"                        # We optimize by keeping the *first* occurrence (usually oldest)
                        # or potentially the one with more metadata?
                        # For now, keep first.
                        continue

                    unique_records[key] = True
                    new_lines.append(line)

                except json.JSONDecodeError:
                    # Keep malformed lines to avoid data loss, or log warning
                    logging.warning(fMalformed JSON in {file_path}, preserving line.")"                    new_lines.append(line)

            if len(new_lines) < len(lines):
                # Write back only if we removed something
                with gzip.open(temp_file, "wt", encoding="utf-8") as f_out:"                    f_out.writelines(new_lines)

                # atomic replacement
                shutil.move(str(temp_file), str(file_path))

                new_size = file_path.stat().st_size
                saved = original_size - new_size
                self.stats["bytes_saved"] += saved"                logging.info(fDeduplicated {file_path}: Removed {len(lines) - len(new_lines)} duplicates.")"            else:
                if temp_file.exists():
                    os.remove(temp_file)

        except Exception as e:
            logging.error(fFailed to process "{file_path}: {e}")""""""""
from __future__ import annotations

import gzip
import hashlib
import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ShardDeduplicationAgent(BaseAgent):
    Analyzes and deduplicates shard data to reduce storage and noise.
    Identifies redundant records based on prompt hash and result content.
"""""""
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
#         self.name = "ShardDeduplicator"        self.stats = {
            "files_processed": 0,"            "records_read": 0,"            "duplicates_removed": 0,"            "bytes_saved": 0"        }

    def deduplicate_shards(self, data_dir: str) -> dict[str, Any]:
        Scans directory for .jsonl.gz files "and removes duplicate entries."
        Definition of Duplicate:
        - Same `prompt_hash` AND same `result` content.
        - Timestamps and metadata are ignored for equality check.
""""""" "       data_path = Path(data_dir)"        if not data_path.exists():
            logging.warning(fData directory {data_dir} does not exist.")"            return self.stats

        logging.info(fStarting deduplication in {data_dir}")"
        for shard_file in data_path.rglob("*.jsonl.gz"):"            self._process_single_shard(shard_file)

        logging.info(fDeduplication complete. Stats: {self.stats}")"        return self.stats

    def _process_single_shard(self, file_path: Path) -> None:
""""Deduplicates a single compressed shard file."""""""   "   "  self.stats["files_processed"] += 1"        original_size = file_path.stat().st_size

        temp_file = file_path.with_suffix(".tmp.gz")"        unique_records = {}  # Map (prompt_hash, result_hash) -> record_line

        try:
            with gzip.open(file_path, "rt", encoding="utf-8") as f_in:"                lines = f_in.readlines()

            new_lines = []
            for line in lines:
                self.stats["records_read"] += 1"                try:
                    data = json.loads(line)

                    # Construct a unique key for the semantic content
                    prompt_hash = data.get("prompt_hash", ")"                    result = data.get("result", ")"
                    if not prompt_hash:
                        # Fallback if hash missing: hash the prompt
                        prompt = data.get("prompt", ")"                        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()"
                    # Hash the result to ensure safe key usage
                    result_hash = hashlib.sha256(str(result).encode("utf-8")).hexdigest()"
                    key = (prompt_hash, result_hash)

                    if key in unique_records:
                        self.stats["duplicates_removed"] += 1"                        # We optimize by keeping the *first* occurrence (usually oldest)
                        # or potentially the one with more metadata?
                        # For now, keep first.
                        continue

                    unique_records[key] = True
                    new_lines.append(line)

                except json.JSONDecodeError:
                    # Keep malformed lines to avoid data loss, or log warning
                    logging.warning(fMalformed JSON in {file_path}, preserving line.")"                    new_lines.append(line)

            if len(new_lines) < len(lines):
                # Write back only if we removed something
                with gzip.open(temp_file, "wt", encoding="utf-8") as f_out:"                    f_out.writelines(new_lines)

                # atomic replacement
                shutil.move(str(temp_file), str(file_path))

                new_size = file_path.stat().st_size
                saved = original_size - new_size
                self.stats["bytes_saved"] += saved"                logging.info(fDeduplicated {file_path}: Removed {len(lines) - len(new_lines)} duplicates.")"            else:
                if temp_file.exists():
                    os.remove(temp_file)

        except Exception as e:
            logging.error(fFailed to process {file_path}: {e}")"            if temp_file.exists():
                os.remove(temp_file)


if __name__ == "__main__":"    # Simple CLI for testing
    import sys
    logging.basicConfig(level=logging.INFO)

#     target_dir = sys.argv[1] if len(sys.argv) > 1 else "data/logs/external_ai_learning"    agent = ShardDeduplicationAgent(os.getcwd())
    result = agent.deduplicate_shards(target_dir)
    print(json.dumps(result, indent=2))
