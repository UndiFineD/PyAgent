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
Guardrails and Safety Patterns for Agent Systems

This module implements comprehensive safety mechanisms for multi-agent systems including:
- Input validation and moderation
- Output validation and filtering
- Structured output schemas
- Error handling and resilience
- Rate limiting and abuse prevention

Based on patterns from agentic_design_patterns repository.
"""

import asyncio
import json
import logging
import re
import time
from functools import wraps
from typing import Any, Dict, List, Optional, Callable, TypeVar
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, field_validator

logger = logging.getLogger(__name__)

T = TypeVar('T')


class ValidationResult(BaseModel):
    """Result of a validation operation."""
    is_valid: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: str = Field(default="low", description="Validation severity level")


class SafetyLevel(Enum):
    """Safety enforcement levels."""
    PERMISSIVE = "permissive"
    MODERATE = "moderate"
    STRICT = "strict"
    PARANOID = "paranoid"


class ContentCategory(Enum):
    """Content categories for filtering."""
    VIOLENCE = "violence"
    HATE_SPEECH = "hate_speech"
    ADULT_CONTENT = "adult_content"
    SPAM = "spam"
    MALICIOUS_CODE = "malicious_code"
    SENSITIVE_DATA = "sensitive_data"


@dataclass
class SafetyConfig:
    """Configuration for safety mechanisms."""
    level: SafetyLevel = SafetyLevel.MODERATE
    blocked_categories: List[ContentCategory] = field(default_factory=lambda: [
        ContentCategory.VIOLENCE,
        ContentCategory.HATE_SPEECH,
        ContentCategory.MALICIOUS_CODE
    ])
    max_input_length: int = 10000
    max_output_length: int = 50000
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    enable_logging: bool = True
    custom_filters: List[Callable[[str], ValidationResult]] = field(default_factory=list)


class InputValidator:
    """Validates and moderates input content."""

    def __init__(self, config: SafetyConfig):
        self.config = config
        self._patterns = self._build_patterns()

    def _build_patterns(self) -> Dict[ContentCategory, List[str]]:
        """Build regex patterns for content filtering."""
        return {
            ContentCategory.VIOLENCE: [
                r'\b(kill|murder|attack|assault|harm|injure)\b',
                r'\b(weapon|gun|knife|bomb|explosive)\b',
                r'\b(violent|brutal|savage)\b'
            ],
            ContentCategory.HATE_SPEECH: [
                r'\b(racist|sexist|homophobic|transphobic)\b',
                r'\b(hate|bigot|supremacist)\b',
                r'\b(slur|derogatory|offensive)\b'
            ],
            ContentCategory.ADULT_CONTENT: [
                r'\b(porn|sex|naked|nude|erotic)\b',
                r'\b(adult|xxx|mature)\b'
            ],
            ContentCategory.SPAM: [
                r'\b(buy now|click here|free money|win prize)\b',
                r'\b(casino|lottery|scam)\b'
            ],
            ContentCategory.MALICIOUS_CODE: [
                r'\b(eval|exec|system|subprocess|os\.system)\b',
                r'\b(rm -rf|format|delete)\b',
                r'\b(malware|virus|trojan|ransomware)\b'
            ],
            ContentCategory.SENSITIVE_DATA: [
                r'\b(\d{3}-\d{2}-\d{4})\b',  # SSN pattern
                r'\b(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})\b',  # Credit card
                r'\b(password|secret|token|key)\s*[:=]\s*\S+\b'
            ]
        }

    async def validate_input(self, content: str, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate input content against safety rules."""
        try:
            # Length check
            if len(content) > self.config.max_input_length:
                return ValidationResult(
                    is_valid=False,
                    message=f"Input too long: {len(content)} > {self.config.max_input_length}",
                    severity="high"
                )

            # Content category filtering
            for category in self.config.blocked_categories:
                if category in self._patterns:
                    for pattern in self._patterns[category]:
                        if re.search(pattern, content, re.IGNORECASE):
                            return ValidationResult(
                                is_valid=False,
                                message=f"Content blocked: {category.value}",
                                severity="high",
                                details={"category": category.value, "pattern": pattern}
                            )

            # Custom filters
            for filter_func in self.config.custom_filters:
                result = await self._run_filter(filter_func, content)
                if not result.is_valid:
                    return result

            # All checks passed
            return ValidationResult(
                is_valid=True,
                message="Input validation passed",
                severity="low"
            )

        except Exception as e:
            logger.error(f"Error during input validation: {e}")
            return ValidationResult(
                is_valid=False,
                message=f"Validation error: {str(e)}",
                severity="high"
            )

    async def _run_filter(self, filter_func: Callable[[str], ValidationResult], content: str) -> ValidationResult:
        """Run a custom filter function."""
        try:
            # Run filter in thread pool if it's synchronous
            if asyncio.iscoroutinefunction(filter_func):
                return await filter_func(content)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, filter_func, content)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Filter error: {str(e)}",
                severity="medium"
            )


