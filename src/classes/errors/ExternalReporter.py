#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess

class ExternalReporter(Enum):
    """External error reporting systems."""
    SENTRY = "sentry"
    ROLLBAR = "rollbar"
    BUGSNAG = "bugsnag"
    DATADOG = "datadog"
    NEWRELIC = "newrelic"
