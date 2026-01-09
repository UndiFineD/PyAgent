# PyAgent Versioning Gatekeeper
# This file serves as the source of truth for the project's current maturity level.

VERSION = "2.1.0-stable"
EVOLUTION_PHASE = 108
STABILITY_SCORE = 0.99  # Phase 108: Integrated FTS5, Sharded Intelligence, and Rust Readiness complete

def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase

def get_version_info():
    """Returns detailed version and phase information for orchestrators."""
    return {
        "version": VERSION,
        "phase": EVOLUTION_PHASE,
        "stability": STABILITY_SCORE,
        "rust_readiness": "Protocol typing > 80%, LogicCore isolation complete"
    }
