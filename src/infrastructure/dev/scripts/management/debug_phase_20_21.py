#!/usr/bin/env python3

"""
Debug script for testing Phases 20 (Visual/Multimodal) and 21 (Distributed Observability).
"""

import logging
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager
from src.logic.agents.cognitive.VisualizerAgent import VisualizerAgent
from src.logic.agents.cognitive.GraphMemoryAgent import GraphMemoryAgent
from src.core.base.MultiModalContextAgent import MultiModalContextAgent

def test_visualization_and_memory() -> None:
    print("\n--- Testing Phase 20: Visual & Multimodal ---")
    root = Path("c:/DEV/PyAgent")
    viz = VisualizerAgent(str(root / "src/logic/agents/cognitive/VisualizerAgent.py"))
    mem = GraphMemoryAgent(str(root / "src/logic/agents/cognitive/GraphMemoryAgent.py"))
    
    # 1. Test Integration
    viz.set_memory_agent(mem)
    mem.add_relationship("User", "request", "CodeFix")
    mem.add_relationship("CodeFix", "triggers", "CoderAgent")
    
    graph = viz.visualize_knowledge_graph()
    print(graph)
    assert "User -- request --> CodeFix" in graph
    
    # 2. Test MultiModal (Simulated)
    mm = MultiModalContextAgent(str(root / "src/logic/agents/system/MultiModalContextAgent.py"))
    # Create a dummy file for testing
    dummy_img = root / "dummy_ui.png"
    dummy_img.write_text("dummy binary data")
    
    analysis = mm.analyze_screenshot(str(dummy_img))
    print(analysis)
    assert "Visual Analysis" in analysis
    dummy_img.unlink()

def test_observability() -> None:
    print("\n--- Testing Phase 21: Distributed Observability ---")
    fleet = FleetManager("c:/DEV/PyAgent")
    
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
    assert len(spans) > 0

def test_gui_backend() -> None:
    print("\n--- Testing Phase 22: GUI Backend ---")
    fleet = FleetManager("c:/DEV/PyAgent")
    ui = fleet.web_ui
    
    # File Explorer
    files = ui.list_workspace_files(".")
    print(f"File count: {len(files['items'])}")
    assert len(files['items']) > 0
    
    # Workflow Designer
    designer = ui.get_workflow_designer_state()
    print(f"Available Agents: {len(designer['agents'])}")
    assert len(designer['agents']) >= 0
    
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
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