class OutputValidator:
    """Validates and filters output content."""

    def __init__(self, config: SafetyConfig):
        self.config = config

    async def validate_output(
        self,
        content: Any,
        expected_schema: Optional[BaseModel] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate output content."""
        try:
            # Convert to string for basic checks
            content_str = str(content)

            # Length check
            if len(content_str) > self.config.max_output_length:
                return ValidationResult(
                    is_valid=False,
                    message=f"Output too long: {len(content_str)} > {self.config.max_output_length}",
                    severity="medium"
                )

            # Schema validation if provided
            if expected_schema:
                validation_result = await self._validate_schema(content, expected_schema)
                if not validation_result.is_valid:
                    return validation_result

            # Content safety checks
            safety_result = await self._check_output_safety(content_str)
            if not safety_result.is_valid:
                return safety_result

            return ValidationResult(
                is_valid=True,
                message="Output validation passed",
                severity="low"
            )

        except Exception as e:
            logger.error(f"Error during output validation: {e}")
            return ValidationResult(
                is_valid=False,
                message=f"Validation error: {str(e)}",
                severity="high"
            )

    async def _validate_schema(self, content: Any, schema: BaseModel) -> ValidationResult:
        """Validate content against a Pydantic schema."""
        try:
            if isinstance(content, dict):
                validated = schema(**content)
            elif isinstance(content, str):
                # Try to parse as JSON
                data = json.loads(content)
                validated = schema(**data)
            else:
                # Try direct validation
                validated = schema(content)

            return ValidationResult(
                is_valid=True,
                message="Schema validation passed",
                details={"validated_data": validated.model_dump()}
            )

        except (ValidationError, json.JSONDecodeError) as e:
            return ValidationResult(
                is_valid=False,
                message=f"Schema validation failed: {str(e)}",
                severity="medium",
                details={"error": str(e)}
            )

    async def _check_output_safety(self, content: str) -> ValidationResult:
        """Check output content for safety issues."""
        # Basic checks for potentially harmful content
        dangerous_patterns = [
            r'\b(rm -rf|del|format|destroy)\b',
            r'\b(password|secret|token)\s*[:=]\s*\S+\b',
            r'\b(malware|virus|exploit)\b'
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return ValidationResult(
                    is_valid=False,
                    message="Potentially harmful content detected",
                    severity="high",
                    details={"pattern": pattern}
                )

        return ValidationResult(is_valid=True, message="Safety check passed")


class RateLimiter:
    """Rate limiting for agent requests."""

    def __init__(self, requests_per_window: int = 100, window_seconds: int = 60):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = {}

    async def check_rate_limit(self, identifier: str) -> ValidationResult:
        """Check if request is within rate limits."""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
        else:
            self.requests[identifier] = []

        # Check limit
        if len(self.requests[identifier]) >= self.requests_per_window:
            return ValidationResult(
                is_valid=False,
                message=f"Rate limit exceeded: {self.requests_per_window} requests per {self.window_seconds}s",
                severity="medium",
                details={
                    "current_requests": len(self.requests[identifier]),
                    "limit": self.requests_per_window,
                    "window_seconds": self.window_seconds
                }
            )

        # Add current request
        self.requests[identifier].append(now)

        return ValidationResult(
            is_valid=True,
            message="Rate limit check passed",
            details={"remaining_requests": self.requests_per_window - len(self.requests[identifier])}
        )


class Guardrail:
    """Comprehensive guardrail system combining multiple safety mechanisms."""

    def __init__(self, config: Optional[SafetyConfig] = None):
        self.config = config or SafetyConfig()
        self.input_validator = InputValidator(self.config)
        self.output_validator = OutputValidator(self.config)
        self.rate_limiter = RateLimiter(
            self.config.rate_limit_requests,
            self.config.rate_limit_window_seconds
        )

    async def validate_request(
        self,
        input_content: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate an incoming request."""
        # Rate limiting
        if user_id:
            rate_result = await self.rate_limiter.check_rate_limit(user_id)
            if not rate_result.is_valid:
                return rate_result

        # Input validation
        input_result = await self.input_validator.validate_input(input_content, context)
        if not input_result.is_valid:
            return input_result

        return ValidationResult(
            is_valid=True,
            message="Request validation passed",
            details={
                "input_validation": input_result.details,
                "rate_limit": rate_result.details if user_id else None
            }
        )

    async def validate_response(
        self,
        output_content: Any,
        expected_schema: Optional[BaseModel] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate an outgoing response."""
        return await self.output_validator.validate_output(output_content, expected_schema, context)

    def create_guarded_function(
        self,
        func: Callable[..., T],
        input_param: str = "input",
        output_schema: Optional[BaseModel] = None,
        user_id_param: Optional[str] = None
    ) -> Callable[..., T]:
        """Create a guarded version of a function with automatic validation."""

        @wraps(func)
        async def guarded_function(*args, **kwargs) -> T:
            # Extract parameters - try kwargs first, then positional args
            input_content = kwargs.get(input_param)
            user_id = kwargs.get(user_id_param) if user_id_param else None

            # If input_content not in kwargs, check positional args
            if input_content is None and input_param in func.__code__.co_varnames:
                param_index = func.__code__.co_varnames.index(input_param)
                if param_index < len(args):
                    input_content = args[param_index]

            # Validate request
            if input_content is not None:
                request_validation = await self.validate_request(input_content, user_id)
                if not request_validation.is_valid:
                    raise ValueError(f"Request validation failed: {request_validation.message}")

            # Execute function
            try:
                result = await func(*args, **kwargs)

                # Validate response
                if output_schema:
                    response_validation = await self.validate_response(result, output_schema)
                    if not response_validation.is_valid:
                        raise ValueError(f"Response validation failed: {response_validation.message}")

                return result

            except Exception as e:
                logger.error(f"Error in guarded function {func.__name__}: {e}")
                raise

        return guarded_function


class ResilienceDecorator:
    """Decorator for adding resilience patterns to functions."""

    @staticmethod
    def retry_with_exponential_backoff(
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 60.0
    ):
        """Decorator that retries a function with exponential backoff."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                delay = initial_delay
                last_exception = None

                for attempt in range(max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt == max_retries:
                            logger.error(f"Function {func.__name__} failed after {max_retries + 1} attempts")
                            raise e

                        logger.warning(f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}")
                        await asyncio.sleep(min(delay, max_delay))
                        delay *= backoff_factor

                # This should never be reached, but just in case
                raise last_exception

            return wrapper
        return decorator

    @staticmethod
    def circuit_breaker(
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Exception = Exception
    ):
        """Circuit breaker decorator."""
        def decorator(func):
            failures = 0
            last_failure_time = None
            state = "closed"  # closed, open, half-open

            @wraps(func)
            async def wrapper(*args, **kwargs):
                nonlocal failures, last_failure_time, state

                now = time.time()

                # Check if circuit should be half-open
                if state == "open" and last_failure_time:
                    if now - last_failure_time > recovery_timeout:
                        state = "half-open"
                        logger.info(f"Circuit breaker for {func.__name__} entering half-open state")

                # Check circuit state
                if state == "open":
                    raise Exception(f"Circuit breaker is open for {func.__name__}")

                try:
                    result = await func(*args, **kwargs)

                    # Success - reset failures and close circuit
                    if state == "half-open":
                        state = "closed"
                        failures = 0
                        logger.info(f"Circuit breaker for {func.__name__} closed after successful call")

                    return result

                except expected_exception as e:
                    failures += 1
                    last_failure_time = now

                    if failures >= failure_threshold:
                        state = "open"
                        logger.warning(f"Circuit breaker for {func.__name__} opened after {failures} failures")

                    raise e

            return wrapper
        return decorator


# Example usage and predefined schemas

class ResearchSummary(BaseModel):
    """Schema for research summary outputs."""
    title: str = Field(..., description="A concise title for the research summary")
    key_findings: List[str] = Field(..., description="A list of 3-5 key findings")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score from 0.0 to 1.0")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v.strip()) < 5:
            raise ValueError('Title must be at least 5 characters long')
        return v

    @field_validator('key_findings')
    @classmethod
    def validate_findings(cls, v: List[str]) -> List[str]:
        if len(v) < 3:
            raise ValueError('Must have at least 3 key findings')
        if len(v) > 5:
            raise ValueError('Cannot have more than 5 key findings')
        return v


class CodeReviewResult(BaseModel):
    """Schema for code review outputs."""
    overall_score: int = Field(..., ge=1, le=10, description="Overall code quality score")
    issues: List[Dict[str, str]] = Field(..., description="List of identified issues")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    security_concerns: List[str] = Field(default_factory=list, description="Security-related concerns")


# Convenience functions

def create_default_guardrail(level: SafetyLevel = SafetyLevel.MODERATE) -> Guardrail:
    """Create a guardrail with default configuration."""
    config = SafetyConfig(level=level)
    return Guardrail(config)


def validate_with_schema(schema: BaseModel):
    """Decorator to validate function output against a schema."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            try:
                if isinstance(result, dict):
                    validated = schema(**result)
                elif isinstance(result, schema):
                    validated = result  # Already validated
                else:
                    validated = schema(result)
                return validated
            except ValidationError as e:
                raise ValueError(f"Output validation failed: {e}")

        return wrapper
    return decorator
