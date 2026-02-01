
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

# Ensure project root is in path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
from src.infrastructure.swarm.orchestration.intel.self_improvement_orchestrator import SelfImprovementOrchestrator

def test_static_profiling():
    print("[Test] Initializing Fleet and Orchestrator...")
    fleet = FleetManager(os.getcwd())
    orchestrator = SelfImprovementOrchestrator(fleet)
    # Ensure profiling agent is injected
    from src.logic.agents.analysis.profiling_agent import ProfilingAgent
    orchestrator.analysis.profiling_agent = ProfilingAgent()
    
    # Create a complex file to test
    test_file = "scratch/complex_logic.py"
    os.makedirs("scratch", exist_ok=True)
    with open(test_file, "w") as f:
        f.write("\"\"\"Complex logic test.\"\"\"\n\n")
        # Add 200 lines to bypass the heuristic check
        for i in range(210):
            f.write(f"# Line {i} padding\n")
        f.write("def deep_loops():\n")
        for i in range(10):
            f.write("    " * (i + 1) + f"for i{i} in range(10):\n")
        f.write("    " * 11 + "pass\n")

    print(f"[Test] Analyzing {test_file}...")
    findings = orchestrator._analyze_and_fix(test_file)
    
    print("\n[Test] Findings:")
    for f in findings:
        print(f" - [{f.get('type')}] {f.get('message')} at Line {f.get('line')}")

    # Verify intelligence synthesis
    print("\n[Test] Running Intelligence Synthesis...")
    # Add an insight manually to ensure we have something to synthesize if loop count is low
    fleet.intelligence.contribute_insight("ProfilingAgent", f"File: {test_file} | Line: 1 | Description: High complexity detected in deep_loops", 0.99)
    
    patterns = fleet.intelligence.synthesize_collective_intelligence()
    print(f"\n[Test] Patterns Identified: {len(patterns)}")
    for p in patterns:
        print(f" - {p}")

if __name__ == "__main__":
    test_static_profiling()
