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
Module: test_api_security
Comprehensive tests for API security patterns implemented from 31-days-of-API-Security-Tips.
"""

import asyncio
import hmac
import hashlib
import pytest
from unittest.mock import patch

from src.core.base.logic.security.api_security_core import (
    APISecurityCore, AgentCredentials, InputValidator, RateLimiter,
    Authenticator, ErrorHandler, RateLimitConfig, SecurityEvent
)


class TestInputValidator:
    """Test input validation and sanitization."""

    def test_sanitize_string_removes_injection(self):
        """Test that dangerous injection patterns are removed."""
        dangerous_input = "<script>alert('xss')</script> UNION SELECT * FROM users"
        sanitized = InputValidator.sanitize_input(dangerous_input)
        assert "<script>" not in sanitized
        assert "UNION" not in sanitized
        assert "SELECT" not in sanitized

    def test_sanitize_dict_recursively(self):
        """Test sanitization of nested dictionaries."""
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
        """Test agent ID validation."""
        valid_id = "12345678-1234-1234-1234-123456789abc"
        invalid_id = "invalid-agent-id"
        assert InputValidator.validate_agent_id(valid_id)
        assert not InputValidator.validate_agent_id(invalid_id)

    def test_validate_resource_access(self):
        """Test BOLA prevention in resource access."""
        creds = AgentCredentials(
            agent_id="agent-1",
            secret_key="secret",
            tenant_id="tenant-1"
        )
        # Same agent, same tenant
        assert InputValidator.validate_resource_access("agent-1", "tenant-1_resource", creds)
        # Different agent
        assert not InputValidator.validate_resource_access("agent-2", "tenant-1_resource", creds)
        # Different tenant
        assert not InputValidator.validate_resource_access("agent-1", "tenant-2_resource", creds)


class TestRateLimiter:
    """Test rate limiting functionality."""

    def test_rate_limit_within_bounds(self):
        """Test that requests within limits are allowed."""
        limiter = RateLimiter(RateLimitConfig(requests_per_minute=5, burst_limit=10))
        agent_id = "test-agent"

        for _ in range(5):
            assert limiter.is_allowed(agent_id)

    def test_rate_limit_exceeded(self):
        """Test that exceeding rate limit blocks requests."""
        limiter = RateLimiter(RateLimitConfig(requests_per_minute=2, burst_limit=5))
        agent_id = "test-agent"

        # First two should be allowed
        assert limiter.is_allowed(agent_id)
        assert limiter.is_allowed(agent_id)
        # Third should be blocked
        assert not limiter.is_allowed(agent_id)

    def test_burst_limit(self):
        """Test burst limit enforcement."""
        limiter = RateLimiter(RateLimitConfig(requests_per_minute=10, burst_limit=1))
        agent_id = "test-agent"

        # First request allowed
        assert limiter.is_allowed(agent_id)
        # Immediate second request should be blocked due to burst limit
        assert not limiter.is_allowed(agent_id)


class TestAuthenticator:
    """Test authentication functionality."""

    def test_register_and_authenticate(self):
        """Test agent registration and authentication."""
        auth = Authenticator()
        creds = AgentCredentials(
            agent_id="agent-1",
            secret_key="my-secret-key",
            permissions={"read", "write"}
        )
        auth.register_agent(creds)

        # Generate valid token
        token = hmac.new(
            creds.secret_key.encode(),
            creds.agent_id.encode(),
            hashlib.sha256
        ).hexdigest()

        authenticated = auth.authenticate("agent-1", token)
        assert authenticated is not None
        assert authenticated.agent_id == "agent-1"

    def test_invalid_token_rejected(self):
        """Test that invalid tokens are rejected."""
        auth = Authenticator()
        creds = AgentCredentials(agent_id="agent-1", secret_key="secret")
        auth.register_agent(creds)

        invalid_token = "invalid-token"
        authenticated = auth.authenticate("agent-1", invalid_token)
        assert authenticated is None

    def test_authorize_permissions(self):
        """Test permission-based authorization."""
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
    """Test error handling and masking."""

    def test_mask_authentication_error(self):
        """Test that auth errors are properly masked."""
        error = ValueError("Authentication failed")
        masked = ErrorHandler.mask_error(error)
        assert "Access denied" in masked
        assert "Authentication failed" not in masked

    def test_mask_rate_limit_error(self):
        """Test that rate limit errors are masked."""
        error = ValueError("Rate limit exceeded")
        masked = ErrorHandler.mask_error(error)
        assert "Rate limit exceeded" in masked

    def test_mask_generic_error(self):
        """Test that generic errors are masked."""
        error = RuntimeError("Internal database error")
        masked = ErrorHandler.mask_error(error)
        assert "Internal error" in masked
        assert "database" not in masked

    @patch('src.core.base.logic.security.api_security_core.logging')
    def test_log_security_event(self, mock_logging):
        """Test security event logging."""
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
    """Test the main API security core."""

    @pytest.fixture
    def security_core(self):
        """Create a security core instance."""
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
        """Generate HMAC token for testing."""
        return hmac.new(
            secret.encode(),
            agent_id.encode(),
            hashlib.sha256
        ).hexdigest()

    @pytest.mark.asyncio
    async def test_secure_communication_success(self, security_core):
        """Test successful secure communication."""
        token = self.generate_token("agent-1", "secret")
        message = {
            "action": "communicate",
            "resource_id": "tenant-1_data",
            "data": "Hello <script>alert('xss')</script>"
        }

        result = await security_core.secure_communication("agent-1", "agent-2", message, token)

        # Check sanitization
        assert "<script>" not in result["data"]
        assert result["action"] == "communicate"

    @pytest.mark.asyncio
    async def test_authentication_failure(self, security_core):
        """Test authentication failure."""
        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Access denied: ValueError"):
                await security_core.secure_communication("agent-1", "agent-2", {}, "invalid-token")
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "AUTHENTICATION_FAILED"

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self, security_core):
        """Test rate limit enforcement."""
        token = self.generate_token("agent-1", "secret")
        security_core.rate_limiter.config.requests_per_minute = 1

        # First request should succeed
        await security_core.secure_communication("agent-1", "agent-2", {"action": "communicate"}, token)

        # Second should fail due to rate limit
        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Rate limit exceeded"):
                await security_core.secure_communication("agent-1", "agent-2", {"action": "communicate"}, token)
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "RATE_LIMIT_EXCEEDED"

    @pytest.mark.asyncio
    async def test_bola_prevention(self, security_core):
        """Test BOLA (IDOR) prevention."""
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
        """Test authorization failure."""
        token = self.generate_token("agent-1", "secret")
        message = {"action": "forbidden_action"}

        with patch.object(security_core.error_handler, 'log_security_event') as mock_log:
            with pytest.raises(ValueError, match="Access denied: ValueError"):
                await security_core.secure_communication("agent-1", "agent-2", message, token)
            mock_log.assert_called_once()
            assert mock_log.call_args[0][0].event_type == "AUTHORIZATION_FAILED"
