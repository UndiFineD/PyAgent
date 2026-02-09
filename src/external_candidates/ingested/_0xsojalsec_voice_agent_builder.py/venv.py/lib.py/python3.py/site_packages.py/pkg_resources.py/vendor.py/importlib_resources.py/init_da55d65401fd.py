# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pkg_resources\_vendor\importlib_resources\__init__.py
"""Read resources contained within a package."""

from ._common import (
    Package,
    as_file,
    files,
)
from ._legacy import (
    Resource,
    contents,
    is_resource,
    open_binary,
    open_text,
    path,
    read_binary,
    read_text,
)
from .abc import ResourceReader

__all__ = [
    "Package",
    "Resource",
    "ResourceReader",
    "as_file",
    "contents",
    "files",
    "is_resource",
    "open_binary",
    "open_text",
    "path",
    "read_binary",
    "read_text",
]
