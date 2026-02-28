
"""
Self improvement analysis.py module.
"""
# Copyright 2026 PyAgent Authors
# Logic for analyzing tech debt and structural issues in the fleet.

import os

from .mixins.complexity_analysis_mixin import ComplexityAnalysisMixin
from .mixins.research_analysis_mixin import ResearchAnalysisMixin
from .mixins.structural_analysis_mixin import StructuralAnalysisMixin


class SelfImprovementAnalysis(StructuralAnalysisMixin, ResearchAnalysisMixin, ComplexityAnalysisMixin):
    """Specialized assistant for scanning and analyzing tech debt and fleet metrics."""

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.research_doc = os.path.join(workspace_root, "docs", "IMPROVEMENT_RESEARCH.md")

    # Logic delegated to mixins
