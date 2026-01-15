
"""
Core logic for Resource Curation (Phase 173).
Handles pruning of temporary directories and old files.
"""

import os
import shutil
import time




class CurationCore:
    """Core logic for pruning and managing filesystem resources."""
    @staticmethod
    def prune_directory(directory: str, max_age_days: int = 7) -> int:
        """
        Removes files in a directory that are older than max_age_days.
        Returns the number of files removed.
        """
        if not os.path.exists(directory):
            return 0

        try:
            import rust_core
            return rust_core.prune_directory_rust(directory, max_age_days)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        count = 0
        now = time.time()
        max_age_seconds = max_age_days * 86400

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if now - os.path.getmtime(file_path) > max_age_seconds:
                        os.remove(file_path)
                        count += 1
                except OSError:
                    continue

        return count

    @staticmethod
    def deep_clean_pycache(root_dir: str) -> int:
        """
        Forcefully removes all __pycache__ folders.
        """
        if not os.path.exists(root_dir):
            return 0

        try:
            import rust_core
            return rust_core.deep_clean_pycache_rust(root_dir)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        count = 0
        for root, dirs, files in os.walk(root_dir):
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
                count += 1
                dirs.remove("__pycache__")
        return count
