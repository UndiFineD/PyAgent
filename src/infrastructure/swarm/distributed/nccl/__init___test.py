import importlib


def test_import_src_infrastructure_swarm_distributed_nccl___init__():
    mod = importlib.import_module("src.infrastructure.swarm.distributed.nccl.__init__")
    # Basic smoke tests
    assert mod is not None
