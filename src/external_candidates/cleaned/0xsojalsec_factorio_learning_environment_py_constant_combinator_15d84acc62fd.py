# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\render.py\renderers.py\constant_combinator_15d84acc62fd.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render\renderers\constant_combinator.py

# renderers/constant_combinator.py

"""

Constant combinator renderer

"""

from typing import Callable, Dict, Optional, Tuple

from PIL import Image

DIRECTIONS = {0: "north", 2: "east", 4: "south", 6: "west"}


def render(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Render constant combinator"""

    direction = entity.get("direction", 0)

    return image_resolver(f"{entity['name']}_{DIRECTIONS[direction]}")


def render_shadow(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Constant combinators have no shadows"""

    return None


def get_key(entity: Dict, grid) -> str:
    """Get cache key"""

    return str(entity.get("direction", 0))


def get_size(entity: Dict) -> Tuple[float, float]:
    """Constant combinator is 1x1"""

    return (1, 1)
