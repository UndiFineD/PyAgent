def test_context_components_exist(tmp_path):
    from context_manager import ContextManager
    from skills_registry import SkillsRegistry

    cm = ContextManager(max_tokens=5)
    assert hasattr(cm, "push")
    registry = SkillsRegistry(tmp_path / "skills")
    assert isinstance(registry.list_skills(), list)
