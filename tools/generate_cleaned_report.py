#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

import os
import re

CLEANED_DIR = r"C:\DEV\PyAgent\src\external_candidates\cleaned"
REPORT_PATH = r"C:\DEV\PyAgent\docs\architecture\external_cleaned.md"

def get_file_purpose(content, filename):
    # Heuristics for purpose
    if "class " in content and "Exception" in content:
        return "Defines custom exception classes for domain-specific error handling and fault tolerance."
    if "test_" in filename or "def test_" in content:
        return "Unit test module providing verification logic and behavioral examples for the associated functionality."
    if "utils" in filename or "util.py" in filename:
        return "Collection of utility functions and helper methods to support core logic and reduce code redundancy."
    if "config" in filename or "settings" in filename:
        return "Configuration handler for managing environment variables, API keys, and operational parameters."
    
    # Try to extract from docstring
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        doc = docstring_match.group(1).strip().split('\n')[0]
        if len(doc) > 10:
            return doc
            
    # Try to extract from the header comments (ingestion metadata)
    metadata_match = re.search(r'# Extracted from: .*?\\(.*?)\.py', content)
    if metadata_match:
        original_name = metadata_match.group(1)
        return f"Component originally named '{original_name}', providing core logic for its parent repository."

    # Fallback to name-based inference
    parts = filename.replace(".py", "").split("_")
    module = " ".join([p for p in parts if p and not p.startswith('0x')])
    return f"Implements {module} logic, facilitating specialized tasks and enhancing the swarm's multi-domain expertise."

def main():
    if not os.path.exists(CLEANED_DIR):
        print(f"Directory {CLEANED_DIR} not found.")
        return

    files = sorted([f for f in os.listdir(CLEANED_DIR) if f.endswith(".py")])
    total = len(files)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# External Cleaned Candidates Report\n\n")
        f.write(f"Total Files: {total}\n\n")
        f.write("| File | Utility to Swarm |\n")
        f.write("|------|------------------|\n")
        
        for i, filename in enumerate(files):
            filepath = os.path.join(CLEANED_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as src:
                    content = src.read(4000) # Read first 4KB
                
                purpose = get_file_purpose(content, filename)
                # Keep it concise
                purpose = purpose.replace("|", "\\|").replace("\n", " ").strip()
                
                # Check for "useless" files - e.g. nearly empty
                if len(content.strip()) < 100 and "__init__" not in filename:
                    purpose = "**STALE/MINIMAL candidate** - Review for deletion."

                f.write(f"| {filename} | {purpose} |\n")
                
                if (i + 1) % 500 == 0:
                    print(f"Processed {i+1}/{total} files...")
            except Exception as e:
                f.write(f"| {filename} | Error analyzing file: {str(e)} |\n")

    print(f"Report generated at {REPORT_PATH}")

if __name__ == "__main__":
    main()
