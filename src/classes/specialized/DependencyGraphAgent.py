import os
import ast
from pathlib import Path

class DependencyGraphAgent:
    """
    Maps and analyzes dependencies between agent modules and classes.
    Helps in understanding the impact of changes and optimizing imports.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = Path(workspace_path)
        self.dependency_map = {} # module -> set of imports

    def scan_dependencies(self, start_dir="src"):
        """
        Scans a directory for Python files and extracts their imports.
        """
        search_path = self.workspace_path / start_dir
        if not search_path.exists():
            return {"error": f"Path {search_path} does not exist"}

        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    try:
                        rel_path = full_path.relative_to(self.workspace_path)
                        self.dependency_map[str(rel_path)] = self._extract_imports(full_path)
                    except ValueError:
                        continue
        
        return {"modules_scanned": len(self.dependency_map)}

    def _extract_imports(self, file_path):
        imports = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except Exception:
            pass
        return list(imports)

    def get_impact_scope(self, module_name):
        """
        Identifies which modules depend on a given module.
        """
        dependents = []
        for mod, imps in self.dependency_map.items():
            for imp in imps:
                # Basic check for module name in import string
                if module_name in imp or imp.startswith(module_name + "."):
                    dependents.append(mod)
                    break
        return dependents

    def generate_graph_stats(self):
        """Returns complexity metrics for the dependency graph."""
        total_links = sum(len(imps) for imps in self.dependency_map.values())
        return {
            "node_count": len(self.dependency_map),
            "edge_count": total_links,
            "density": total_links / (len(self.dependency_map) ** 2) if len(self.dependency_map) > 0 else 0
        }
