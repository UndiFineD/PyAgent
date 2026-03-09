from pathlib import Path

def test_self_healing_detects(tmp_path: Path) -> None:
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))

    import importlib.util, sys
    sys.path.insert(0, str(tmp_path / "src"))
    spec = importlib.util.find_spec("tools.self_heal")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    assert hasattr(module, "detect_misconfig")
    info = module.detect_misconfig()
    assert isinstance(info, dict)
