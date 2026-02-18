#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import os
except ImportError:
    import os

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .mixins.complexity_analysis_mixin import ComplexityAnalysisMixin
except ImportError:
    from .mixins.complexity_analysis_mixin import ComplexityAnalysisMixin

try:
    from .mixins.profiling_analysis_mixin import ProfilingAnalysisMixin
except ImportError:
    from .mixins.profiling_analysis_mixin import ProfilingAnalysisMixin

try:
    from .mixins.research_analysis_mixin import ResearchAnalysisMixin
except ImportError:
    from .mixins.research_analysis_mixin import ResearchAnalysisMixin

try:
    from .mixins.structural_analysis_mixin import StructuralAnalysisMixin
except ImportError:
    from .mixins.structural_analysis_mixin import StructuralAnalysisMixin




class SelfImprovementAnalysis(
    StructuralAnalysisMixin,
    ResearchAnalysisMixin,
    ComplexityAnalysisMixin,
    ProfilingAnalysisMixin
):
    """Specialized assistant for scanning and analyzing tech debt and fleet metrics.
    def __init__(self, workspace_root: str):
        """Initializes the SelfImprovementAnalysis assistant.        self.workspace_root = workspace_root
        self.research_doc = os.path.join(workspace_root, "docs", "IMPROVEMENT_RESEARCH.md")"        self.profiling_agent: Any = None  # Set by orchestrator

    # Logic delegated to mixins
