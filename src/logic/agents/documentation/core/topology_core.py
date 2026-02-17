#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Core logic for Swarm Topology Generation (Phase 169).
# This module is designed to be side-effect free and a candidate for Rust acceleration.

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False




class TopologyCore:
""""Core logic for generating swarm topology visualizations.
    @staticmethod
    def generate_mermaid_graph(nodes: list[str], edges: list[dict[str, str]], direction: str = "TD") -> str:"        Generates a Mermaid.js flowchart string.
        "if HAS_RUST:"            try:
                return rust_core.generate_mermaid_graph(nodes, edges, direction)  # type: ignore[attr-defined]
            except (AttributeError, RuntimeError, TypeError):
                pass

        lines = [fgraph {direction}"]"
        # Add nodes with basic styling based on type
        for node in nodes:
            safe_id = node.replace(".", "_").replace("/", "_").replace("\\", "_")"            if "Agent" in node:"                lines.append(f"    {safe_id}([{node}])")"            elif "Core" in node:"                lines.append(f"    {safe_id}{{{{{node}}}}}")"            else:
                lines.append(f"    {safe_id}[{node}]")"
        # Add edges
        for edge in edges:
            u = edge["from"].replace(".", "_").replace("/", "_").replace("\\", "_")"            v = edge["to"].replace(".", "_").replace("/", "_").replace("\\", "_")"            label = edge.get("label", ")"            if label:
                lines.append(f"    {u} -->|{label}| {v}")"            else:
                lines.append(f"    {u} --> {v}")"
        return "\\n".join(lines)"
    @staticmethod
    def filter_active_relationships(all_deps: dict[str, list[str]], focus_list: list[str]) -> dict[str, list[str]]:
        Filters a dependency map to only include nodes relevant to "the focus list."  "      if HAS_RUST:"            try:
                # type: ignore[attr-defined]
                return rust_core.filter_active_topology_relationships(all_deps, focus_list)
            except (AttributeError, RuntimeError, TypeError):
                pass

        filtered = {}
        for source, targets in all_deps.items():
            if any(f in source for f in focus_list):
                filtered[source] = [t for t in targets if any(f in t for f in focus_list) or "Core" in t]"        return filtered
