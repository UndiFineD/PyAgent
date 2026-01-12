"""
Core logic for Swarm Rebirth (Phase 180).
Handles mass directory scaffolding and cleanup.
"""

import os
import shutil
import yaml
from typing import List, Dict

class RebirthCore:
    @staticmethod
    def scaffold_structure(root_dir: str, structure: Dict[str, Any]) -> int:
        """
        Recursively creates a directory structure from a dictionary.
        Returns the number of directories created.
        """
        count = 0
        for name, sub in structure.items():
            path = os.path.join(root_dir, name)
            if isinstance(sub, dict):
                os.makedirs(path, exist_ok=True)
                count += 1
                count += RebirthCore.scaffold_structure(path, sub)
            elif isinstance(sub, list):
                os.makedirs(path, exist_ok=True)
                count += 1
                for item in sub:
                    # Create empty files for list items
                    open(os.path.join(path, item), 'a').close()
        return count

    @staticmethod
    def purge_pycache(root_dir: str):
        """
        Forcefully removes all __pycache__ folders.
        """
        for root, dirs, _ in os.walk(root_dir):
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
                dirs.remove("__pycache__")

    @staticmethod
    def parse_manifest(manifest_path: str) -> Dict[str, Any]:
        """
        Parses the rebirth manifest.yaml.
        """
        if not os.path.exists(manifest_path):
            return {}
        with open(manifest_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
