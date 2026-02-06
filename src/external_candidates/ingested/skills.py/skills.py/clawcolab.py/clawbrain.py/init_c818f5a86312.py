# Extracted from: C:\DEV\PyAgent\.external\skills\skills\clawcolab\clawbrain\__init__.py
"""
Claw Brain v3 - Personal AI Memory System for AI Agents

A sophisticated memory and learning system that enables truly personalized AI-human communication.

Install: pip install git+https://github.com/clawcolab/clawbrain.git
"""

__version__ = "3.0.0"
__author__ = "ClawColab"

# Core exports
from clawbrain import Brain, Embedder, Memory, UserProfile

__all__ = ["Brain", "Memory", "UserProfile", "Embedder"]
