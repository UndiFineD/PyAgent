# -*- coding: utf-8 -*-
"""
Unit tests for the shell and operational logic of the Base Agent.
Tests state persistence, response caching, plugin loading, and health diagnostics.
"""
# Shell Logic Focus (IO, Plugins, Diagnostics)

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

# Import from src
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

class TestAgentStatePersistence:
    def test_state_save_and_load(self, tmp_path: Path, base_agent_module: Any) -> None:
        StatePersistence = base_agent_module.StatePersistence
        state_file: Path = tmp_path / 'state.json'
        persistence = StatePersistence(state_file)
        state = {'counter': 42, 'items': ['a', 'b']}
        persistence.save(state)
        loaded = persistence.load()
        assert loaded['counter'] == 42

class TestContentBasedResponseCaching:
    def test_response_cache_set_get(self, base_agent_module: Any, tmp_path: Path) -> None:
        ResponseCache = base_agent_module.ResponseCache
        cache = ResponseCache(cache_dir=tmp_path)
        cache.set('prompt1', 'response1')
        assert cache.get('prompt1') == 'response1'

class TestAgentPluginLoading:
    def test_plugin_registration(self, base_agent_module: Any) -> None:
        PluginManager = base_agent_module.PluginManager
        manager = PluginManager()
        class MockPlugin:
            name: str = 'mock'
            def activate(self) -> None: pass
        manager.register(MockPlugin())
        assert 'mock' in manager.plugins

class TestAgentHealthDiagnostics:
    def test_health_check_basic(self, base_agent_module: Any) -> None:
        HealthChecker = base_agent_module.HealthChecker
        checker = HealthChecker()
        status = checker.check()
        assert 'status' in status

class TestCustomAuthenticationMethods:
    def test_auth_token_method(self, base_agent_module: Any) -> None:
        AuthMethod = base_agent_module.AuthMethod
        AuthManager = base_agent_module.AuthManager
        manager = AuthManager()
        manager.set_method(AuthMethod.TOKEN, token='secret-token')
        headers = manager.get_headers()
        assert 'Authorization' in headers
