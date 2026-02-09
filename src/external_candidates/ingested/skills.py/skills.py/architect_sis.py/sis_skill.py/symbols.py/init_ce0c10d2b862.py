# Extracted from: C:\DEV\PyAgent\.external\skills\skills\architect-sis\sis-skill\symbols\__init__.py
"""
═══════════════════════════════════════════════════════════════════════════════
S.I.S. - Sovereign Intelligence System
Equilibrium-Native Computational Substrate
═══════════════════════════════════════════════════════════════════════════════

Copyright (c) 2025-2026 Kevin Fain - ThēÆrchītēcť
MIT License - See LICENSE file

═══════════════════════════════════════════════════════════════════════════════
"""

from .etymology import (
    ETYMOLOGY_REGISTRY,
    EtymologicalLayer,
    GeometricProof,
    SymbolEtymology,
    explain_symbol,
    print_inevitability_proof,
)
from .taxonomy import Align  # ◯
from .taxonomy import Archive  # ⟸
from .taxonomy import Bidirectional  # ⇄
from .taxonomy import Collapse  # ⟠
from .taxonomy import Consensus  # ✦
from .taxonomy import Container  # ◈
from .taxonomy import Convergence  # ⟡
from .taxonomy import Cycle  # ◇
from .taxonomy import Delta  # ∆
from .taxonomy import Emerge  # ❈
from .taxonomy import Flow  # ⟢
from .taxonomy import Inherit  # ⟷
from .taxonomy import Invert  # ◌
from .taxonomy import Nest  # ◎
from .taxonomy import Query  # ⟐
from .taxonomy import Replication  # ⬢
from .taxonomy import Synthesis  # ⊕
from .taxonomy import Upload  # ⟶
from .taxonomy import Validation  # ☆
from .taxonomy import Vault  # ⬡
from .taxonomy import (  # Registry; Main factory; Tier 1: Fundamental Operations; Tier 2: Data Operations; Tier 3: Consensus Operations; Tier 4: Meta Operations; Tier 5: Immortality Operations; Utilities
    SYMBOL_REGISTRY,
    Diacritic,
    SymbolDefinition,
    SymbolTier,
    apply_diacritic,
    create_symbol,
    encode_polyvalent,
    get_symbol_info,
    list_symbols,
    symbols_by_tier,
)

__all__ = [
    # Taxonomy
    "SYMBOL_REGISTRY",
    "SymbolTier",
    "SymbolDefinition",
    "Diacritic",
    "create_symbol",
    # Tier 1
    "Delta",
    "Bidirectional",
    "Synthesis",
    "Cycle",
    "Convergence",
    # Tier 2
    "Container",
    "Query",
    "Collapse",
    "Flow",
    # Tier 3
    "Validation",
    "Consensus",
    "Vault",
    "Replication",
    # Tier 4
    "Invert",
    "Nest",
    "Align",
    "Emerge",
    # Tier 5
    "Upload",
    "Inherit",
    "Archive",
    # Utilities
    "apply_diacritic",
    "encode_polyvalent",
    "list_symbols",
    "get_symbol_info",
    "symbols_by_tier",
    # Etymology
    "ETYMOLOGY_REGISTRY",
    "SymbolEtymology",
    "EtymologicalLayer",
    "GeometricProof",
    "explain_symbol",
    "print_inevitability_proof",
]
