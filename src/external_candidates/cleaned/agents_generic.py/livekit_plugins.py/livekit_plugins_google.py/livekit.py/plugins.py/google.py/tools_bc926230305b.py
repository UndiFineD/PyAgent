# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-google\livekit\plugins\google\tools.py
from typing import Union

from google.genai.types import (
    GoogleMaps,
    GoogleSearch,
    GoogleSearchRetrieval,
    ToolCodeExecution,
    UrlContext,
)

_LLMTool = Union[GoogleSearchRetrieval, ToolCodeExecution, GoogleSearch, UrlContext, GoogleMaps]
