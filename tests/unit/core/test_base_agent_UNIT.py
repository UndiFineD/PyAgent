# -*- coding: utf-8 -*-
"""
Unit tests for the shell and operational logic of the Base Agent.
Tests state persistence, response caching, plugin loading, and health diagnostics.
"""
# Shell Logic Focus (IO, Plugins, Diagnostics)

from __future__ import annotations
from typing import Any
from pathlib import Path

# Import from src




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
            def setup(self) -> None: pass
            def health_check(self) -> Any:
                return base_agent_module.AgentHealthCheck(agent_name="mock", status="healthy")




            def run(self, path: Any, ctx: Any) -> bool: return False
            def shutdown(self) -> None: pass

        plugin = MockPlugin()
        # Manual registration since register() was removed in favor of discover/load
        manager.active_plugins[plugin.name] = plugin
        assert 'mock' in manager.active_plugins




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
