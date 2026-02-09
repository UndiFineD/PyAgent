import glob
import os
import shutil

def purge_videos_py():
    patterns = [
        "c:/Dev/PyAgent/src/external_candidates/cleaned/*videos_py*",
        "c:/Dev/PyAgent/tests/unit/test_auto_*videos_py*",
        "c:/Dev/PyAgent/tests/unit/__pycache__/test_auto_*videos_py*"
    ]
    
    deleted_count = 0
    for pattern in patterns:
        files = glob.glob(pattern)
        for f in files:
            try:
                if os.path.isfile(f):
                    os.remove(f)
                    print(f"Deleted file: {f}")
                    deleted_count += 1
                elif os.path.isdir(f):
                    shutil.rmtree(f)
                    print(f"Deleted directory: {f}")
                    deleted_count += 1
            except Exception as e:
                print(f"Error deleting {f}: {e}")
    
    print(f"Total items deleted: {deleted_count}")

if __name__ == "__main__":
    purge_videos_py()
