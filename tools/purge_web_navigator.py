#!/usr/bin/env python3
import os
import glob
import shutil

def purge_web_navigator():
    patterns = [
        "src/external_candidates/cleaned/*web_navigator*",
        "tests/unit/*web_navigator*",
        "tests/unit/__pycache__/*web_navigator*"
    ]
    
    count = 0
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"Deleted File: {path}")
                    count += 1
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Deleted Directory: {path}")
                    count += 1
            except Exception as e:
                print(f"Error deleting {path}: {e}")
    
    print(f"\nPurge complete. Total items deleted: {count}")

if __name__ == "__main__":
    purge_web_navigator()
