# Auto-synced test for logic/agents/specialists/web_search_essay_agent.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "web_search_essay_agent.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EssayStyle"), "EssayStyle missing"
    assert hasattr(mod, "EssayLength"), "EssayLength missing"
    assert hasattr(mod, "Source"), "Source missing"
    assert hasattr(mod, "EssayOutline"), "EssayOutline missing"
    assert hasattr(mod, "WebSearchEssayAgent"), "WebSearchEssayAgent missing"

