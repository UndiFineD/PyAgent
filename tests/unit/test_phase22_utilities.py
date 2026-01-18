"""
Phase 22 Tests: Advanced Utilities

Tests for:
1. JSONTreeUtils - Nested JSON traversal and transformation
2. DynamicImporter - Runtime import utilities
3. HTTPClient - Unified sync/async HTTP client
4. ReasoningParser - Extensible reasoning extraction framework
"""

import asyncio
import json
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# ============================================================================
# JSONTreeUtils Tests
# ============================================================================


class TestJSONTreeUtils:
    """Tests for JSONTreeUtils module."""
    
    def test_json_iter_leaves_dict(self):
        """Test iterating leaves in a nested dict."""
        from src.core.base.utils.JSONTreeUtils import json_iter_leaves
        
        data = {"a": 1, "b": {"c": 2, "d": 3}}
        leaves = list(json_iter_leaves(data))
        
        assert sorted(leaves) == [1, 2, 3]
    
    def test_json_iter_leaves_list(self):
        """Test iterating leaves in nested lists."""
        from src.core.base.utils.JSONTreeUtils import json_iter_leaves
        
        data = [1, [2, 3], [[4, 5]]]
        leaves = list(json_iter_leaves(data))
        
        assert leaves == [1, 2, 3, 4, 5]
    
    def test_json_iter_leaves_mixed(self):
        """Test iterating leaves in mixed structure."""
        from src.core.base.utils.JSONTreeUtils import json_iter_leaves
        
        data = {"a": [1, 2], "b": {"c": [3, 4]}}
        leaves = list(json_iter_leaves(data))
        
        assert sorted(leaves) == [1, 2, 3, 4]
    
    def test_json_iter_leaves_with_path(self):
        """Test iterating leaves with their paths."""
        from src.core.base.utils.JSONTreeUtils import json_iter_leaves_with_path
        
        data = {"a": {"b": 1}, "c": 2}
        leaves = list(json_iter_leaves_with_path(data))
        
        paths = [path for path, _ in leaves]
        assert "a.b" in paths
        assert "c" in paths
    
    def test_json_map_leaves(self):
        """Test mapping function over leaves."""
        from src.core.base.utils.JSONTreeUtils import json_map_leaves
        
        data = {"a": 1, "b": {"c": 2}}
        result = json_map_leaves(lambda x: x * 2, data)
        
        assert result == {"a": 2, "b": {"c": 4}}
    
    def test_json_map_leaves_preserves_structure(self):
        """Test that mapping preserves structure."""
        from src.core.base.utils.JSONTreeUtils import json_map_leaves
        
        data = [1, [2, 3], {"a": 4}]
        result = json_map_leaves(str, data)
        
        assert result == ["1", ["2", "3"], {"a": "4"}]
    
    def test_json_reduce_leaves(self):
        """Test reducing leaves to single value."""
        from src.core.base.utils.JSONTreeUtils import json_reduce_leaves
        
        data = {"a": 1, "b": {"c": 2, "d": 3}}
        result = json_reduce_leaves(lambda a, b: a + b, data)
        
        assert result == 6
    
    def test_json_reduce_leaves_with_initial(self):
        """Test reducing with initial value."""
        from src.core.base.utils.JSONTreeUtils import json_reduce_leaves
        
        data = [1, 2, 3]
        result = json_reduce_leaves(lambda a, b: a + b, data, 10)
        
        assert result == 16
    
    def test_json_count_leaves(self):
        """Test counting leaves."""
        from src.core.base.utils.JSONTreeUtils import json_count_leaves
        
        data = {"a": 1, "b": {"c": 2, "d": {"e": 3}}, "f": [4, 5]}
        count = json_count_leaves(data)
        
        assert count == 5
    
    def test_json_depth(self):
        """Test calculating depth."""
        from src.core.base.utils.JSONTreeUtils import json_depth
        
        assert json_depth("leaf") == 0
        assert json_depth({"a": 1}) == 1
        assert json_depth({"a": {"b": 1}}) == 2
        assert json_depth({"a": {"b": {"c": 1}}}) == 3
    
    def test_json_flatten(self):
        """Test flattening nested structure."""
        from src.core.base.utils.JSONTreeUtils import json_flatten
        
        data = {"a": {"b": 1, "c": 2}, "d": 3}
        flat = json_flatten(data)
        
        assert flat == {"a.b": 1, "a.c": 2, "d": 3}
    
    def test_json_flatten_with_arrays(self):
        """Test flattening with arrays."""
        from src.core.base.utils.JSONTreeUtils import json_flatten
        
        data = {"a": [1, 2, 3]}
        flat = json_flatten(data)
        
        assert flat == {"a[0]": 1, "a[1]": 2, "a[2]": 3}
    
    def test_json_unflatten(self):
        """Test unflattening to nested structure."""
        from src.core.base.utils.JSONTreeUtils import json_unflatten
        
        flat = {"a.b": 1, "a.c": 2, "d": 3}
        nested = json_unflatten(flat)
        
        assert nested == {"a": {"b": 1, "c": 2}, "d": 3}
    
    def test_json_get_path(self):
        """Test getting value by path."""
        from src.core.base.utils.JSONTreeUtils import json_get_path
        
        data = {"a": {"b": {"c": 42}}}
        
        assert json_get_path(data, "a.b.c") == 42
        assert json_get_path(data, "a.b") == {"c": 42}
        assert json_get_path(data, "x.y.z", "default") == "default"
    
    def test_json_get_path_with_arrays(self):
        """Test getting value with array indices."""
        from src.core.base.utils.JSONTreeUtils import json_get_path
        
        data = {"a": [1, 2, 3]}
        
        assert json_get_path(data, "a[1]") == 2
    
    def test_json_set_path(self):
        """Test setting value by path."""
        from src.core.base.utils.JSONTreeUtils import json_set_path
        
        data = {"a": {}}
        json_set_path(data, "a.b.c", 42)
        
        assert data == {"a": {"b": {"c": 42}}}
    
    def test_json_filter_leaves(self):
        """Test filtering leaves by predicate."""
        from src.core.base.utils.JSONTreeUtils import json_filter_leaves
        
        data = {"a": 1, "b": 2, "c": 3, "d": 4}
        filtered = json_filter_leaves(lambda x: x > 2, data)
        
        assert filtered == {"c": 3, "d": 4}
    
    def test_json_validate_leaves(self):
        """Test validating all leaves."""
        from src.core.base.utils.JSONTreeUtils import json_validate_leaves
        
        data = {"a": 1, "b": 2, "c": 3}
        
        assert json_validate_leaves(lambda x: isinstance(x, int), data) is True
        assert json_validate_leaves(lambda x: x > 0, data) is True
        assert json_validate_leaves(lambda x: x > 2, data) is False
    
    def test_json_find_leaves(self):
        """Test finding leaves matching predicate."""
        from src.core.base.utils.JSONTreeUtils import json_find_leaves
        
        data = {"a": 1, "b": {"c": 10}, "d": 5}
        matches = json_find_leaves(lambda x: x >= 5, data)
        
        paths = [path for path, _ in matches]
        assert "b.c" in paths
        assert "d" in paths


