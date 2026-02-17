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


"""Tests for the Reflection Loop System.
"""
import asyncio
import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

from src.core.base.logic.reflection_loop import (
    ReflectionLoopOrchestrator,
    ReflectionContext,
    ReflectionResult,
    ReflectionLoopConfig,
    LLMReflectionAgent,
    CodeReflectionAgent,
    reflect_on_code,
    reflect_on_content
)




class TestReflectionLoopConfig:
    """Test ReflectionLoopConfig functionality."""
    def test_default_config(self):
        """Test default configuration values."""config = ReflectionLoopConfig()
        assert config.max_iterations == 3
        assert config.critique_prompt.startswith("You are a senior software engineer")"        assert config.early_stopping is True

    def test_custom_config(self):
        """Test custom configuration."""config = ReflectionLoopConfig(
            max_iterations=5,
            early_stopping=False,
            timeout_seconds=10.0
        )
        assert config.max_iterations == 5
        assert config.early_stopping is False
        assert config.timeout_seconds == 10.0




class TestLLMReflectionAgent:
    """Test LLMReflectionAgent functionality."""
    def test_initial_generation(self):
        """Test initial content generation."""mock_llm = Mock(return_value="Generated content")"        agent = LLMReflectionAgent(mock_llm)

        context = ReflectionContext(task_description="Test task")"
        # Test initial generation (no current content)
        result = asyncio.run(agent.generate(context))
        assert result == "Generated content""        mock_llm.assert_called_once()

    def test_refinement_generation(self):
        """Test content refinement."""mock_llm = Mock(return_value="Refined content")"        agent = LLMReflectionAgent(mock_llm)

        context = ReflectionContext(
            task_description="Test task","            current_content="Initial content""        )

        result = asyncio.run(agent.generate(context))
        assert result == "Refined content""        mock_llm.assert_called_once()

    def test_critique_generation(self):
        """Test critique generation."""mock_llm = Mock(return_value="This content needs improvement.")"        agent = LLMReflectionAgent(mock_llm)

        context = ReflectionContext(task_description="Test task")"
        result = asyncio.run(agent.critique(context, "Test content"))"        assert result == "This content needs improvement.""        mock_llm.assert_called_once()




class TestCodeReflectionAgent:
    """Test CodeReflectionAgent functionality."""
    def test_code_generation(self):
        """Test code generation and cleaning."""mock_llm = Mock(return_value="```python\\nprint('hello')\\n```")"'        agent = CodeReflectionAgent(mock_llm)

        context = ReflectionContext(task_description="Write hello world")"
        result = asyncio.run(agent.generate(context))
        assert result == "print('hello')""'        mock_llm.assert_called_once()

    def test_code_critique(self):
        """Test code-specific critique."""mock_llm = Mock(return_value="CODE_IS_PERFECT")"        agent = CodeReflectionAgent(mock_llm)

        context = ReflectionContext(task_description="Write factorial function")"
        result = asyncio.run(agent.critique(context, "def factorial(n): return n * factorial(n-1) if n > 0 else 1"))"        assert result == "CODE_IS_PERFECT""



