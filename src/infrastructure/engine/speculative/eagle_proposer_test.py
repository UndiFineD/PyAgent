# Auto-synced test for infrastructure/engine/speculative/eagle_proposer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "eagle_proposer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EagleConfig"), "EagleConfig missing"
    assert hasattr(mod, "EagleMethod"), "EagleMethod missing"
    assert hasattr(mod, "AttentionBackend"), "AttentionBackend missing"
    assert hasattr(mod, "DraftOutput"), "DraftOutput missing"
    assert hasattr(mod, "DraftModelWrapper"), "DraftModelWrapper missing"
    assert hasattr(mod, "SimpleDraftModel"), "SimpleDraftModel missing"
    assert hasattr(mod, "TreeNode"), "TreeNode missing"
    assert hasattr(mod, "SpeculativeTree"), "SpeculativeTree missing"
    assert hasattr(mod, "TreeAttentionMetadata"), "TreeAttentionMetadata missing"
    assert hasattr(mod, "AcceptanceStats"), "AcceptanceStats missing"
    assert hasattr(mod, "AttentionMetadata"), "AttentionMetadata missing"
    assert hasattr(mod, "InputBuffer"), "InputBuffer missing"
    assert hasattr(mod, "CpuGpuBuffer"), "CpuGpuBuffer missing"
    assert hasattr(mod, "EagleProposer"), "EagleProposer missing"
    assert hasattr(mod, "EagleProposerFactory"), "EagleProposerFactory missing"
    assert hasattr(mod, "AsyncEagleProposer"), "AsyncEagleProposer missing"

