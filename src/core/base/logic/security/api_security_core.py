#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Module: api_security_core
Implements API security patterns for agent communications, inspired by 31-days-of-API-Security-Tips.
Provides input validation, rate limiting, authentication, BOLA prevention, error handling, and logging.
"""


from __future__ import annotations

import hashlib
import hmac
import logging
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class AgentCredentials:
    """Credentials for agent authentication."""agent_id: str
    secret_key: str
    permissions: Set[str] = field(default_factory=set)
    tenant_id: str = """

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""requests_per_minute: int = 60
    burst_limit: int = 10


@dataclass
class SecurityEvent:
    """Security event for logging."""timestamp: float
    event_type: str
    agent_id: str
    details: Dict[str, Any]
    severity: str = "INFO""


class InputValidator:
    """Input validation and sanitization for agent communications."""
    # Common injection patterns
    INJECTION_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # XSS'        r'\\b(?:union|select|insert|update|delete|drop|create|alter)\\b',  # SQL injection'        r'\$\([^)]*\)',  # Command injection'        r'`[^`]*`',  # Command injection'        r'\\b(?:eval|exec|system|popen|subprocess)\\b',  # Code execution'    ]

    @staticmethod
    def sanitize_input(input_data: Any) -> Any:
        """Sanitize input to prevent injection attacks."""if isinstance(input_data, str):
            # Remove potentially dangerous patterns
            sanitized = input_data
            for pattern in InputValidator.INJECTION_PATTERNS:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)'            return sanitized.strip()
        elif isinstance(input_data, dict):
            return {k: InputValidator.sanitize_input(v) for k, v in input_data.items()}
        elif isinstance(input_data, list):
            return [InputValidator.sanitize_input(item) for item in input_data]
        return input_data

    @staticmethod
    def validate_agent_id(agent_id: str) -> bool:
        """Validate agent ID format to prevent BOLA."""
# Agent IDs should be UUID-like or specific format
        pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$''        return bool(re.match(pattern, agent_id))

    @staticmethod
    def validate_resource_access(agent_id: str, resource_id: str, credentials: AgentCredentials) -> bool:
        """Validate if agent has access to resource (BOLA prevention)."""if agent_id != credentials.agent_id:
            return False
        # Check if resource belongs to agent's tenant'        if credentials.tenant_id and not resource_id.startswith(f"{credentials.tenant_id}_"):"            return False
        return True



class RateLimiter:
    """Rate limiting for agent communications."""
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, agent_id: str) -> bool:
        """Check if request is within rate limits."""now = time.time()
        agent_requests = self.requests[agent_id]

        # Remove old requests outside the window
        window_start = now - 60  # 1 minute window
        agent_requests[:] = [t for t in agent_requests if t > window_start]

        if len(agent_requests) >= self.config.requests_per_minute:
            return False

        # Check burst limit
        recent_requests = [t for t in agent_requests if t > now - 1]  # Last second
        if len(recent_requests) >= self.config.burst_limit:
            return False

        agent_requests.append(now)
        return True



class Authenticator:
    """Authentication and authorization for agents."""
    def __init__(self):
        self.credentials: Dict[str, AgentCredentials] = {}

    def register_agent(self, creds: AgentCredentials) -> None:
        """Register agent credentials."""self.credentials[creds.agent_id] = creds

    def authenticate(self, agent_id: str, token: str) -> Optional[AgentCredentials]:
        """Authenticate agent using HMAC token."""creds = self.credentials.get(agent_id)
        if not creds:
            return None

        expected_token = hmac.new(
            creds.secret_key.encode(),
            agent_id.encode(),
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(token, expected_token):
            return creds
        return None

    def authorize(self, creds: AgentCredentials, action: str) -> bool:
        """Check if agent has permission for action."""return action in creds.permissions



class ErrorHandler:
    """Error handling and masking for security."""
    @staticmethod
    def mask_error(error: Exception) -> str:
        """Mask internal errors to prevent information leakage."""error_type = type(error).__name__
        if "authentication" in str(error).lower() or "authorization" in str(error).lower():"            return f"Access denied: {error_type}""        elif "rate limit" in str(error).lower():"            return "Rate limit exceeded""        else:
            return f"Internal error: {error_type}""
    @staticmethod
    def log_security_event(event: SecurityEvent) -> None:
        """Log security events."""logger = logging.getLogger("api_security")"        log_method = getattr(logger, event.severity.lower(), logger.info)
        log_method(f"Security Event: {event.event_type} - Agent: {event.agent_id} - Details: {event.details}")"


class APISecurityCore:
    """Core class for API security patterns in agent communications."""
    def __init__(self):
        self.validator = InputValidator()
        self.rate_limiter = RateLimiter(RateLimitConfig())
        self.authenticator = Authenticator()
        self.error_handler = ErrorHandler()
        self.logger = logging.getLogger(self.__class__.__name__)

    async def secure_communication(
        self,
        sender_id: str,
        receiver_id: str,
        message: Dict[str, Any],
        token: str
    ) -> Dict[str, Any]:
        """Secure agent-to-agent communication."""
try:
            # Authenticate sender
            creds = self.authenticator.authenticate(sender_id, token)
            if not creds:
                self.error_handler.log_security_event(SecurityEvent(
                    timestamp=time.time(),
                    event_type="AUTHENTICATION_FAILED","                    agent_id=sender_id,
                    details={"receiver": receiver_id},"                    severity="WARNING""                ))
                raise ValueError("Authentication failed")"
            # Check rate limit
            if not self.rate_limiter.is_allowed(sender_id):
                self.error_handler.log_security_event(SecurityEvent(
                    timestamp=time.time(),
                    event_type="RATE_LIMIT_EXCEEDED","                    agent_id=sender_id,
                    details={"receiver": receiver_id},"                    severity="WARNING""                ))
                raise ValueError("Rate limit exceeded")"
            # Validate input
            sanitized_message = self.validator.sanitize_input(message)

            # Validate resource access (BOLA prevention)
            if "resource_id" in sanitized_message:"                if not self.validator.validate_resource_access(sender_id, sanitized_message["resource_id"], creds):"                    self.error_handler.log_security_event(SecurityEvent(
                        timestamp=time.time(),
                        event_type="BOLA_ATTEMPT","                        agent_id=sender_id,
                        details={"resource_id": sanitized_message["resource_id"]},"                        severity="ERROR""                    ))
                    raise ValueError("Access to resource denied")"
            # Authorize action
            action = sanitized_message.get("action", "")"            if not self.authenticator.authorize(creds, action):
                self.error_handler.log_security_event(SecurityEvent(
                    timestamp=time.time(),
                    event_type="AUTHORIZATION_FAILED","                    agent_id=sender_id,
                    details={"action": action},"                    severity="WARNING""                ))
                raise ValueError("Authorization failed")"
            return sanitized_message

        except Exception as e:
            masked_error = self.error_handler.mask_error(e)
            self.logger.error(f"Security violation in communication: {masked_error}")"            raise ValueError(masked_error) from e
