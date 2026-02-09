import os
import glob
import shutil
import re

def purge_prefix(prefix):
    print(f"Purging files containing: {prefix}")
    
    # Paths to clean
    targets = [
        "src/external_candidates/cleaned",
        "tests/unit"
    ]
    
    deleted_count = 0
    regex = re.compile(re.escape(prefix), re.IGNORECASE)
    
    for target in targets:
        if not os.path.exists(target):
            continue
        for filename in os.listdir(target):
            if regex.search(filename):
                file_path = os.path.join(target, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    # Also clean up __pycache__
    cache_patterns = [
        "src/external_candidates/cleaned/**/__pycache__",
        "tests/unit/**/__pycache__"
    ]
    for pattern in cache_patterns:
        for cache_dir in glob.glob(pattern, recursive=True):
            try:
                shutil.rmtree(cache_dir)
                print(f"Deleted cache: {cache_dir}")
            except:
                pass

    print(f"Total items deleted: {deleted_count}")

if __name__ == "__main__":
    purge_prefix("graph_r1")
