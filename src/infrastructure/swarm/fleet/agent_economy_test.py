# Auto-synced test for infrastructure/swarm/fleet/agent_economy.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_economy.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MarketPricingEngine"), "MarketPricingEngine missing"
    assert hasattr(mod, "AgentEconomy"), "AgentEconomy missing"
    assert hasattr(mod, "AuctionOrchestrator"), "AuctionOrchestrator missing"

