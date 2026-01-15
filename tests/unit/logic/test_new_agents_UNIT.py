"""Unit tests for the new agent infrastructure."""
from typing import Any, Dict
from src.logic.agents.system.ModelOptimizerAgent import ModelOptimizerAgent
from src.logic.agents.cognitive.LatentReasoningAgent import LatentReasoningAgent


def test_hopper_optimization() -> None:
    agent = ModelOptimizerAgent("dummy_path")


    # Test strategy selection for H100
    strategy: Dict[str, Any] = agent.select_optimization_strategy(70, 80, hardware_features=["h100"])
    assert strategy["hopper_optimized"] is True
    assert strategy["quantization"] == "FP8"

    # Test simulation
    sim: Dict[str, Any] = agent.simulate_hopper_load(70)
    assert sim["hardware"] == "NVIDIA H100 (Hopper)"
    assert sim["simulated_throughput_tokens_s"] > 0

def test_latent_reasoning_guardrails() -> None:
    agent = LatentReasoningAgent("dummy_path")
    # Test high-resource language
    audit_eng = agent.audit_multilingual_output("Sort this list", "[1, 2, 3]", "English")
    assert audit_eng["is_consistent"] is True

    # Test low-resource language with complex task
    complex_task = "Identify the morphological differences between Swahili and Telugu in the context of neural syntax pruning."
    audit_swa = agent.audit_multilingual_output(complex_task, "...", "Swahili")
    assert audit_swa["is_consistent"] is False
    assert "English-centered reasoning drift" in audit_swa["detected_bias"]
