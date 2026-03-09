from pathlib import Path


def test_common_helpers_importable(tmp_path: Path):
    # structure must exist for import path
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))
    import importlib.util, sys
    sys.path.insert(0, str(tmp_path / "src"))
    spec = importlib.util.find_spec("tools.common")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    assert hasattr(module, "load_config")
    assert callable(module.load_config)
