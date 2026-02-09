# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\__init__.py
"""Factorio Learning Environment (FLE) package."""

# Suppress slpp SyntaxWarning about invalid escape sequences
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning, module="slpp")

__version__ = "0.3.0"

# Make submodules available
from fle import agents, cluster, commons, env, eval

# Auto-register all gym environments when FLE is imported
try:
    from fle.env.gym_env.registry import register_all_environments

    register_all_environments()
except ImportError:
    # Gym environments not available, continue without them
    pass

__all__ = ["agents", "env", "eval", "cluster", "commons"]
