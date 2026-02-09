import os
import glob
import shutil

patterns = [
    "src/external_candidates/cleaned/*volweb_py*",
    "tests/unit/*volweb_py*",
]

def purge_volweb():
    deleted_count = 0
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"Deleted File: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Deleted Directory: {path}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {path}: {e}")

    # Also clean up __pycache__ in tests/unit that might contain volweb references
    cache_pattern = "tests/unit/__pycache__/*volweb_py*"
    for path in glob.glob(cache_pattern):
        try:
            os.remove(path)
            print(f"Deleted Cache: {path}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting cache {path}: {e}")

    print(f"\nPurge complete. Total items deleted: {deleted_count}")

if __name__ == "__main__":
    purge_volweb()
