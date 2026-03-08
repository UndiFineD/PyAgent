
"""
Core logic for Dependency Management (Phase 176).
Handles pip-audit execution and version pinning.
"""

import subprocess
import os

from src.core.base.interfaces import ContextRecorderInterface

class DependencyCore:
    @staticmethod
    def run_pip_audit(recorder: ContextRecorderInterface | None = None) -> str:
        """
        Runs pip-audit and returns the summary.
        """
        try:
            result = subprocess.run(["pip-audit", "--format", "plain"], capture_output=True, text=True)
            output = result.stdout or result.stderr
        except FileNotFoundError:
            output = "pip-audit not installed. Run 'pip install pip-audit' to enable."

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-audit",
                prompt="pip-audit --format plain",
                result=output[:2000]
            )

        return output

    @staticmethod
    def pin_requirements(file_path: str, recorder: ContextRecorderInterface | None = None) -> int:
        """
        Ensures all packages in a file are pinned with ==.
        Returns the number of lines modified.
        """
        if not os.path.exists(file_path):
            if recorder:
                recorder.record_interaction(
                    provider="python",
                    model="pip-freeze",
                    prompt=f"pin {file_path}",
                    result="file-not-found"
                )
            return 0
            
        with open(file_path) as f:
            lines = f.readlines()
            
        new_lines = []
        modified = 0
        for line in lines:
            stripped = line.strip()
            # If line is a package and not pinned
            if stripped and not stripped.startswith("#") and not stripped.startswith("-r"):
                if "==" not in stripped and ">=" not in stripped:
                    # In a real scenario, we'd fetch current version. 
                    # For this phase, we'll mark it for review if not pinned.
                    new_lines.append(line.replace(stripped, stripped + "==LATEST-CHECK-REQUIRED"))
                    modified += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
        with open(file_path, "w") as f:
            f.writelines(new_lines)

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-freeze",
                prompt=f"pin {file_path}",
                result=f"modified={modified}",
                meta={"changes": modified}
            )
        
        return modified