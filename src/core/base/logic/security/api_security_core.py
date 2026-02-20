#!/usr/bin/env python3
"""
Minimal API security core shim for tests.

Provides lightweight validators, authenticators and rate limiter
sufficient for unit tests to import and exercise security mixins.
"""
from __future__ import annotations




import hashlib
import hmac
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class AgentCredentials:
    agent_id: str
    secret_key: str
    permissions: Set[str] = field(default_factory=set)
    tenant_id: str = ""


@dataclass
class RateLimitConfig:
    requests_per_minute: int = 60
    burst_limit: int = 10


@dataclass
class SecurityEvent:
    timestamp: float
    event_type: str
    agent_id: str
    details: Dict[str, Any]
    severity: str = "INFO"


class InputValidator:
    @staticmethod
    def sanitize_input(input_data: Any) -> Any:
        return input_data

    @staticmethod
    def validate_agent_id(agent_id: str) -> bool:
        return True

    @staticmethod
    def validate_resource_access(agent_id: str, resource_id: str, credentials: AgentCredentials) -> bool:
        if agent_id != credentials.agent_id:
            return False
        return True


class RateLimiter:
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.requests: Dict[str, List[float]] = {}

    def is_allowed(self, agent_id: str) -> bool:
        now = time.time()
        self.requests.setdefault(agent_id, [])
        reqs = [t for t in self.requests[agent_id] if t > now - 60]
        self.requests[agent_id] = reqs
        if len(reqs) >= self.config.requests_per_minute:
            return False
        reqs.append(now)
        return True


class Authenticator:
    def __init__(self):
        self.credentials: Dict[str, AgentCredentials] = {}

    def register_agent(self, creds: AgentCredentials) -> None:
        self.credentials[creds.agent_id] = creds

    def authenticate(self, agent_id: str, token: str) -> Optional[AgentCredentials]:
        creds = self.credentials.get(agent_id)
        if not creds:
            return None
        expected = hmac.new(creds.secret_key.encode(), agent_id.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, token):
            return creds
        return None

    def authorize(self, creds: AgentCredentials, action: str) -> bool:
        return action in creds.permissions


class ErrorHandler:
    @staticmethod
    def mask_error(error: Exception) -> str:
        return f"Internal error: {type(error).__name__}"

    @staticmethod
    def log_security_event(event: SecurityEvent) -> None:
        logger = logging.getLogger("api_security")
        getattr(logger, event.severity.lower(), logger.info)(
            f"Security Event: {event.event_type} - Agent: {event.agent_id} - Details: {event.details}"
        )


class APISecurityCore:
    def __init__(self):
        self.validator = InputValidator()
        self.rate_limiter = RateLimiter(RateLimitConfig())
        self.authenticator = Authenticator()
        self.error_handler = ErrorHandler()
        self.logger = logging.getLogger(self.__class__.__name__)

        async def secure_communication(self, sender_id: str, receiver_id: str, message: Dict[str, Any], token: str) -> Dict[str, Any]:
        try:
        creds = self.authenticator.authenticate(sender_id, token)
        if not creds:
        raise ValueError("Authentication failed")
        if not self.rate_limiter.is_allowed(sender_id):
        raise ValueError("Rate limit exceeded")
        sanitized = self.validator.sanitize_input(message)
        if "resource_id" in sanitized and not self.validator.validate_resource_access(sender_id, sanitized["resource_id"], creds):
        raise ValueError("Access denied")
        action = sanitized.get("action", "")
        if not self.authenticator.authorize(creds, action):
        raise ValueError("Authorization failed")
        return sanitized
        except Exception as e:
        masked = self.error_handler.mask_error(e)
        self.logger.error(f"Security violation: {masked}")
        raise