# ============================================================================
# DynamicImporter Tests
# ============================================================================


class TestDynamicImporter:
    """Tests for DynamicImporter module."""
    
    def test_resolve_obj_by_qualname_module(self):
        """Test resolving a module."""
        from src.core.base.utils.DynamicImporter import resolve_obj_by_qualname
        
        json_mod = resolve_obj_by_qualname("json")
        assert json_mod is json
    
    def test_resolve_obj_by_qualname_class(self):
        """Test resolving a class."""
        from src.core.base.utils.DynamicImporter import resolve_obj_by_qualname
        from collections import OrderedDict
        
        cls = resolve_obj_by_qualname("collections.OrderedDict")
        assert cls is OrderedDict
    
    def test_resolve_obj_by_qualname_function(self):
        """Test resolving a function."""
        from src.core.base.utils.DynamicImporter import resolve_obj_by_qualname
        
        loads = resolve_obj_by_qualname("json.loads")
        assert loads is json.loads
    
    def test_placeholder_module(self):
        """Test PlaceholderModule behavior."""
        from src.core.base.utils.DynamicImporter import PlaceholderModule
        
        placeholder = PlaceholderModule(
            "fake_module",
            install_hint="pip install fake_module"
        )
        
        assert placeholder.is_placeholder is True
        
        with pytest.raises(ImportError) as exc_info:
            placeholder.some_attr
        
        assert "fake_module" in str(exc_info.value)
        assert "pip install" in str(exc_info.value)
    
    def test_lazy_import_available(self):
        """Test lazy import of available module."""
        from src.core.base.utils.DynamicImporter import lazy_import
        
        result = lazy_import("json")
        assert result is json
    
    def test_lazy_import_unavailable(self):
        """Test lazy import of unavailable module."""
        from src.core.base.utils.DynamicImporter import lazy_import, PlaceholderModule
        
        result = lazy_import("nonexistent_module_xyz")
        assert isinstance(result, PlaceholderModule)
    
    def test_safe_import_available(self):
        """Test safe import of available module."""
        from src.core.base.utils.DynamicImporter import safe_import
        
        result = safe_import("json")
        assert result is json
    
    def test_safe_import_unavailable(self):
        """Test safe import of unavailable module."""
        from src.core.base.utils.DynamicImporter import safe_import
        
        result = safe_import("nonexistent_module_xyz", default="fallback")
        assert result == "fallback"
    
    def test_lazy_module_registry(self):
        """Test LazyModuleRegistry."""
        from src.core.base.utils.DynamicImporter import LazyModuleRegistry
        
        registry = LazyModuleRegistry()
        registry.register("my_json", "json")
        
        assert "my_json" in registry
        assert not registry.is_loaded("my_json")
        
        result = registry.get("my_json")
        assert result is json
        assert registry.is_loaded("my_json")
    
    def test_lazy_module_registry_class(self):
        """Test LazyModuleRegistry with class."""
        from src.core.base.utils.DynamicImporter import LazyModuleRegistry
        
        registry = LazyModuleRegistry()
        registry.register("ordered_dict", "collections.OrderedDict")
        
        from collections import OrderedDict
        result = registry.get("ordered_dict")
        assert result is OrderedDict
    
    def test_is_module_available(self):
        """Test checking module availability."""
        from src.core.base.utils.DynamicImporter import is_module_available
        
        assert is_module_available("json") is True
        assert is_module_available("nonexistent_xyz") is False
    
    def test_get_module_version(self):
        """Test getting module version."""
        from src.core.base.utils.DynamicImporter import get_module_version
        
        # pytest has a version
        version = get_module_version("pytest")
        assert version is not None
        
        # os doesn't have a __version__ attribute
        version = get_module_version("os")
        assert version is None
    
    def test_require_module(self):
        """Test requiring a module."""
        from src.core.base.utils.DynamicImporter import require_module
        
        result = require_module("json")
        assert result is json
        
        with pytest.raises(ImportError):
            require_module("nonexistent_xyz")


