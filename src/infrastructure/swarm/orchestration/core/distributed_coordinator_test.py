# Auto-synced test for infrastructure/swarm/orchestration/core/distributed_coordinator.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "distributed_coordinator.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BaseWorker"), "BaseWorker missing"
    assert hasattr(mod, "ControlMessage"), "ControlMessage missing"
    assert hasattr(mod, "CoordinatorMessage"), "CoordinatorMessage missing"
    assert hasattr(mod, "DPCoordinator"), "DPCoordinator missing"
    assert hasattr(mod, "DistributedExecutor"), "DistributedExecutor missing"
    assert hasattr(mod, "DistributedSyncProvider"), "DistributedSyncProvider missing"
    assert hasattr(mod, "EngineIdentity"), "EngineIdentity missing"
    assert hasattr(mod, "EngineState"), "EngineState missing"
    assert hasattr(mod, "LoadBalancingStrategy"), "LoadBalancingStrategy missing"
    assert hasattr(mod, "MPClient"), "MPClient missing"
    assert hasattr(mod, "MetricsMessage"), "MetricsMessage missing"
    assert hasattr(mod, "MultiProcessExecutor"), "MultiProcessExecutor missing"
    assert hasattr(mod, "NixlSyncProvider"), "NixlSyncProvider missing"
    assert hasattr(mod, "ParallelConfig"), "ParallelConfig missing"
    assert hasattr(mod, "RequestMessage"), "RequestMessage missing"
    assert hasattr(mod, "ResponseMessage"), "ResponseMessage missing"
    assert hasattr(mod, "TCPSyncProvider"), "TCPSyncProvider missing"
    assert hasattr(mod, "WorkerIdentity"), "WorkerIdentity missing"
    assert hasattr(mod, "WorkerProcess"), "WorkerProcess missing"
    assert hasattr(mod, "WorkerState"), "WorkerState missing"
    assert hasattr(mod, "create_distributed_executor"), "create_distributed_executor missing"
    assert hasattr(mod, "get_dp_rank"), "get_dp_rank missing"
    assert hasattr(mod, "get_dp_size"), "get_dp_size missing"
    assert hasattr(mod, "get_tp_rank"), "get_tp_rank missing"
    assert hasattr(mod, "get_tp_size"), "get_tp_size missing"

