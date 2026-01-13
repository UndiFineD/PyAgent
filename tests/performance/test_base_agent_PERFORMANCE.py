# -*- coding: utf-8 -*-
"""Test classes from test_base_agent.py - performance module."""

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
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 

            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed

class TestRequestBatchingPerformance:
    """Tests for request batching performance."""

    def test_batch_request_creation(self, base_agent_module: Any) -> None:
        """Test creating batch requests."""
        BatchRequest = base_agent_module.BatchRequest

        batch = BatchRequest()
        batch.add("prompt1")
        batch.add("prompt2")
        batch.add("prompt3")

        assert batch.size == 3

    def test_batch_execution(self, base_agent_module: Any) -> None:
        """Test batch execution."""
        BatchRequest = base_agent_module.BatchRequest

        batch = BatchRequest()
        batch.add("A")
        batch.add("B")

        # Mock processor
        def processor(prompts: list[str]) -> list[str]:
            return [p.upper() for p in prompts]

        results = batch.execute(processor)
        assert results == ["A", "B"]

    def test_batch_max_size(self, base_agent_module: Any) -> None:
        """Test batch respects max size."""
        BatchRequest = base_agent_module.BatchRequest

        batch = BatchRequest(max_size=2)
        batch.add("A")
        batch.add("B")
        batch.add("C")  # Should trigger auto-flush or be rejected

        assert batch.size <= 2



