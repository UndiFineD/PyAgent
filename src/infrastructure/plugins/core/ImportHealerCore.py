
"""
Core logic for Broken Import Self-Healing (Phase 186).
Suggests fixes for ModuleNotFound errors and builds import maps.
"""

import re
import os




class ImportHealerCore:
    """Core logic for diagnosing and fixing import errors."""
    @staticmethod
    def suggest_fix(error_message: str) -> str:
        """
        Parses a ModuleNotFoundError and suggests a pip install command.
        """
        match = re.search(r"No module named ['\"](.*?)['\"]", error_message)
        if match:
            module = match.group(1).split('.')[0]
            return f"Suggested fix: pip install {module}"
        return "Suggested fix: Check sys.path or internal module naming."

    @staticmethod
    def build_internal_import_map(directory: str) -> dict[str, list[str]]:
        """
        Scans directory for internal imports and builds a map.
        """
        import_map = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    rel_path = os.path.relpath(os.path.join(root, file), directory)
                    with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        # Find internal imports (src.xxx)
                        imports = re.findall(r"^from\s+(src\.[a-zA-Z0-9_\.]+)", content, re.MULTILINE)
                        imports += re.findall(r"^import\s+(src\.[a-zA-Z0-9_\.]+)", content, re.MULTILINE)
                        if imports:
                            import_map[rel_path] = list(set(imports))
        return import_map
