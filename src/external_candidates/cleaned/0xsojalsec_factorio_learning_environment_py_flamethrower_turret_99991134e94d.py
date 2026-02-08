# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\render.py\renderers.py\flamethrower_turret_99991134e94d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render\renderers\flamethrower_turret.py

# renderers/flamethrower_turret.py

"""

Flamethrower turret renderer

"""

from typing import Callable, Dict, Optional, Tuple

from PIL import Image

DIRECTIONS = {0: "north", 2: "east", 4: "south", 6: "west"}


def render(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Render flamethrower turret"""

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
    """Get flamethrower turret size based on direction"""

    direction = entity.get("direction", 0)

    if direction in [2, 6]:  # East/West
        return (3, 2)

    else:  # North/South
        return (2, 3)
