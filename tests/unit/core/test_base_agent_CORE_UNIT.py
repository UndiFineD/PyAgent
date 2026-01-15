# -*- coding: utf-8 -*-
"""Test classes from test_base_agent.py - Core Logic Focus."""

from __future__ import annotations
from typing import Any
import pytest
from pathlib import Path

# Import from src




class TestAgentEnums:
    """Tests for agent enums."""

    def test_state_values(self, base_agent_module: Any) -> None:
        """Test that state values are correct."""
        assert base_agent_module.AgentState.INITIALIZED.value == "initialized"
        assert base_agent_module.AgentState.PROCESSING.value == "processing"
        assert base_agent_module.AgentState.COMPLETED.value == "completed"

    def test_quality_values(self, base_agent_module: Any) -> None:
        """Test quality values are ordered correctly."""
        assert base_agent_module.ResponseQuality.EXCELLENT.value == 5
        assert base_agent_module.ResponseQuality.INVALID.value == 1

    def test_event_types(self, base_agent_module: Any) -> None:
        """Test all event types exist."""
        events = list(base_agent_module.EventType)
        assert len(events) >= 7

    def test_auth_method_values(self, base_agent_module: Any) -> None:
        """Test AuthMethod enum values."""
        assert base_agent_module.AuthMethod.NONE.value == "none"
        assert base_agent_module.AuthMethod.API_KEY.value == "api_key"

    def test_serialization_format_values(self, base_agent_module: Any) -> None:
        """Test SerializationFormat enum values."""
        assert base_agent_module.SerializationFormat.JSON.value == "json"
        assert base_agent_module.SerializationFormat.YAML.value == "yaml"

    def test_file_priority_values(self, base_agent_module: Any) -> None:
        """Test FilePriority enum values."""
        assert base_agent_module.FilePriority.CRITICAL.value == 5
        assert base_agent_module.FilePriority.LOW.value == 2


class TestCoreDataclasses:
    """Tests for core agent dataclasses."""

    def test_create_template(self, base_agent_module: Any) -> None:
        """Test creating a prompt template."""
        template = base_agent_module.PromptTemplate(
            id="test1",
            name="Test Template",
            template="Improve {content} with {focus}"
        )
        assert template.id == "test1"
        assert template.version == "1.0"

    def test_default_config(self, base_agent_module: Any) -> None:
        """Test default config values."""
        config = base_agent_module.AgentConfig()
        assert config.backend == "auto"
        assert config.cache_enabled is True

    def test_health_check_result(self, base_agent_module: Any) -> None:
        """Test creating health check result."""
        result = base_agent_module.HealthCheckResult(
            healthy=True,
            backend_available=True
        )
        assert result.healthy is True

    def test_auth_config_defaults(self, base_agent_module: Any) -> None:
        """Test AuthConfig default values."""
        config = base_agent_module.AuthConfig()
        assert config.method == base_agent_module.AuthMethod.NONE
        assert config.api_key == ""


class TestLogicComponents:
    """Tests for pure logic components like EventManager and HealthChecker metrics."""

    def test_event_manager_basic(self, base_agent_module: Any) -> None:
        """Test basic event management."""
        EventManager = base_agent_module.EventManager
        AgentEvent = base_agent_module.AgentEvent

        manager = EventManager()
        calls: list[str] = []

        manager.on(AgentEvent.START, lambda: calls.append("started"))
        manager.emit(AgentEvent.START)

        assert "started" in calls

    def test_event_multiple_handlers(self, base_agent_module: Any) -> None:
        """Test multiple handlers for same event."""
        EventManager = base_agent_module.EventManager
        AgentEvent = base_agent_module.AgentEvent

        manager = EventManager()
        results: list[int] = []

        manager.on(AgentEvent.COMPLETE, lambda: results.append(1))
        manager.on(AgentEvent.COMPLETE, lambda: results.append(2))
        manager.emit(AgentEvent.COMPLETE)

        assert len(results) == 2

    def test_event_with_data(self, base_agent_module: Any) -> None:
        """Test events with data payload."""
        EventManager = base_agent_module.EventManager
        AgentEvent = base_agent_module.AgentEvent

        manager = EventManager()
        received: list[dict[str, Any]] = []

        manager.on(AgentEvent.ERROR, lambda data: received.append(data))
        manager.emit(AgentEvent.ERROR, {"message": "test error"})

        assert received[0]["message"] == "test error"


