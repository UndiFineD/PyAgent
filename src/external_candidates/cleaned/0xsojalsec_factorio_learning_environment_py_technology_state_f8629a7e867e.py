# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\commons.py\models.py\technology_state_f8629a7e867e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\commons\models\technology_state.py

from dataclasses import dataclass

from typing import Dict, List


@dataclass
class TechnologyState:
    """Represents the state of a technology"""

    name: str

    researched: bool

    enabled: bool

    level: int

    research_unit_count: int

    research_unit_energy: float

    prerequisites: List[str]

    ingredients: List[Dict[str, int]]
