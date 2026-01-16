import sys
from pathlib import Path

# Add src to path

from src.infrastructure.orchestration.DirectorAgent import DirectorAgent
from src.logic.agents.development.RustAgent import RustAgent
from src.logic.agents.development.GoAgent import GoAgent
from src.logic.agents.cognitive.KnowledgeAgent import KnowledgeAgent


def test_specialists_exist() -> None:
    print("Checking specialist availability...")
    agents = [
        DirectorAgent("test_plan.md"),
        RustAgent("test.rs"),
        GoAgent("test.go"),
        KnowledgeAgent("."),
    ]
    for agent in agents:
        print(f"Verified: {agent.__class__.__name__}")


def test_knowledge_agent_scan() -> None:
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
