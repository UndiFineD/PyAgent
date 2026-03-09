from context_manager import ContextManager
from skills_registry import SkillsRegistry
from cort import ChainOfThought


def test_context_and_skills(tmp_path):
    cm = ContextManager(max_tokens=5)
    assert hasattr(cm, "push")
    registry = SkillsRegistry(tmp_path / "skills")
    assert isinstance(registry.list_skills(), list)
    cort = ChainOfThought(cm)
    root = cort.new_node("start")
    child = root.fork("x")
    child.add("y")
    assert "y" in cm.snapshot()
