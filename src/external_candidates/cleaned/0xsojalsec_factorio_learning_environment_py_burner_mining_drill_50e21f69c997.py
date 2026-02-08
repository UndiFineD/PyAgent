# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\render.py\renderers.py\burner_mining_drill_50e21f69c997.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render\renderers\burner_mining_drill.py

# renderers/burner_mining_drill.py

"""

Burner mining drill renderer

"""

from typing import Callable, Dict, Optional, Tuple

from PIL import Image

DIRECTIONS = {0: "north", 2: "east", 4: "south", 6: "west"}


def render(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Render burner mining drill"""

    direction = entity.get("direction", 0)

    return image_resolver(f"{entity['name']}_{DIRECTIONS[direction]}")


def render_shadow(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Render shadow"""

    direction = entity.get("direction", 0)

    return image_resolver(f"{entity['name']}_{DIRECTIONS[direction]}", True)


def get_key(entity: Dict, grid) -> str:
    """Get cache key"""

    return str(entity.get("direction", 0))


def get_size(entity: Dict) -> Tuple[float, float]:
    """Burner mining drill is 2x2"""

    return (2, 2)
