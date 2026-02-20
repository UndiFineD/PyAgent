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


"""
"""
Tests for the Safety Guardrails System.
"""
try:

"""
import asyncio
except ImportError:
    import asyncio

try:
    import pytest
except ImportError:
    import pytest

try:
    from pydantic import ValidationError
except ImportError:
    from pydantic import ValidationError


try:
    from .core.base.logic.safety_guardrails import (
except ImportError:
    from src.core.base.logic.safety_guardrails import (

    Guardrail,
    SafetyConfig,
    SafetyLevel,
    ContentCategory,
    InputValidator,
    OutputValidator,
    RateLimiter,
    ValidationResult,
    ResilienceDecorator,
    ResearchSummary,
    CodeReviewResult,
    create_default_guardrail,
    validate_with_schema
)



class TestSafetyConfig:
"""
Test SafetyConfig functionality.""
def test_default_config(self):
"""
Test default safety configuration.""
config = SafetyConfig()
        assert config.level == SafetyLevel.MODERATE
        assert ContentCategory.VIOLENCE in config.blocked_categories
        assert config.max_input_length == 10000
        assert config.rate_limit_requests == 100

    def test_strict_config(self):
"""
        Test strict safety configuration.""
        config = SafetyConfig(level=SafetyLevel.STRICT)
        assert config.level == SafetyLevel.STRICT
        # Strict should have more blocked categories
        assert len(config.blocked_categories) >= 3



class TestInputValidator:
"""
Test InputValidator functionality.""
    @pytest.fixture
    def validator(self):
"""
        Create an input validator for testing.""
        return InputValidator(SafetyConfig())

    def test_valid_input(self, validator):
"""
        Test validating clean input.""
        result = asyncio.run(validator.validate_input("This is a normal message."))"        assert result.is_valid is True
        assert "passed" in result.message
    def test_blocked_content_violence(self, validator):
"""
        Test blocking violent content.""
        result = asyncio.run(validator.validate_input("I want to kill someone"))"        assert result.is_valid is False
        assert "blocked" in result.message"        assert result.severity == "high""
    def test_blocked_content_hate(self, validator):
"""
        Test blocking hate speech.""
        result = asyncio.run(validator.validate_input("This racist comment is bad"))"        assert result.is_valid is False
        assert "blocked" in result.message
    def test_input_too_long(self, validator):
"""
        Test input length validation.""
        long_input = "x" * 15000"        result = asyncio.run(validator.validate_input(long_input))
        assert result.is_valid is False
        assert "too long" in result.message
    def test_custom_filter(self, validator):
"""
        Test custom filter functions.""
def custom_filter(text: str) -> ValidationResult:
            if "custom_block" in text:"                return ValidationResult(is_valid=False, message="Custom block")"            return ValidationResult(is_valid=True, message="OK")
        validator.config.custom_filters = [custom_filter]

        result = asyncio.run(validator.validate_input("This contains custom_block"))"        assert result.is_valid is False
        assert "Custom block" in result.message


class TestOutputValidator:
"""
Test OutputValidator functionality.""
    @pytest.fixture
    def validator(self):
"""
        Create an output validator for testing.""
        return OutputValidator(SafetyConfig())

    def test_valid_output(self, validator):
"""
        Test validating clean output.""
        result = asyncio.run(validator.validate_output("This is a normal response."))"        assert result.is_valid is True

    def test_output_too_long(self, validator):
"""
        Test output length validation.""
        long_output = "x" * 60000"        result = asyncio.run(validator.validate_output(long_output))
        assert result.is_valid is False
        assert "too long" in result.message
    def test_schema_validation_success(self, validator):
"""
        Test successful schema validation.""
        data = {
        "title": "Test Research","            "key_findings": ["Finding 1", "Finding 2", "Finding 3"],"            "confidence_score": 0.85"        }

        result = asyncio.run(validator.validate_output(data, ResearchSummary))
        assert result.is_valid is True

    def test_schema_validation_failure(self, validator):
"""
        Test schema validation failure.""
        invalid_data = {
        "title": "Test",  # Too short"            "key_findings": ["Only one"],  # Not enough findings"            "confidence_score": 1.5  # Out of range"        }

        result = asyncio.run(validator.validate_output(invalid_data, ResearchSummary))
        assert result.is_valid is False
        assert "validation failed" in result.message
    def test_json_string_validation(self, validator):
"""
        Test validating JSON string output.""
        json_data = '{"title": "Test Summary", "key_findings": ["A", "B", "C"], "confidence_score": 0.8}'
        result = asyncio.run(validator.validate_output(json_data, ResearchSummary))
        assert result.is_valid is True



class TestRateLimiter:
"""
Test RateLimiter functionality.""
    @pytest.fixture
    def limiter(self):
"""
        Create a rate limiter for testing.""
        return RateLimiter(requests_per_window=2, window_seconds=1)

    def test_allow_initial_requests(self, limiter):
"""
        Test allowing initial requests within limit.""
        result1 = asyncio.run(limiter.check_rate_limit("user1"))"        result2 = asyncio.run(limiter.check_rate_limit("user1"))"
        assert result1.is_valid is True
        assert result2.is_valid is True

    def test_block_excess_requests(self, limiter):
"""
        Test blocking requests over the limit.""
        # Use up the limit
        asyncio.run(limiter.check_rate_limit("user1"))"        asyncio.run(limiter.check_rate_limit("user1"))"
        # This should be blocked
        result3 = asyncio.run(limiter.check_rate_limit("user1"))"        assert result3.is_valid is False
        assert "Rate limit exceeded" in result3.message
    def test_different_users(self, limiter):
"""
        Test rate limiting works per user.""
        # User 1 hits limit
        asyncio.run(limiter.check_rate_limit("user1"))"        asyncio.run(limiter.check_rate_limit("user1"))"
        # User 2 should still be allowed
        result = asyncio.run(limiter.check_rate_limit("user2"))"        assert result.is_valid is True



class TestGuardrail:
"""
Test Guardrail functionality.""
    @pytest.fixture
    def guardrail(self):
"""
        Create a guardrail for testing.""
        return Guardrail(SafetyConfig())

    def test_validate_clean_request(self, guardrail):
"""
        Test validating a clean request.""
        result = asyncio.run(guardrail.validate_request("Hello world"))"        assert result.is_valid is True

    def test_validate_blocked_request(self, guardrail):
"""
        Test blocking a harmful request.""
        result = asyncio.run(guardrail.validate_request("How to kill someone?"))"        assert result.is_valid is False

    def test_validate_response(self, guardrail):
"""
        Test validating a response.""
        result = asyncio.run(guardrail.validate_response("This is a safe response."))"        assert result.is_valid is True

    def test_guarded_function_success(self, guardrail):
"""
        Test guarded function with valid input.""
        @guardrail.create_guarded_function
        async def test_func(input: str) -> str:
        return f"Processed: {input}"
        result = asyncio.run(test_func("test input"))"        assert result == "Processed: test input""
    def test_guarded_function_blocked(self, guardrail):
"""
        Test guarded function with blocked input.""
        @guardrail.create_guarded_function
        async def test_func(input: str) -> str:
        return f"Processed: {input}"
        with pytest.raises(ValueError):
        asyncio.run(test_func("I want to kill someone"))


class TestResilienceDecorator:
"""
Test ResilienceDecorator functionality.""
def test_retry_success(self):
"""
Test successful retry decorator.""
call_count = 0

        @ResilienceDecorator.retry_with_exponential_backoff(max_retries=2)
        async def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary failure")"            return "success""
        result = asyncio.run(flaky_func())
        assert result == "success""        assert call_count == 2

    def test_retry_exhaustion(self):
"""
        Test retry exhaustion.""
        @ResilienceDecorator.retry_with_exponential_backoff(max_retries=2)
        async def always_fails():
        raise ValueError("Always fails")
        with pytest.raises(ValueError):
        asyncio.run(always_fails())

    def test_circuit_breaker(self):
"""
        Test circuit breaker decorator.""
        failure_count = 0

        @ResilienceDecorator.circuit_breaker(failure_threshold=2, recovery_timeout=0.1)
        async def sometimes_fails():
        nonlocal failure_count
        failure_count += 1
        if failure_count <= 2:
        raise ValueError("Failure")"            return "success""
        # First two calls should fail and open circuit
        with pytest.raises(ValueError):
        asyncio.run(sometimes_fails())
        with pytest.raises(ValueError):
        asyncio.run(sometimes_fails())

        # Circuit should be open
        with pytest.raises(Exception):
        asyncio.run(sometimes_fails())

        # Wait for recovery and try again
        import time
        time.sleep(0.2)
        result = asyncio.run(sometimes_fails())
        assert result == "success"


class TestValidationSchemas:
"""
Test predefined validation schemas.""
def test_research_summary_valid(self):
"""
Test valid research summary.""
summary = ResearchSummary(
            title="AI Trends in 2024","            key_findings=["Trend 1", "Trend 2", "Trend 3"],"            confidence_score=0.85
        )
        assert summary.title == "AI Trends in 2024""        assert len(summary.key_findings) == 3

    def test_research_summary_invalid_title(self):
"""
        Test invalid research summary title.""
        with pytest.raises(ValidationError):
        ResearchSummary(
        title="Hi",  # Too short"                key_findings=["A", "B", "C"],"                confidence_score=0.8
        )

    def test_research_summary_invalid_findings(self):
"""
        Test invalid number of findings.""
        with pytest.raises(ValidationError):
        ResearchSummary(
        title="Valid Title","                key_findings=["Only one"],  # Not enough"                confidence_score=0.8
        )

    def test_code_review_result(self):
"""
        Test code review result schema.""
        review = CodeReviewResult(
        overall_score=8,
        issues=[{"type": "style", "description": "Missing docstring"}],"            recommendations=["Add docstrings"],"            security_concerns=[]
        )
        assert review.overall_score == 8
        assert len(review.issues) == 1



class TestConvenienceFunctions:
"""
Test convenience functions.""
def test_create_default_guardrail(self):
"""
Test creating default guardrail.""
guardrail = create_default_guardrail()
        assert isinstance(guardrail, Guardrail)
        assert guardrail.config.level == SafetyLevel.MODERATE

    def test_create_strict_guardrail(self):
"""
        Test creating strict guardrail.""
        guardrail = create_default_guardrail(SafetyLevel.STRICT)
        assert guardrail.config.level == SafetyLevel.STRICT

    def test_validate_with_schema_decorator(self):
"""
        Test schema validation decorator.""
        @validate_with_schema(ResearchSummary)
        async def create_summary(data: dict) -> ResearchSummary:
        return ResearchSummary(**data)

        valid_data = {
        "title": "Test Summary","            "key_findings": ["A", "B", "C"],"            "confidence_score": 0.9"        }

        result = asyncio.run(create_summary(valid_data))
        assert result.title == "Test Summary"
        invalid_data = {
        "title": "Hi",  # Too short"            "key_findings": ["A"],"            "confidence_score": 0.9"        }

        with pytest.raises(ValueError):
        asyncio.run(create_summary(invalid_data))