# ============================================================================
# HTTPClient Tests
# ============================================================================


class TestHTTPClient:
    """Tests for HTTPClient module."""
    
    def test_http_connection_init(self):
        """Test HTTPConnection initialization."""
        from src.infrastructure.network.HTTPClient import HTTPConnection
        
        conn = HTTPConnection()
        assert conn.reuse_client is True
        assert conn.default_timeout == 30.0
        assert "PyAgent" in conn.user_agent
    
    def test_http_connection_custom_config(self):
        """Test HTTPConnection with custom config."""
        from src.infrastructure.network.HTTPClient import HTTPConnection
        
        conn = HTTPConnection(
            reuse_client=False,
            default_timeout=60.0,
            user_agent="CustomAgent/1.0"
        )
        
        assert conn.reuse_client is False
        assert conn.default_timeout == 60.0
        assert conn.user_agent == "CustomAgent/1.0"
    
    def test_url_validation(self):
        """Test URL validation."""
        from src.infrastructure.network.HTTPClient import HTTPConnection
        
        conn = HTTPConnection()
        
        # Valid URLs should not raise
        conn._validate_http_url("http://example.com")
        conn._validate_http_url("https://example.com")
        
        # Invalid URLs should raise
        with pytest.raises(ValueError):
            conn._validate_http_url("ftp://example.com")
        
        with pytest.raises(ValueError):
            conn._validate_http_url("not-a-url")
    
    def test_headers(self):
        """Test header generation."""
        from src.infrastructure.network.HTTPClient import HTTPConnection
        
        conn = HTTPConnection(user_agent="TestAgent/1.0")
        headers = conn._headers(Authorization="Bearer token")
        
        assert headers["User-Agent"] == "TestAgent/1.0"
        assert headers["Authorization"] == "Bearer token"
    
    def test_retryable_client_init(self):
        """Test RetryableHTTPClient initialization."""
        from src.infrastructure.network.HTTPClient import RetryableHTTPClient
        
        client = RetryableHTTPClient(
            max_retries=5,
            retry_delay=0.5,
            retry_backoff=1.5
        )
        
        assert client.max_retries == 5
        assert client.retry_delay == 0.5
        assert client.retry_backoff == 1.5
    
    def test_context_manager(self):
        """Test context manager protocol."""
        from src.infrastructure.network.HTTPClient import HTTPClient
        
        with HTTPClient() as client:
            assert client._sync_client is None  # Not created until used


