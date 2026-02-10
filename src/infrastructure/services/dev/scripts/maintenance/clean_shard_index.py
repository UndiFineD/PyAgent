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
Module: clean_shard_index
Cleans and rebuilds the shard index for distributed storage in PyAgent.
"""
import os

files_to_clean = [
    "data/logs/external_ai_learning/shards_lookup.index",
    "data/memory/logs/external_ai_learning/shards_lookup.index"
]

shards_to_remove = [
    "shard_202601_029.jsonl.gz",
    "shard_202601_032.jsonl.gz",
    "shard_202601_032_jsonl.gz",  # Just in case
    "shard_202601_029_jsonl.gz"
]

for file_path in files_to_clean:
    full_path = os.path.abspath(file_path)
    print(f"Checking {full_path}...")
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue

    print(f"Cleaning {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        removed_count = 0
        for line in lines:
            if any(s in line for s in shards_to_remove):
                removed_count += 1
            else:
                new_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"Removed {removed_count} lines from {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Cleanup complete.")