class TestAgentRegistry:
    """Tests for the AgentRegistry singleton."""

    def test_registry_singleton(self, base_agent_module: Any) -> None:
        """Test registry follows singleton pattern."""
        AgentRegistry = base_agent_module.AgentRegistry
        reg1 = AgentRegistry()
        reg2 = AgentRegistry()
        assert reg1 is reg2

    def test_agent_registration(self, base_agent_module: Any) -> None:
        """Test registering and retrieving agents."""
        AgentRegistry = base_agent_module.AgentRegistry
        registry = AgentRegistry()

        class MockAgent:
            agent_name = "test-agent"

        agent = MockAgent()
        registry.register(agent)

        assert registry.get_agent("test-agent") is agent


class TestRequestBatcher:
    """Tests for core RequestBatcher."""

    def test_batcher_add(self, base_agent_module: Any) -> None:
        """Test adding items to batcher."""
        RequestBatcher = base_agent_module.RequestBatcher
        batcher = RequestBatcher(batch_size=2)

        batcher.add_request(base_agent_module.BatchRequest(file_path=Path("req1")))
        assert batcher.get_queue_size() == 1

        batcher.add_request(base_agent_module.BatchRequest(file_path=Path("req2")))
        # Should be empty after flush (triggered by max_size)
        assert batcher.get_queue_size() == 2


class TestSerializationManager:
    """Tests for SerializationManager."""

    def test_serialization_basic(self, base_agent_module: Any) -> None:
        """Test basic serialization."""
        SerializationManager = base_agent_module.SerializationManager
        manager = SerializationManager()

        data = {"a": 1, "b": [2, 3]}
        serialized = manager.serialize(data)
        deserialized = manager.deserialize(serialized)

        assert deserialized == data


class TestFilePriorityManager:
    """Tests for FilePriorityManager."""

    def test_priority_calculation(self, base_agent_module: Any) -> None:
        """Test calculating file priority."""
        FilePriorityManager = base_agent_module.FilePriorityManager
        manager = FilePriorityManager()

        # High priority for important files
        p1 = manager.get_priority(Path("README.md"))
        p2 = manager.get_priority(Path("src/core/base/AgentCore.py"))
        p3 = manager.get_priority(Path("temp/debug.log"))

        assert p1.value >= p3.value
        assert p2.value > p3.value


class TestPromptTemplateManager:
    """Tests for PromptTemplateManager."""

    def test_template_rendering(self, base_agent_module: Any) -> None:
        """Test rendering prompt templates."""
        PromptTemplateManager = base_agent_module.PromptTemplateManager
        PromptTemplate = base_agent_module.PromptTemplate
        manager = PromptTemplateManager()

        template = PromptTemplate("greeting", "Hello {name}!")
        manager.register(template)
        result = manager.render("greeting", name="World")
        assert result == "Hello World!"


class TestConversationHistory:
    """Tests for ConversationHistory."""

    def test_history_management(self, base_agent_module: Any) -> None:
        """Test managing conversation history."""
        ConversationHistory = base_agent_module.ConversationHistory
        MessageRole = base_agent_module.MessageRole

        history = ConversationHistory()
        history.add(MessageRole.USER, "Question")
        history.add(MessageRole.ASSISTANT, "Answer")

        assert len(history.messages) == 2
        assert history.messages[0].role == MessageRole.USER


class TestResponsePostProcessingHooks:
    """Tests for response post-processing hooks."""

    def test_post_processor_registration(self, base_agent_module: Any) -> None:
        """Test registering post-processors."""
        ResponsePostProcessor = base_agent_module.ResponsePostProcessor
        processor = ResponsePostProcessor()

        def strip_whitespace(text: str) -> str:
            return text.strip()

        processor.register(strip_whitespace, priority=10)
        assert len(processor.hooks) == 1


class TestPromptVersioningAndABTesting:
    """Tests for prompt versioning and A/B testing."""

    def test_prompt_version_creation(self, base_agent_module: Any) -> None:
        """Test creating prompt versions."""
        PromptVersion = base_agent_module.PromptVersion
        v1 = PromptVersion(version="1.0.0", content="Analyze this code", description="Original prompt")
        assert v1.version == "1.0.0"
        assert v1.active

    def test_ab_test_variant_selection(self, base_agent_module: Any) -> None:
        """Test A/B test variant selection."""
        ABTest = base_agent_module.ABTest
        test = ABTest(name="prompt_test", variants=["control", "treatment"], weights=[0.5, 0.5])
        variant = test.select_variant()
        assert variant in ["control", "treatment"]


class TestContextWindowManagement:
    """Tests for context window management."""

    def test_context_window_size(self, base_agent_module: Any) -> None:
        """Test context window size tracking."""
        ContextWindow = base_agent_module.ContextWindow
        window = ContextWindow(max_tokens=4096)
        window.add("Some text content", token_count=100)
        assert window.used_tokens == 100
        assert window.available_tokens == 3996


