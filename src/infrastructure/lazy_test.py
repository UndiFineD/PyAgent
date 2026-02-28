# Auto-synced test for infrastructure/lazy.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lazy.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "get_eagle_proposer"), "get_eagle_proposer missing"
    assert hasattr(mod, "get_arc_offload_manager"), "get_arc_offload_manager missing"
    assert hasattr(mod, "get_tool_parser_registry"), "get_tool_parser_registry missing"
    assert hasattr(mod, "get_reasoning_engine"), "get_reasoning_engine missing"
    assert hasattr(mod, "get_paged_attention_engine"), "get_paged_attention_engine missing"
    assert hasattr(mod, "get_mooncake_connector"), "get_mooncake_connector missing"
    assert hasattr(mod, "get_nixl_connector"), "get_nixl_connector missing"
    assert hasattr(mod, "get_prefill_worker"), "get_prefill_worker missing"
    assert hasattr(mod, "get_decode_worker"), "get_decode_worker missing"
    assert hasattr(mod, "get_pp_transfer"), "get_pp_transfer missing"
    assert hasattr(mod, "get_tp_transfer"), "get_tp_transfer missing"

