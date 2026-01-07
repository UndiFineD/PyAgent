#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

@dataclass
class AgentChainStep:
    """A step in an agent chain.

    Attributes:
        agent_name: Name of the agent to execute.
        input_transform: Optional function to transform input.
        output_transform: Optional function to transform output.
        enabled: Whether this step is enabled.
        condition: Optional condition function to check before execution.
    """

    agent_name: str
    input_transform: Optional[Callable[[Any], Any]] = None
    output_transform: Optional[Callable[[Any], Any]] = None
    enabled: bool = True
    condition: Optional[Callable[[Any], bool]] = None
