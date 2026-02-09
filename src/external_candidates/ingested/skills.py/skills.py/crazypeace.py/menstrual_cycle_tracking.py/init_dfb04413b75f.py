# Extracted from: C:\DEV\PyAgent\.external\skills\skills\crazypeace\menstrual-cycle-tracking\__init__.py
"""
Menstrual Tracking Skill for OpenClaw
Initialization module
"""

from .menstrual_tracker import MenstrualTracker

__version__ = "1.0.0"
__author__ = "OpenClaw Community"
__description__ = "A skill for tracking and analyzing menstrual cycle data"


def initialize_skill():
    """Initialize the menstrual tracking skill"""
    print("Menstrual Tracking Skill initialized")
    return MenstrualTracker()
