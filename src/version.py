"""
PyAgent SDK Version Info and Stability Gates.
"""

# PyAgent SDK Version Info (Core/Fleet Version)
VERSION = "2.1.5-stable"
SDK_VERSION = "3.1.0"
EVOLUTION_PHASE = 116
STABILITY_SCORE = 1.0  # Phase 108: Multi-Agent Logic Harvesting and Rust-Readiness verified
COMPATIBLE_CORE_VERSIONS = ["3.0.0", "2.2.0", "2.1.0", "2.0.0"]

def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase
