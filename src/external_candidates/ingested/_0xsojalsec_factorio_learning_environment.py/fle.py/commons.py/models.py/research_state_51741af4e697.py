# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\commons\models\research_state.py
from dataclasses import dataclass
from typing import Dict, List, Optional

from fle.commons.models.technology_state import TechnologyState


@dataclass
class ResearchState:
    """Complete research state including all technologies and current research"""

    technologies: Dict[str, TechnologyState]
    current_research: Optional[str]
    research_progress: float
    research_queue: List[str]
    progress: Dict
