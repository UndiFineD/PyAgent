import os
from typing import Dict, List, Any, Tuple, Optional

class OrchestratorRegistryCore:
    """
    Pure logic core for Orchestrator Registry.
    Handles dynamic discovery of orchestrator classes.
    """
    
    def __init__(self, current_sdk_version: str) -> None:
        self.sdk_version: str = current_sdk_version

    def process_discovered_files(self, file_paths: List[str]) -> Dict[str, Tuple[str, str, bool, Optional[str]]]:
        """
        Processes a list of file paths and extracts orchestrator configurations.
        Expects relative paths from workspace root.
        """
        discovered: Dict[str, Tuple[str, str, bool, Optional[str]]] = {}
        
        for rel_path in file_paths:
            file = os.path.basename(rel_path)
            if file.endswith(".py") and not file.startswith("__"):
                class_name: str = file[:-3]
                
                if any(x in class_name for x in ["Orchestrator", "Manager", "Selector", "Engine", "Spawner", "Bridge"]):
                     # Calculate module path
                    module_path: str = rel_path.replace(os.sep, ".").replace(".py", "")
                    
                    # Convert ClassName -> snake_case key
                    # "SelfHealingOrchestrator" -> "self_healing"
                    key: str = self._to_snake_case(class_name.replace("Orchestrator", ""))
                    if not key: key = self._to_snake_case(class_name)

                    # Default heuristic for 'needs_fleet'
                    needs_fleet: bool = any(x in class_name for x in ["Orchestrator", "Spawner", "Bridge", "Selector", "Engine"])
                    
                    # (module, class, needs_fleet, arg_path)
                    discovered[key] = (module_path, class_name, needs_fleet, None)

        return discovered

    def _to_snake_case(self, name: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def parse_manifest(self, raw_manifest: Dict[str, Any]) -> Dict[str, Tuple[str, str, bool, Optional[str]]]:
        """
        Parses the raw manifest dictionary and filters incompatible plugins.
        Returns a dict of {Name: (module, class, needs_fleet, arg_path)}.
        """
        valid_configs: Dict[str, Tuple[str, str, bool, Optional[str]]] = {}
        for key, cfg in raw_manifest.items():
            # Expecting: "Name": ["module.path", "ClassName", needs_fleet, "arg_path", "min_sdk_version"]
            if isinstance(cfg, list) and len(cfg) >= 2:
                # Version gate
                min_sdk: str = cfg[4] if len(cfg) > 4 else "1.0.0"
                
                if self.is_compatible(min_sdk):
                    needs_fleet: bool = cfg[2] if len(cfg) > 2 else False
                    arg_path: Optional[str] = cfg[3] if len(cfg) > 3 else None
                    valid_configs[key] = (cfg[0], cfg[1], needs_fleet, arg_path)
                
        return valid_configs

    def is_compatible(self, required_version: str) -> bool:
        """
        Checks if the current SDK version meets the required version.
        """
        try:
            p_parts = [int(x) for x in self.sdk_version.split('.')]
            r_parts = [int(x) for x in required_version.split('.')]
            
            # Pad to length 3
            p_parts += [0] * (3 - len(p_parts))
            r_parts += [0] * (3 - len(r_parts))
            
            if p_parts[0] > r_parts[0]: return True
            if p_parts[0] < r_parts[0]: return False
            return p_parts[1] >= r_parts[1]
        except Exception:
            return True
