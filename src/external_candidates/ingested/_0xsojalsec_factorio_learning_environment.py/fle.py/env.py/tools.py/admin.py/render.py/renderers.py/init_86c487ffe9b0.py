# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render\renderers\__init__.py
# renderers/__init__.py
"""
Base renderer functionality for entity rendering
"""

from typing import Callable, Dict, Optional, Tuple

from PIL import Image


class BaseRenderer:
    """Base class for entity renderers"""

    @staticmethod
    def render(entity: Dict, grid, image_resolver: Callable) -> Optional[Image.Image]:
        """Render entity"""
        raise NotImplementedError

    @staticmethod
    def render_shadow(
        entity: Dict, grid, image_resolver: Callable
    ) -> Optional[Image.Image]:
        """Render entity shadow"""
        return None

    @staticmethod
    def get_key(entity: Dict, grid) -> str:
        """Get cache key for entity state"""
        return str(entity.get("direction", 0))

    @staticmethod
    def get_size(entity: Dict) -> Tuple[float, float]:
        """Get entity size in tiles"""
        return (1, 1)
