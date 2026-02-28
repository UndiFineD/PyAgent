# Auto-synced test for infrastructure/storage/kv_transfer/block_table_v2.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "block_table_v2.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BlockAllocationStrategy"), "BlockAllocationStrategy missing"
    assert hasattr(mod, "BlockTableConfig"), "BlockTableConfig missing"
    assert hasattr(mod, "BlockInfo"), "BlockInfo missing"
    assert hasattr(mod, "CpuGpuBuffer"), "CpuGpuBuffer missing"
    assert hasattr(mod, "BlockTable"), "BlockTable missing"
    assert hasattr(mod, "SparseBlockTable"), "SparseBlockTable missing"
    assert hasattr(mod, "PredictiveBlockAllocator"), "PredictiveBlockAllocator missing"
    assert hasattr(mod, "DistributedBlockTable"), "DistributedBlockTable missing"
    assert hasattr(mod, "BlockTableV2"), "BlockTableV2 missing"
    assert hasattr(mod, "BlockTableFactory"), "BlockTableFactory missing"