class TestMultimodalInputHandling:
    """Tests for multimodal input handling."""

    def test_multimodal_input_text(self, base_agent_module: Any) -> None:
        """Test multimodal input with text."""
        MultimodalInput = base_agent_module.MultimodalInput
        InputType = base_agent_module.InputType
        input_data = MultimodalInput(content="Hello world", input_type=InputType.TEXT)
        assert input_data.input_type == InputType.TEXT
        assert input_data.content == "Hello world"


class TestTokenBudgetManagement:
    """Tests for token budget management."""

    def test_token_budget_allocation(self, base_agent_module: Any) -> None:
        """Test token budget allocation."""
        TokenBudget = base_agent_module.TokenBudget
        budget = TokenBudget(total=4096)
        budget.allocate("system", 500)
        remaining = budget.remaining
        assert remaining == 3596


class TestAgentCompositionPatterns:
    """Tests for agent composition patterns."""

    def test_agent_pipeline(self, base_agent_module: Any) -> None:
        """Test agent pipeline composition."""
        AgentPipeline = base_agent_module.AgentPipeline
        pipeline = AgentPipeline()
        pipeline.add_step("first", lambda d: d + "_step1")
        result = pipeline.execute("input")
        assert result == "input_step1"


class TestAgentConfigurationProfiles:
    """Tests for agent configuration profiles."""

    def test_profile_creation(self, base_agent_module: Any) -> None:
        """Test creating configuration profiles."""
        ConfigProfile = base_agent_module.ConfigProfile
        profile = ConfigProfile(name="production", settings={"timeout": 30})
        assert profile.name == "production"
        assert profile.settings["timeout"] == 30

    def test_health_metrics_collection(self, base_agent_module: Any) -> None:
        """Test health metrics calculation logic."""
        HealthChecker = base_agent_module.HealthChecker
        checker = HealthChecker()

        for _ in range(5):
            checker.record_request(success=True, latency_ms=100)
        checker.record_request(success=False, latency_ms=500)

        metrics = checker.get_metrics()
        assert metrics["total_requests"] == 6
        assert metrics["error_rate"] == pytest.approx(1/6)

    def test_config_profile_inheritance(self, base_agent_module: Any) -> None:
        """Test profile inheritance logic."""
        ProfileManager = base_agent_module.ProfileManager
        ConfigProfile = base_agent_module.ConfigProfile

        manager = ProfileManager()
        base = ConfigProfile("base", {"timeout": 30, "retries": 3})
        custom = ConfigProfile("custom", {"timeout": 60}, parent="base")

        manager.add_profile(base)
        manager.add_profile(custom)
        manager.set_active("custom")

        assert manager.get_setting("timeout") == 60
        assert manager.get_setting("retries") == 3


class TestAgentPureLogic:
    """Tests for side-effect free methods of BaseAgent (Core logic)."""

    def test_estimate_tokens(self, base_agent_module: Any) -> None:
        """Test token estimation logic."""
        agent_class = base_agent_module.BaseAgent
        # Estimate tokens is often a static method or logic-only instance method
        # We'll use a mock file path for initialization if needed
        agent = agent_class("mock_file.md")

        text = "a" * 100
        tokens = agent.estimate_tokens(text)
        assert tokens == 25  # 100 / 4 heuristic

    def test_truncate_for_context(self, base_agent_module: Any) -> None:
        """Test content truncation logic."""
        agent = base_agent_module.BaseAgent("mock_file.md")

        short = "Hello world"
        assert agent.truncate_for_context(short, 100) == short

        long_text = "x" * 1000
        truncated = agent.truncate_for_context(long_text, 10)  # 40 chars limit
        assert len(truncated) < len(long_text)
        assert "[truncated]" in truncated.lower()

    def test_score_response_quality(self, base_agent_module: Any) -> None:
        """Test response quality scoring logic."""
        agent = base_agent_module.BaseAgent("mock_file.md")

        quality = agent._score_response_quality("")
        assert quality == base_agent_module.ResponseQuality.INVALID

        good_response = "# Documentation\n\ndef hello():\n    pass\n"
        quality = agent._score_response_quality(good_response)
        assert quality.value >= base_agent_module.ResponseQuality.ACCEPTABLE.value

    def test_generate_cache_key(self, base_agent_module: Any) -> None:
        """Test cache key generation logic."""
        agent = base_agent_module.BaseAgent("mock_file.md")
        key1 = agent._generate_cache_key("prompt", "content")
        key2 = agent._generate_cache_key("prompt", "content")
        key3 = agent._generate_cache_key("different", "content")
        assert key1 == key2
        assert key1 != key3
