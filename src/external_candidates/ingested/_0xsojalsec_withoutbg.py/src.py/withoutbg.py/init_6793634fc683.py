# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\src\withoutbg\__init__.py
"""withoutbg: AI-powered background removal with local and cloud options."""

from .__version__ import __version__
from .api import StudioAPI
from .core import remove_background, remove_background_batch
from .exceptions import APIError, ModelNotFoundError, WithoutBGError
from .models import SnapModel

__all__ = [
    "remove_background",
    "remove_background_batch",
    "SnapModel",
    "StudioAPI",
    "WithoutBGError",
    "ModelNotFoundError",
    "APIError",
    "__version__",
]
