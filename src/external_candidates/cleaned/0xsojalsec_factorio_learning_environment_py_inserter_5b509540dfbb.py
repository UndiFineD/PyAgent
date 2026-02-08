# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\render.py\renderers.py\inserter_5b509540dfbb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render\renderers\inserter.py

# renderers/inserter.py

"""

Inserter renderer

"""

from typing import Callable, Dict, Optional, Tuple, Union

from PIL import Image

from ..constants import DIRECTIONS


def render(entity: Union[Dict], grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Render inserter"""

    direction = entity.get("direction", 0)

    if not isinstance(direction, int):
        direction = direction.value

    return image_resolver(f"{entity['name']}_{DIRECTIONS[direction]}")


def render_shadow(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Inserters have no shadows"""

    return None


def get_key(entity: Dict, grid) -> str:
    """Get cache key"""

    return str(entity.get("direction", 0))


def get_size(entity: Dict) -> Tuple[float, float]:
    """Inserter is 1x1"""

    return (1, 1)
