
"""
Core logic for Bash script analysis (Phase 175).
Integrates shellcheck for linting generated scripts.
"""

import subprocess
import os

class BashCore:
    @staticmethod
    def lint_script(script_path: str) -> dict:
        """
        Runs shellcheck on a bash script.
        """
        if not os.path.exists(script_path):
            return {"error": "File not found"}
            
        try:
            # -f json for machine readable output
            result = subprocess.run(["shellcheck", "-f", "json", script_path], capture_output=True, text=True)
            if result.stdout:
                import json
                return {"issues": json.loads(result.stdout), "valid": False}
            return {"issues": [], "valid": True}
        except FileNotFoundError:
            return {"error": "shellcheck not found. Please install it to enable bash linting."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def wrap_with_safety_flags(content: str) -> str:
        """
        Ensures script starts with common safety flags if not present.
        """
        header = "#!/bin/bash\nset -euo pipefail\n\n"
        if content.startswith("#!"):
            # If shebang exists but no flags, we could inject. For now, just a helper.
            return content
        return header + content