# -*- coding: utf-8 -*-
"""Test classes from test_agent_changes_tests.py - performance module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestChangelogPerformance:
    """Tests for changelog performance with large histories."""

    def test_large_changelog_readable(self, tmp_path: Path) -> None:
        """Test large changelog can be read."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        # Create large changelog
        entries = "\n".join([f"- Entry {i}" for i in range(100)])
        content = f"# Changelog\n{entries}"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Entry 0" in previous
        assert "Entry 99" in previous


# =============================================================================
# Session 9: Backup and Recovery Tests
# =============================================================================



