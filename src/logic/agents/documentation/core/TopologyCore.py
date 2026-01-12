"""
Core logic for Swarm Topology Generation (Phase 169).
This module is designed to be side-effect free and a candidate for Rust acceleration.
"""

from typing import Dict, List, Optional

class TopologyCore:
    @staticmethod
    def generate_mermaid_graph(nodes: List[str], edges: List[Dict[str, str]], direction: str = "TD") -> str:
        """
        Generates a Mermaid.js flowchart string.
        :param nodes: List of node names.
        :param edges: List of dicts with 'from', 'to', and optional 'label'.
        :param direction: Mermaid direction (TD, LR, etc.)
        :return: A mermaid formatted string.
        """
        lines = [f"graph {direction}"]
        
        # Add nodes with basic styling based on type
        for node in nodes:
            safe_id = node.replace(".", "_").replace("/", "_").replace("\\", "_")
            if "Agent" in node:
                lines.append(f"    {safe_id}([{node}])")
            elif "Core" in node:
                lines.append(f"    {safe_id}{{{{{node}}}}}")
            else:
                lines.append(f"    {safe_id}[{node}]")
                
        # Add edges
        for edge in edges:
            u = edge['from'].replace(".", "_").replace("/", "_").replace("\\", "_")
            v = edge['to'].replace(".", "_").replace("/", "_").replace("\\", "_")
            label = edge.get('label', '')
            if label:
                lines.append(f"    {u} -->|{label}| {v}")
            else:
                lines.append(f"    {u} --> {v}")
                
        return "\n".join(lines)

    @staticmethod
    def filter_active_relationships(all_deps: Dict[str, List[str]], focus_list: List[str]) -> Dict[str, List[str]]:
        """
        Filters a dependency map to only include nodes relevant to the focus list.
        """
        filtered = {}
        for source, targets in all_deps.items():
            if any(f in source for f in focus_list):
                filtered[source] = [t for t in targets if any(f in t for f in focus_list) or "Core" in t]
        return filtered
