# PyAgent Versioning Gatekeeper
# This file serves as the source of truth for the project's current maturity level.

VERSION = "2.1.8-stable"
EVOLUTION_PHASE = 119
STABILITY_SCORE = 1.0  # Phase 108: Multi-Agent Logic Harvesting and Rust-Readiness verified

def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase

from typing import Dict, Any

def get_version_info() -> Dict[str, Any]:
    """Returns detailed version and phase information for orchestrators."""
    return {
        "version": VERSION,
        "phase": EVOLUTION_PHASE,
        "stability": STABILITY_SCORE,
        "rust_readiness": "Protocol typing > 80%, LogicCore isolation complete"
    }
