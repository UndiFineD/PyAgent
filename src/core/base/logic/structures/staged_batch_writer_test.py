# Auto-synced test for core/base/logic/structures/staged_batch_writer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "staged_batch_writer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "WritePolicy"), "WritePolicy missing"
    assert hasattr(mod, "CoalesceStrategy"), "CoalesceStrategy missing"
    assert hasattr(mod, "StagedWrite"), "StagedWrite missing"
    assert hasattr(mod, "WriteStats"), "WriteStats missing"
    assert hasattr(mod, "StagedBatchWriter"), "StagedBatchWriter missing"
    assert hasattr(mod, "StagedWriteTensor"), "StagedWriteTensor missing"
    assert hasattr(mod, "create_staged_tensor"), "create_staged_tensor missing"
    assert hasattr(mod, "coalesce_write_indices"), "coalesce_write_indices missing"