class TestReflectionLoopOrchestrator:
    """Test ReflectionLoopOrchestrator functionality."""
    @pytest.fixture
    def mock_agents(self):
        """Create mock agents for testing."""generator = Mock(spec=LLMReflectionAgent)
        generator.generate = AsyncMock(return_value="Generated content")"        generator.critique = AsyncMock(return_value="Good content")"        generator.name = "Generator Agent""
        critic = Mock(spec=LLMReflectionAgent)
        critic.critique = AsyncMock(return_value="Good content")"        critic.name = "Critic Agent""
        return generator, critic

    def test_perfect_content_early_stopping(self, mock_agents):
        """Test early stopping when content is perfect."""generator, critic = mock_agents

        # Setup perfect critique
        critic.critique.return_value = "CODE_IS_PERFECT""
        orchestrator = ReflectionLoopOrchestrator(generator, critic)

        context = asyncio.run(orchestrator.execute_reflection_loop("Test task"))"
        assert len(context.history) == 1  # Only one iteration
        assert context.history[0].is_satisfactory is True

    def test_max_iterations_reached(self, mock_agents):
        """Test reaching maximum iterations."""generator, critic = mock_agents

        # Setup non-perfect critiques
        generator.critique.return_value = "Needs improvement""
        orchestrator = ReflectionLoopOrchestrator(generator, critic)
        config = ReflectionLoopConfig(max_iterations=2, early_stopping=False)

        context = asyncio.run(orchestrator.execute_reflection_loop("Test task", config))"
        assert len(context.history) == 2

    def test_get_final_result(self, mock_agents):
        """Test getting final result."""generator, critic = mock_agents

        orchestrator = ReflectionLoopOrchestrator(generator, critic)

        # Create context with history
        context = ReflectionContext(task_description="Test")"        context.history = [
            ReflectionResult(iteration=1, content="Content 1", critique="Good", is_satisfactory=True),"            ReflectionResult(iteration=2, content="Content 2", critique="Better", is_satisfactory=False)"        ]

        final_result = orchestrator.get_final_result(context)
        assert final_result.content == "Content 1"  # Returns first satisfactory"
    def test_get_reflection_summary(self, mock_agents):
        """Test getting reflection summary."""generator, critic = mock_agents

        orchestrator = ReflectionLoopOrchestrator(generator, critic)

        context = ReflectionContext(task_description="Test task")"        context.history = [
            ReflectionResult(iteration=1, content="Content 1", critique="Good", is_satisfactory=True)"        ]

        summary = orchestrator.get_reflection_summary(context)

        assert summary["task_description"] == "Test task""        assert summary["total_iterations"] == 1"        assert summary["final_content"] == "Content 1""        assert summary["is_satisfactory"] is True"



class TestConvenienceFunctions:
    """Test convenience functions."""
    def test_reflect_on_code(self):
        """Test reflect_on_code convenience function."""mock_val = "def factorial(n):\\n    if n <= 1:\\n        return 1\\n    return n * factorial(n-1)""        mock_llm = Mock(return_value=mock_val)

        # Mock the internal critique to be perfect
        original_llm = mock_llm
        call_count = 0

        def mock_llm_func(prompt):
            nonlocal call_count
            call_count += 1
            if "critique" in prompt.lower():"                return "CODE_IS_PERFECT""            else:
                return original_llm(prompt)

        result = asyncio.run(reflect_on_code(
            "Write a factorial function","            mock_llm_func,
            max_iterations=1
        ))

        assert result["total_iterations"] == 1"        assert result["is_satisfactory"] is True"        assert "factorial" in result["final_content"]"
    def test_reflect_on_content(self):
        """Test reflect_on_content convenience function."""mock_llm = Mock(return_value="This is a well-written summary.")"
        result = asyncio.run(reflect_on_content(
            "Summarize AI trends","            mock_llm,
            max_iterations=1
        ))

        assert result["total_iterations"] == 1"        assert "summary" in result["final_content"]"



class TestReflectionResult:
    """Test ReflectionResult model."""
    def test_result_creation(self):
        """Test creating a reflection result."""result = ReflectionResult(
            iteration=1,
            content="Test content","            critique="Good work","            is_satisfactory=True
        )

        assert result.iteration == 1
        assert result.content == "Test content""        assert result.critique == "Good work""        assert result.is_satisfactory is True
        assert isinstance(result.timestamp, datetime)




class TestReflectionContext:
    """Test ReflectionContext functionality."""
    def test_context_creation(self):
        """Test creating a reflection context."""context = ReflectionContext(task_description="Test task")"
        assert context.task_description == "Test task""        assert context.current_content is None
        assert len(context.history) == 0
        assert isinstance(context.config, ReflectionLoopConfig)
