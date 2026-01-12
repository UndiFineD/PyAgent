"""
Core logic for Swarm Convergence (Phase 170).
Handles file system cleanup and version management.
"""

import os
import shutil
import re

class ConvergenceCore:
    @staticmethod
    def clean_sweep(root_dir: str) -> dict:
        """
        Removes __pycache__ and temporary files.
        """
        stats = {"pycache_removed": 0, "tmp_removed": 0}
        
        for root, dirs, files in os.walk(root_dir):
            # Remove __pycache__
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
                stats["pycache_removed"] += 1
                dirs.remove("__pycache__")
                
            # Remove .tmp files
            for file in files:
                if file.endswith(".tmp") or file.endswith(".temp"):
                    os.remove(os.path.join(root, file))
                    stats["tmp_removed"] += 1
                    
        return stats

    @staticmethod
    def update_version_file(file_path: str, new_version: str) -> bool:
        """
        Updates the version string in version.py.
        """
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Regex to find VERSION = "..."
        new_content = re.sub(r'VERSION\s*=\s*["\'].*?["\']', f'VERSION = "{new_version}"', content)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return True
