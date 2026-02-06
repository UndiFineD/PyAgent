# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render\renderers\lab.py
# renderers/lab.py
"""
Lab renderer
"""

from typing import Callable, Dict, Optional, Tuple

from PIL import Image


def render(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
    """Render heat exchanger"""

    return image_resolver(f"{entity['name']}_0")


def render_shadow(
    entity: Dict, grid, image_resolver: Callable
) -> Optional[Image.Image]:
    """Render shadow"""

    return image_resolver(f"{entity['name']}_2_shadow", True)


def get_key(entity: Dict, grid) -> str:
    """Get cache key"""
    return str(entity.get("direction", 0))


def get_size(entity: Dict) -> Tuple[float, float]:
    """Get heat exchanger size based on direction"""
    return (3, 3)
