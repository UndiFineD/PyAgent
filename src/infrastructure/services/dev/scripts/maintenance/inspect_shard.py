
"""
Module: inspect_shard
Inspects and validates shard data for distributed storage in PyAgent.
"""
import gzip
import json
import sys

def inspect_shard(file_path):
    print(f"Inspecting {file_path}...")
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    print(f"Skipping malformed line: {line[:50]}...")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_shard.py <path_to_shard>")
        sys.exit(1)

    inspect_shard(sys.argv[1])
