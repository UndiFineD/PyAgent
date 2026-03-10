import importlib


def test_runtime_module_exists() -> None:
    runtime = importlib.import_module("src.core.runtime")
    assert hasattr(runtime, "Runtime"), "Runtime class not found"


def test_runtime_has_validate() -> None:
    runtime = importlib.import_module("src.core.runtime")
    assert callable(getattr(runtime, "validate", None)), "validate() missing"
