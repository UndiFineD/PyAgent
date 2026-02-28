# Extracted from: C:\DEV\PyAgent\.external\skills\skills\clawcolab\clawbrain\brain\__init__.py
"""Claw Brain - Brain module"""

__version__ = "3.0.0"

import importlib.util
import os

clawbrain_path = os.path.join(os.path.dirname(__file__), "clawbrain.py")
spec = importlib.util.spec_from_file_location("clawbrain", clawbrain_path)
clawbrain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clawbrain)

Brain = clawbrain.Brain
Memory = clawbrain.Memory
UserProfile = clawbrain.UserProfile
Embedder = clawbrain.Embedder

__all__ = ["Brain", "Memory", "UserProfile", "Embedder"]
