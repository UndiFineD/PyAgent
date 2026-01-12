"""
Full Reset / Rebirth Script (Phase 180).
Re-scaffolds the entire swarm structure from a manifest.
"""

import os
import sys
import time
from src.infrastructure.dev.core.RebirthCore import RebirthCore

def full_reset():
    root = os.getcwd()
    manifest_path = os.path.join(root, "config/rebirth_manifest.yaml")
    
    print("!!! WARNING: FULL RESET INITIATED !!!")
    print("This will re-scaffold the swarm directory structure.")
    time.sleep(2) # Safety delay
    
    core = RebirthCore()
    
    # 1. Parse manifest
    if not os.path.exists(manifest_path):
        # Create a default manifest if missing
        print("[REBIRTH] Creating default manifest...")
        default_manifest = {
            "src": {
                "core": ["__init__.py", "base.py"],
                "infrastructure": ["__init__.py"],
                "logic": {"agents": {}}
            },
            "data": ["readme.txt"],
            "docs": ["INSTALL.md"]
        }
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        import yaml
        with open(manifest_path, "w") as f:
            yaml.dump(default_manifest, f)
            
    manifest = core.parse_manifest(manifest_path)
    
    # 2. Re-scaffold
    start_time = time.time()
    dirs_created = core.scaffold_structure(root, manifest)
    end_time = time.time()
    
    print(f"[REBIRTH] Success. Created {dirs_created} directories/files in {end_time - start_time:.2f}s")
    print("[REBIRTH] Swarm structure is now consistent with manifest.")

if __name__ == "__main__":
    full_reset()
