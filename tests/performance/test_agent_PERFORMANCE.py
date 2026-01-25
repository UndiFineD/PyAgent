#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""Test classes from test_agent.py - performance module."""

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

class TestBenchmarking:
    """Tests for execution benchmarking."""

    def test_benchmark_execution(self, tmp_path: Path, agent_module) -> None:
        """Test execution benchmarking."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'start_time': time.time() - 10,
            'end_time': time.time(),
            'files_processed': 5,
            'agents_applied': {'coder': 3, 'tests': 2},
        }

        files = [tmp_path / f'test{i}.py' for i in range(5)]
        for f in files:
            f.write_text('# test')

        benchmark = agent.benchmark_execution(files)

        assert benchmark['file_count'] == 5
        assert 'average_per_file' in benchmark



