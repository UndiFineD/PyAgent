import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.classes.orchestration.DirectorAgent import DirectorAgent
from src.classes.coder.RustAgent import RustAgent
from src.classes.coder.GoAgent import GoAgent
from src.classes.context.KnowledgeAgent import KnowledgeAgent

def test_specialists_exist():
    print("Checking specialist availability...")
    agents = [
        DirectorAgent("test_plan.md"),
        RustAgent("test.rs"),
        GoAgent("test.go"),
        KnowledgeAgent(".")
    ]
    for agent in agents:
        print(f"Verified: {agent.__class__.__name__}")

def test_knowledge_agent_scan():
    print("\nTesting KnowledgeAgent scanning...")
    ka = KnowledgeAgent(Path("."))
    context = ka.scan_workspace("DirectorAgent")
    print(f"KnowledgeAgent found {len(context)} chars of context.")
    assert "DirectorAgent" in context
    print("KnowledgeAgent scan: SUCCESS")

if __name__ == "__main__":
    try:
        test_specialists_exist()
        test_knowledge_agent_scan()
        print("\nAll specialist sanity checks: PASSED")
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
        sys.exit(1)
