import importlib
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = REPO_ROOT / ".github" / "agents" / "code"
sys.path.insert(0, str(CODE_DIR))
loader_module = importlib.import_module("loader")
load_agent_module = loader_module.load_agent_module
find_agent_class = loader_module.find_agent_class


def test_load_and_find_agent(tmp_path):
    # create a temporary agent module inside the code dir
    module_name = "test_dummy_agent"
    module_path = CODE_DIR / f"{module_name}.py"
    content = """
class TestDummyAgent:
    def execute(self, task=None):
        return {'ok': True}
"""
    module_path.write_text(content, encoding="utf-8")

    try:
        module = load_agent_module(module_name)
        cls = find_agent_class(module)
        inst = cls()
        assert inst.execute() == {"ok": True}
    finally:
        # cleanup
        module_path.unlink()


def test_spec_loader_missing(monkeypatch):
    # Ensure that when spec.loader is None, load_agent_module raises ImportError
    import importlib.util as util

    def fake_spec(name, path):
        return type("Spec", (), {"loader": None})()

    monkeypatch.setattr(util, "spec_from_file_location", fake_spec)

    # Create a temporary module file so load_agent_module proceeds to call spec_from_file_location
    module_name = "nothing_here"
    module_path = CODE_DIR / f"{module_name}.py"
    module_path.write_text("# placeholder", encoding="utf-8")
    try:
        with pytest.raises(ImportError):
            load_agent_module(module_name)
    finally:
        module_path.unlink()
