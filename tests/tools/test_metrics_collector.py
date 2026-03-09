from pathlib import Path

def test_metrics_collector_api(tmp_path: Path) -> None:
    # prepare structure
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))

    import importlib.util, sys
    sys.path.insert(0, str(tmp_path / "src"))
    spec = importlib.util.find_spec("tools.metrics")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    assert hasattr(module, "collect_metrics")
    assert callable(module.collect_metrics)
