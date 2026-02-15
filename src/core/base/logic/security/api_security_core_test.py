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

"""
Module: api_security_core_test
Comprehensive tests for API security patterns implemented from 31-days-of-API-Security-Tips.
"""

import hmac
import hashlib
import pytest
from unittest.mock import patch
from src.core.base.logic.security.api_security_core import (
    APISecurityCore, AgentCredentials, InputValidator, RateLimiter,
    Authenticator, ErrorHandler, RateLimitConfig, SecurityEvent
)

class TestInputValidator:
    def test_sanitize_string_removes_injection(self):
        dangerous_input = "<script>alert('xss')</script> UNION SELECT * FROM users"
        sanitized = InputValidator.sanitize_input(dangerous_input)
        assert "<script>" not in sanitized
        assert "UNION" not in sanitized
        assert "SELECT" not in sanitized
    def test_sanitize_dict_recursively(self):
        data = {
            "name": "<script>evil</script>",
            "nested": {
                "query": "SELECT * FROM users",
                "safe": "hello"
            }
        }
        sanitized = InputValidator.sanitize_input(data)
        assert "<script>" not in sanitized["name"]
        assert "SELECT" not in sanitized["nested"]["query"]
        assert sanitized["nested"]["safe"] == "hello"
    def test_validate_agent_id(self):
        valid_id = "12345678-1234-1234-1234-123456789abc"
        invalid_id = "invalid-agent-id"
        assert InputValidator.validate_agent_id(valid_id)
        assert not InputValidator.validate_agent_id(invalid_id)
    def test_validate_resource_access(self):
        creds = AgentCredentials(
            agent_id="agent-1",
            secret_key="secret",
            tenant_id="tenant-1"
        )
        assert InputValidator.validate_resource_access("agent-1", "tenant-1_resource", creds)
        assert not InputValidator.validate_resource_access("agent-2", "tenant-1_resource", creds)
        assert not InputValidator.validate_resource_access("agent-1", "tenant-2_resource", creds)

class TestRateLimiter:
    def test_rate_limit_within_bounds(self):
        limiter = RateLimiter(RateLimitConfig(requests_per_minute=5, burst_limit=10))
        agent_id = "test-agent"
        for _ in range(5):
            assert limiter.is_allowed(agent_id)
    def test_rate_limit_exceeded(self):
        limiter = RateLimiter(RateLimitConfig(requests_per_minute=2, burst_limit=5))
        agent_id = "test-agent"
        assert limiter.is_allowed(agent_id)
        assert limiter.is_allowed(agent_id)
        assert not limiter.is_allowed(agent_id)
    def test_burst_limit(self):
        limiter = RateLimiter(RateLimitConfig(requests_per_minute=10, burst_limit=1))
        agent_id = "test-agent"
        assert limiter.is_allowed(agent_id)
        assert not limiter.is_allowed(agent_id)

class TestAuthenticator:
    def test_register_and_authenticate(self):
        auth = Authenticator()
        creds = AgentCredentials(
            agent_id="agent-1",
            secret_key="my-secret-key",
            permissions={"read", "write"}
        )
        auth.register_agent(creds)
        token = hmac.new(
            creds.secret_key.encode(),
            creds.agent_id.encode(),
            hashlib.sha256
        ).hexdigest()
        authenticated = auth.authenticate("agent-1", token)
        assert authenticated is not None
        assert authenticated.agent_id == "agent-1"
    def test_invalid_token_rejected(self):
        auth = Authenticator()
        creds = AgentCredentials(agent_id="agent-1", secret_key="secret")
        auth.register_agent(creds)
        invalid_token = "invalid-token"
        authenticated = auth.authenticate("agent-1", invalid_token)
        assert authenticated is None
    def test_authorize_permissions(self):
        auth = Authenticator()
        creds = AgentCredentials(
            agent_id="agent-1",
            secret_key="secret",
            permissions={"read"}
        )
        auth.register_agent(creds)
        assert auth.authorize(creds, "read")
        assert not auth.authorize(creds, "write")

class TestErrorHandler:
    def test_mask_authentication_error(self):
        error = ValueError("Authentication failed")
        masked = ErrorHandler.mask_error(error)
        assert "Access denied" in masked
        assert "Authentication failed" not in masked
    def test_mask_rate_limit_error(self):
        error = ValueError("Rate limit exceeded")
        masked = ErrorHandler.mask_error(error)
        assert "Rate limit exceeded" in masked
    def test_mask_generic_error(self):
        error = RuntimeError("Internal database error")
        masked = ErrorHandler.mask_error(error)
        assert "Internal error" in masked
        assert "database" not in masked
    @patch('src.core.base.logic.security.api_security_core.logging')
    def test_log_security_event(self, mock_logging):
        event = SecurityEvent(
            timestamp=1234567890.0,
            event_type="AUTHENTICATION_FAILED",
            agent_id="agent-1",
            details={"ip": "192.168.1.1"},
            severity="WARNING"
        )
        ErrorHandler.log_security_event(event)
        mock_logging.getLogger.return_value.warning.assert_called_once()

class TestAPISecurityCore:
    @pytest.fixture
    def security_core(self):
        core = APISecurityCore()
        creds = AgentCredentials(
            agent_id="agent-1",
            secret_key="secret",
            permissions={"communicate"},
            tenant_id="tenant-1"
        )
        core.authenticator.register_agent(creds)
        return core
    def generate_token(self, agent_id: str, secret: str) -> str:
        return hmac.new(
            secret.encode(),
            agent_id.encode(),
            hashlib.sha256
        ).hexdigest()
    @pytest.mark.asyncio
    async def test_secure_communication_success(self, security_core):
        token = self.generate_token("agent-1", "secret")
        message = {
            "action": "communicate",
            "resource_id": "tenant-1_data",
            "data": "Hello <script>alert('xss')</script>"
        }
        result = await security_core.secure_communication("agent-1", "agent-2", message, token)
        assert "<script>" not in result["data"]
        assert result["action"] == "communicate"
    @pytest.mark.asyncio
    async def test_authentication_failure(self, security_core):
        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Access denied: ValueError"):
                await security_core.secure_communication("agent-1", "agent-2", {}, "invalid-token")
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "AUTHENTICATION_FAILED"
    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self, security_core):
        token = self.generate_token("agent-1", "secret")
        security_core.rate_limiter.config.requests_per_minute = 1
        await security_core.secure_communication("agent-1", "agent-2", {"action": "communicate"}, token)
        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Rate limit exceeded"):
                await security_core.secure_communication("agent-1", "agent-2", {"action": "communicate"}, token)
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "RATE_LIMIT_EXCEEDED"
    @pytest.mark.asyncio
    async def test_bola_prevention(self, security_core):
        token = self.generate_token("agent-1", "secret")
        message = {
            "action": "communicate",
            "resource_id": "tenant-2_forbidden"  # Wrong tenant
        }
        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Internal error: ValueError"):
                await security_core.secure_communication("agent-1", "agent-2", message, token)
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "BOLA_ATTEMPT"
    @pytest.mark.asyncio
    async def test_authorization_failure(self, security_core):
        token = self.generate_token("agent-1", "secret")
        message = {"action": "forbidden_action"}
        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Access denied: ValueError"):
                await security_core.secure_communication("agent-1", "agent-2", message, token)
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "AUTHORIZATION_FAILED"
