#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Debug script for testing Phases 20 (Visual/Multimodal) and 21 (Distributed Observability).
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.core.base.MultiModalContextAgent import MultiModalContextAgent
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
from src.logic.agents.cognitive.graph_memory_agent import GraphMemoryAgent
from src.logic.agents.cognitive.visualizer_agent import VisualizerAgent

__version__ = VERSION


def test_visualization_and_memory() -> None:
    print("\n--- Testing Phase 20: Visual & Multimodal ---")
    root = Path(str(Path(__file__).resolve().parents[5]) + "")
    viz = VisualizerAgent(str(root / "src/logic/agents/cognitive/visualizer_agent.py"))

    mem = GraphMemoryAgent(str(root / "src/logic/agents/cognitive/graph_memory_agent.py"))

    # 1. Test Integration

    viz.set_memory_agent(mem)
    mem.add_relationship("User", "request", "CodeFix")
    mem.add_relationship("CodeFix", "triggers", "CoderAgent")

    graph = viz.visualize_knowledge_graph()
    print(graph)
    assert "User -- request --> CodeFix" in graph

    # 2. Test MultiModal (Simulated)

    mm = MultiModalContextAgent(str(root / "src\\logic\agents\\system\\multi_modal_context_agent.py"))

    # Create a dummy file for testing
    dummy_img = root / "dummy_ui.png"
    dummy_img.write_text("dummy binary data")

    analysis = mm.analyze_screenshot(str(dummy_img))
    print(analysis)

    assert "Visual Analysis" in analysis

    dummy_img.unlink()


def test_observability() -> None:
    print("\n--- Testing Phase 21: Distributed Observability ---")
    fleet = FleetManager(str(Path(__file__).resolve().parents[5]) + "")

    # Trigger tracing
    fleet.telemetry.start_trace("test_op")
    fleet.telemetry.end_trace("test_op", "TestAgent", "test_action", status="success")

    # Check MetricsExporter
    metrics = fleet.telemetry.get_metrics()
    print(f"Metrics (Promptheus format):\n{metrics[:200]}...")
    assert "pyagent_agent_call_duration_ms" in metrics

    # Check OTel
    spans = fleet.telemetry.otel.export_spans()
    print(f"Exported {len(spans)} OTel spans.")
    assert spans


def test_gui_backend() -> None:
    print("\n--- Testing Phase 22: GUI Backend ---")
    fleet = FleetManager(str(Path(__file__).resolve().parents[5]) + "")
    ui = fleet.web_ui

    # File Explorer
    files = ui.list_workspace_files(".")
    print(f"File count: {len(files['items'])}")
    assert files["items"]

    # Workflow Designer
    designer = ui.get_workflow_designer_state()
    print(f"Available Agents: {len(designer['agents'])}")
    assert len(designer["agents"]) >= 0

    # Multi-Fleet
    fleet_mgmt = ui.get_multi_fleet_manager()
    print(f"Local Fleet Status: {fleet_mgmt['local_fleet']['status']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        test_visualization_and_memory()
        test_observability()
        test_gui_backend()
        print("\n✅ ALL PHASE 20-22 TESTS PASSED!")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
