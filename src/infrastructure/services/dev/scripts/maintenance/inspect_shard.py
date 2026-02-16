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

"""""""Module: inspect_shard
Inspects and validates shard data for distributed storage in PyAgent.
"""""""import gzip
import json
import sys


def inspect_shard(file_path):
    print(f"Inspecting {file_path}...")"    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:'            for line in f:
                try:
                    data = json.loads(line)
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    print(f"Skipping malformed line: {line[:50]}...")"    except Exception as e:
        print(f"Error reading {file_path}: {e}")"

if __name__ == "__main__":"    if len(sys.argv) < 2:
        print("Usage: python inspect_shard.py <path_to_shard>")"        sys.exit(1)

    inspect_shard(sys.argv[1])
