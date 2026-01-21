# Add workspace root to sys.path

import json
import sys
from pathlib import Path
from src.infrastructure.swarm.orchestration.signals.signal_registry import SignalRegistry

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


def generate_swarm_graph(output_format: str = "mermaid") -> str:
    """
    Phase 247: Traces message flows in SignalRegistry to build an interaction matrix
    and exports a visualization.
    """
    signals = SignalRegistry()
    history = signals.get_history(limit=500)

    # Trace message flows: sender -> signal_name -> subscribers
    # Note: We need to see who is subscribed to what to form the edges.

    nodes: set[str] = set()
    edges: list[tuple[str, str, str]] = []  # (sender, receiver, label)

    # 1. Map subscribers back to agents
    sub_map = {}  # signal_name -> list of subscriber names (inferred)
    for sig_name, callbacks in signals.subscribers.items():
        sub_names = []
        for cb in callbacks:
            # Try to get the class name from the callback
            name = getattr(cb, "__qualname__", str(cb))
            if "." in name:
                name = name.split(".")[0]
            sub_names.append(name)
        sub_map[sig_name] = sub_names

    # 2. Build the graph from history
    for event in history:
        sender = event.get("sender", "unknown")
        sig_name = event.get("event", "unknown")
        data = event.get("data", {})

        # In capability registration, the data contains the agent name
        if sig_name == "agent_capability_registration":
            actual_agent = data.get("agent", sender)
            nodes.add(actual_agent)
            continue

        nodes.add(sender)

        # Look for subscribers
        for receiver in sub_map.get(sig_name, []):
            nodes.add(receiver)
            edges.append((sender, receiver, sig_name))

    if output_format == "mermaid":
        lines = ["graph TD"]
        # Add nodes
        for node in nodes:
            lines.append(f"    {node}")

        # Add edges (deduplicated)
        unique_edges = set()

        for src, dst, label in edges:
            if src != dst:
                unique_edges.add(f'    {src} -- "{label}" --> {dst}')

        lines.extend(list(unique_edges))

        return "\n".join(lines)

    elif output_format == "json":
        return json.dumps(
            {
                "nodes": list(nodes),
                "edges": [
                    {"from": src, "to": dst, "label": label}
                    for src, dst, label in set(edges)
                ],
            },
            indent=2,
        )

    return ""


def main() -> None:
    print("=== SWARM INTERACTION GRAPH GENERATOR ===")
    mermaid_str = generate_swarm_graph(output_format="mermaid")

    output_path = Path("docs/SWARM_GRAPH.md")
    with open(output_path, "w") as f:
        f.write("# Swarm Social Topology\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_str)
        f.write("\n```\n")

    print(f"Graph generated and saved to {output_path}")


if __name__ == "__main__":
    main()