# ============================================================================
# ReasoningParser Tests
# ============================================================================


class TestReasoningParser:
    """Tests for ReasoningParser module."""
    
    def test_reasoning_result_dataclass(self):
        """Test ReasoningResult dataclass."""
        from src.core.base.parsers.ReasoningParser import ReasoningResult
        
        result = ReasoningResult(
            reasoning="I think...",
            content="The answer is 42"
        )
        
        assert result.reasoning == "I think..."
        assert result.content == "The answer is 42"
        assert result.is_complete is True
    
    def test_xml_parser_extract(self):
        """Test XML reasoning parser extraction."""
        from src.core.base.parsers.ReasoningParser import XMLReasoningParser
        
        parser = XMLReasoningParser()
        output = "<think>Let me analyze...</think>The answer is 42."
        
        result = parser.extract_reasoning(output)
        
        assert result.reasoning == "Let me analyze..."
        assert result.content == "The answer is 42."
    
    def test_xml_parser_no_reasoning(self):
        """Test XML parser with no reasoning block."""
        from src.core.base.parsers.ReasoningParser import XMLReasoningParser
        
        parser = XMLReasoningParser()
        output = "The answer is 42."
        
        result = parser.extract_reasoning(output)
        
        assert result.reasoning is None
        assert result.content == "The answer is 42."
    
    def test_xml_parser_multiple_blocks(self):
        """Test XML parser with multiple think blocks."""
        from src.core.base.parsers.ReasoningParser import XMLReasoningParser
        
        parser = XMLReasoningParser()
        output = "<think>First thought</think>Middle<think>Second thought</think>End"
        
        result = parser.extract_reasoning(output)
        
        assert "First thought" in result.reasoning
        assert "Second thought" in result.reasoning
        assert "Middle" in result.content
    
    def test_xml_parser_custom_tags(self):
        """Test XML parser with custom tags."""
        from src.core.base.parsers.ReasoningParser import XMLReasoningParser
        
        parser = XMLReasoningParser(start_tag="<reasoning>", end_tag="</reasoning>")
        output = "<reasoning>Analysis...</reasoning>Result"
        
        result = parser.extract_reasoning(output)
        
        assert result.reasoning == "Analysis..."
        assert result.content == "Result"
    
    def test_json_parser_extract(self):
        """Test JSON reasoning parser extraction."""
        from src.core.base.parsers.ReasoningParser import JSONReasoningParser
        
        parser = JSONReasoningParser()
        output = '{"reasoning": "I analyzed...", "answer": "42"}'
        
        result = parser.extract_reasoning(output)
        
        assert result.reasoning == "I analyzed..."
        assert result.content == "42"
    
    def test_json_parser_invalid_json(self):
        """Test JSON parser with invalid JSON."""
        from src.core.base.parsers.ReasoningParser import JSONReasoningParser
        
        parser = JSONReasoningParser()
        output = "Not valid JSON"
        
        result = parser.extract_reasoning(output)
        
        assert result.content == "Not valid JSON"
    
    def test_markdown_parser_extract(self):
        """Test Markdown reasoning parser extraction."""
        from src.core.base.parsers.ReasoningParser import MarkdownReasoningParser
        
        parser = MarkdownReasoningParser()
        output = "```thinking\nAnalysis here\n```\nThe answer is 42."
        
        result = parser.extract_reasoning(output)
        
        assert "Analysis here" in result.reasoning
        assert "42" in result.content
    
    def test_identity_parser(self):
        """Test identity (no-op) parser."""
        from src.core.base.parsers.ReasoningParser import IdentityReasoningParser
        
        parser = IdentityReasoningParser()
        output = "Some output"
        
        result = parser.extract_reasoning(output)
        
        assert result.reasoning is None
        assert result.content == "Some output"
    
    def test_parser_manager_get_parser(self):
        """Test ReasoningParserManager.get_reasoning_parser."""
        from src.core.base.parsers.ReasoningParser import (
            ReasoningParserManager,
            XMLReasoningParser,
            JSONReasoningParser,
        )
        
        xml_cls = ReasoningParserManager.get_reasoning_parser("xml")
        assert xml_cls is XMLReasoningParser
        
        json_cls = ReasoningParserManager.get_reasoning_parser("json")
        assert json_cls is JSONReasoningParser
    
    def test_parser_manager_list_registered(self):
        """Test listing registered parsers."""
        from src.core.base.parsers.ReasoningParser import ReasoningParserManager
        
        registered = ReasoningParserManager.list_registered()
        
        assert "xml" in registered
        assert "json" in registered
        assert "markdown" in registered
        assert "identity" in registered
    
    def test_parser_manager_create_parser(self):
        """Test creating parser instance via manager."""
        from src.core.base.parsers.ReasoningParser import (
            ReasoningParserManager,
            XMLReasoningParser,
        )
        
        parser = ReasoningParserManager.create_parser("xml")
        assert isinstance(parser, XMLReasoningParser)
    
    def test_parser_decorator(self):
        """Test @reasoning_parser decorator."""
        from src.core.base.parsers.ReasoningParser import (
            reasoning_parser,
            ReasoningParser,
            ReasoningParserManager,
            ReasoningResult,
            StreamingReasoningState,
        )
        
        @reasoning_parser("test_custom")
        class TestCustomParser(ReasoningParser):
            name = "test_custom"
            
            def is_reasoning_end(self, input_ids):
                return True
            
            def extract_content_ids(self, input_ids):
                return input_ids
            
            def extract_reasoning(self, model_output, request=None):
                return ReasoningResult(content=model_output)
            
            def extract_reasoning_streaming(
                self, prev, curr, delta, prev_ids, curr_ids, delta_ids, state=None
            ):
                if state is None:
                    state = StreamingReasoningState()
                return ReasoningResult(content=delta), state
        
        # Should now be registered
        assert "test_custom" in ReasoningParserManager.list_registered()
    
    def test_convenience_extract_reasoning(self):
        """Test convenience function."""
        from src.core.base.parsers.ReasoningParser import extract_reasoning
        
        output = "<think>Thinking...</think>Answer"
        result = extract_reasoning(output, parser_name="xml")
        
        assert result.reasoning == "Thinking..."
        assert result.content == "Answer"
    
    def test_streaming_state(self):
        """Test StreamingReasoningState."""
        from src.core.base.parsers.ReasoningParser import StreamingReasoningState
        
        state = StreamingReasoningState()
        assert state.accumulated_text == ""
        assert state.in_reasoning is False
        assert state.reasoning_complete is False


