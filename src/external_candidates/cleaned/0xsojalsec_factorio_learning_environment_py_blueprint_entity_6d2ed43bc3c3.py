# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\agents.py\data.py\blueprints_to_policies.py\models.py\blueprint_entity_6d2ed43bc3c3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\agents\data\blueprints_to_policies\models\blueprint_entity.py

from dataclasses import dataclass

from typing import Any, Dict, List, Optional


@dataclass
class BlueprintEntity:
    entity_number: int

    name: str

    position: Dict[str, float]

    direction: int = 0

    items: Dict[str, int] = None

    type: str = None

    neighbours: List[int] = None

    input_priority: str = None

    recipe: Optional[str] = None

    output_priority: str = None

    control_behavior: Dict = None

    connections: Dict = None

    filter: Dict = None

    filters: List[Dict] = None

    filter_mode: Any = None

    use_filters: Any = None

    recipe_quality: Dict = None

    bar: Dict = None
