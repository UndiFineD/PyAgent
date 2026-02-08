# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\commons.py\models.py\research_state_51741af4e697.py
# NOTE: extracted with static-only rules; review before use

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
