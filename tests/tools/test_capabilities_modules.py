import importlib.util
import sys
from pathlib import Path

MODULES = [
    "tools.git_utils",
    "tools.remote",
    "tools.ssl_utils",
    "tools.netcalc",
    "tools.nettest",
    "tools.nginx",
    "tools.proxy_test",
    "tools.port_forward",
    "tools.knock",
    "tools.boot",
    "tools.self_heal",
]


def test_modules_importable(tmp_path: Path) -> None:
    # ensure project structure exists for import path
    from scripts.setup_structure import create_core_structure

    create_core_structure(str(tmp_path))
    sys.path.insert(0, str(tmp_path / "src"))

    for name in MODULES:
        spec = importlib.util.find_spec(name)
        assert spec is not None, f"cannot find {name}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
        if name.endswith("self_heal"):
            assert hasattr(module, "detect_misconfig"), "self_heal missing detect_misconfig"
            assert callable(getattr(module, "detect_misconfig"))
        else:
            assert hasattr(module, "main"), f"{name} missing main()"
            assert callable(getattr(module, "main"))