# ============================================================================
# Integration Tests
# ============================================================================


class TestPhase22Integration:
    """Integration tests for Phase 22 components."""
    
    def test_jsontree_with_reasoning_output(self):
        """Test JSONTree with parsed reasoning output."""
        from src.core.base.utils.JSONTreeUtils import json_flatten, json_iter_leaves
        from src.core.base.parsers.ReasoningParser import extract_reasoning
        
        # Simulate model output in JSON format
        model_output = '{"reasoning": "Step 1: analyze\nStep 2: compute", "answer": "42"}'
        result = extract_reasoning(model_output, parser_name="json")
        
        # Create structured output
        structured = {
            "reasoning": result.reasoning,
            "content": result.content,
            "metadata": {"parser": "json", "complete": True}
        }
        
        # Flatten for logging
        flat = json_flatten(structured)
        assert "reasoning" in flat
        assert "content" in flat
        assert "metadata.parser" in flat
    
    def test_dynamic_import_parser(self):
        """Test dynamically importing a parser."""
        from src.core.base.utils.DynamicImporter import resolve_obj_by_qualname
        
        # Resolve XMLReasoningParser dynamically
        parser_cls = resolve_obj_by_qualname(
            "src.core.base.parsers.ReasoningParser.XMLReasoningParser"
        )
        
        parser = parser_cls()
        result = parser.extract_reasoning("<think>Test</think>Answer")
        
        assert result.reasoning == "Test"
        assert result.content == "Answer"
    
    def test_lazy_registry_with_parsers(self):
        """Test lazy registry pattern with parsers."""
        from src.core.base.utils.DynamicImporter import LazyModuleRegistry
        
        registry = LazyModuleRegistry()
        registry.register_many({
            "xml": "src.core.base.parsers.ReasoningParser.XMLReasoningParser",
            "json": "src.core.base.parsers.ReasoningParser.JSONReasoningParser",
        })
        
        # Not loaded yet
        assert not registry.is_loaded("xml")
        
        # Load on access
        xml_cls = registry.get("xml")
        assert registry.is_loaded("xml")
        
        # Use the parser
        parser = xml_cls()
        result = parser.extract_reasoning("<think>Lazy</think>Loaded")
        assert result.reasoning == "Lazy"


# ============================================================================
# Run Tests
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
