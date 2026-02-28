# Auto-synced test for inference/execution/async_model_runner.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "async_model_runner.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RunnerState"), "RunnerState missing"
    assert hasattr(mod, "ModelInput"), "ModelInput missing"
    assert hasattr(mod, "ModelOutput"), "ModelOutput missing"
    assert hasattr(mod, "SchedulerOutput"), "SchedulerOutput missing"
    assert hasattr(mod, "AsyncGPUPoolingModelRunnerOutput"), "AsyncGPUPoolingModelRunnerOutput missing"
    assert hasattr(mod, "ExecutionPipeline"), "ExecutionPipeline missing"
    assert hasattr(mod, "AsyncModelRunner"), "AsyncModelRunner missing"
    assert hasattr(mod, "BatchedAsyncRunner"), "BatchedAsyncRunner missing"

