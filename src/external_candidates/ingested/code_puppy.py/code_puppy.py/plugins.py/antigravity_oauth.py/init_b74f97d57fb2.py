# Extracted from: C:\DEV\PyAgent\.external\code_puppy\code_puppy\plugins\antigravity_oauth\__init__.py
"""Antigravity OAuth Plugin for Code Puppy.

Enables authentication with Google/Antigravity APIs to access Gemini and Claude models
via Google credentials. Supports multi-account load balancing and automatic failover.
"""

from .config import ANTIGRAVITY_OAUTH_CONFIG
from .register_callbacks import *  # noqa: F401, F403

__all__ = ["ANTIGRAVITY_OAUTH_CONFIG"]
