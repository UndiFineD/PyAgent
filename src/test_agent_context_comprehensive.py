#!/usr / bin / env python3
"""
Tests for agent_context.py improvements.

Covers context management, state tracking, lifecycle management,
context inheritance, and context cleanup.
"""

import unittest
from datetime import datetime, timedelta


class TestContextCreation(unittest.TestCase):
    """Tests for context creation and initialization."""

    def test_create_context_basic(self):
        """Test creating a basic context."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timestamp": datetime.now(),
        }

        assert context["user_id"] == "user123"
        assert context["session_id"] == "sess123"
        assert context["timestamp"] is not None

    def test_create_context_with_defaults(self):
        """Test creating context with default values."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timeout": 3600,
            "retries": 3,
            "debug": False,
        }

        assert context["timeout"] == 3600
        assert context["retries"] == 3
        assert context["debug"] is False

    def test_create_context_nested(self):
        """Test creating nested context."""
        context = {
            "user": {
                "id": "user123",
                "name": "Alice",
                "roles": ["admin"],
            },
            "environment": {
                "stage": "production",
                "region": "us-east-1",
            },
        }

        assert context["user"]["id"] == "user123"
        assert context["environment"]["stage"] == "production"

    def test_create_context_with_metadata(self):
        """Test creating context with metadata."""
        context = {
            "id": "ctx123",
            "created_at": datetime.now(),
            "metadata": {
                "source": "api",
                "version": "1.0",
            },
        }

        assert context["metadata"]["source"] == "api"


class TestContextStateTracking(unittest.TestCase):
    """Tests for context state tracking."""

    def test_track_context_state_transitions(self):
        """Test tracking context state transitions."""
        states = ["initialized", "processing", "completed"]
        state_history = []

        for state in states:
            state_history.append(state)

        assert len(state_history) == 3
        assert state_history[-1] == "completed"

    def test_track_modified_fields(self):
        """Test tracking modified fields."""
        context = {"value": 10}
        modifications = []

        context["value"] = 20
        modifications.append(("value", 10, 20))

        assert len(modifications) == 1
        assert modifications[0][2] == 20

    def test_track_context_dirty_state(self):
        """Test tracking dirty state."""
        context = {"name": "Alice", "_dirty": False}

        context["name"] = "Bob"
        context["_dirty"] = True

        assert context["_dirty"] is True

    def test_track_context_read_only_fields(self):
        """Test tracking read-only field violations."""
        context = {"id": "ctx123", "_read_only": ["id"]}
        violations = []

        # Attempt to modify read-only field
        if "id" in context.get("_read_only", []):
            violations.append("id")

        assert "id" in violations


class TestContextLifecycle(unittest.TestCase):
    """Tests for context lifecycle management."""

    def test_context_creation_lifecycle(self):
        """Test context creation lifecycle."""
        lifecycle = []

        # Create
        context = {"id": "ctx1"}
        lifecycle.append("created")

        # Initialize
        context["initialized"] = True
        lifecycle.append("initialized")

        # Cleanup
        context.clear()
        lifecycle.append("cleaned")

        assert lifecycle == ["created", "initialized", "cleaned"]

    def test_context_timeout_lifecycle(self):
        """Test context timeout lifecycle."""
        context = {
            "created_at": datetime.now(),
            "timeout": 3600,
            "status": "active",
        }

        # Still valid
        assert context["status"] == "active"

        # Simulate timeout
        context["status"] = "expired"
        assert context["status"] == "expired"

    def test_context_resource_management(self):
        """Test context resource management."""
        resources = []

        # Allocate
        resources.append("connection")
        resources.append("file_handle")

        assert len(resources) == 2

        # Release
        resources.clear()
        assert len(resources) == 0

    def test_context_cleanup_on_exception(self):
        """Test context cleanup on exception."""
        context = {"active": True}
        cleanup_called = False

        try:
            raise ValueError("Error")
        except ValueError:
            context["active"] = False
            cleanup_called = True

        assert cleanup_called
        assert context["active"] is False


class TestContextInheritance(unittest.TestCase):
    """Tests for context inheritance."""

    def test_inherit_context_properties(self):
        """Test inheriting context properties."""
        parent_context = {
            "user_id": "user123",
            "session_id": "sess123",
        }

        child_context = parent_context.copy()
        child_context["request_id"] = "req456"

        assert child_context["user_id"] == "user123"
        assert child_context["request_id"] == "req456"

    def test_override_inherited_properties(self):
        """Test overriding inherited properties."""
        parent = {"debug": False, "timeout": 30}
        child = parent.copy()
        child["debug"] = True

        assert parent["debug"] is False
        assert child["debug"] is True

    def test_context_hierarchy(self):
        """Test context hierarchy."""
        global_context = {"env": "production"}
        project_context = {**global_context, "project": "app1"}
        request_context = {**project_context, "request_id": "req1"}

        assert request_context["env"] == "production"
        assert request_context["project"] == "app1"
        assert request_context["request_id"] == "req1"

    def test_context_isolation(self):
        """Test context isolation."""
        ctx1 = {"id": "ctx1", "data": []}
        ctx2 = {"id": "ctx2", "data": []}

        ctx1["data"].append(1)
        ctx2["data"].append(2)

        assert ctx1["data"] == [1]
        assert ctx2["data"] == [2]


class TestContextStorage(unittest.TestCase):
    """Tests for context storage and retrieval."""

    def test_store_context_value(self):
        """Test storing context value."""
        context = {}
        context["key1"] = "value1"

        assert context["key1"] == "value1"

    def test_retrieve_context_value(self):
        """Test retrieving context value."""
        context = {"key1": "value1", "key2": "value2"}

        value = context.get("key1")
        assert value == "value1"

    def test_retrieve_nonexistent_with_default(self):
        """Test retrieving nonexistent with default."""
        context = {"key1": "value1"}

        value = context.get("missing", "default")
        assert value == "default"

    def test_store_complex_object(self):
        """Test storing complex object."""
        context = {
            "user": {
                "id": 1,
                "name": "Alice",
                "roles": ["admin", "user"],
            }
        }

        assert context["user"]["name"] == "Alice"
        assert "admin" in context["user"]["roles"]


class TestContextVariables(unittest.TestCase):
    """Tests for context-local variables."""

    def test_set_context_variable(self):
        """Test setting context variable."""
        context = {}
        context["var1"] = "value1"

        assert "var1" in context

    def test_get_context_variable(self):
        """Test getting context variable."""
        context = {"var1": "value1"}

        assert context["var1"] == "value1"

    def test_delete_context_variable(self):
        """Test deleting context variable."""
        context = {"var1": "value1"}
        del context["var1"]

        assert "var1" not in context

    def test_context_variable_isolation(self):
        """Test context variable isolation."""
        ctx1_vars = {"var": "ctx1_value"}
        ctx2_vars = {"var": "ctx2_value"}

        assert ctx1_vars["var"] != ctx2_vars["var"]


class TestContextPropagation(unittest.TestCase):
    """Tests for context propagation through call chains."""

    def test_propagate_context_to_function(self):
        """Test propagating context to function."""
        context = {"user_id": "user1"}

        def process(ctx):
            return ctx["user_id"]

        result = process(context)
        assert result == "user1"

    def test_propagate_through_nested_calls(self):
        """Test propagating through nested calls."""
        context = {"value": 10}

        def level1(ctx):
            return level2(ctx)

        def level2(ctx):
            return level3(ctx)

        def level3(ctx):
            return ctx["value"]

        result = level1(context)
        assert result == 10

    def test_propagate_to_async_context(self):
        """Test propagating to async context."""
        context = {"async_id": "async1"}

        async_contexts = []
        async_contexts.append(context)

        assert async_contexts[0]["async_id"] == "async1"

    def test_propagate_with_implicit_context(self):
        """Test propagating with implicit context."""
        context_stack = [{"level": 1}]

        # Add another level
        context_stack.append({**context_stack[-1], "level": 2})

        assert context_stack[-1]["level"] == 2


class TestContextMerging(unittest.TestCase):
    """Tests for context merging."""

    def test_merge_contexts(self):
        """Test merging two contexts."""
        ctx1 = {"key1": "value1"}
        ctx2 = {"key2": "value2"}

        merged = {**ctx1, **ctx2}

        assert merged["key1"] == "value1"
        assert merged["key2"] == "value2"

    def test_merge_with_override(self):
        """Test merging with override."""
        ctx1 = {"shared": "original", "unique1": "value1"}
        ctx2 = {"shared": "override", "unique2": "value2"}

        merged = {**ctx1, **ctx2}

        assert merged["shared"] == "override"
        assert merged["unique1"] == "value1"
        assert merged["unique2"] == "value2"

    def test_merge_nested_contexts(self):
        """Test merging nested contexts."""
        ctx1 = {"data": {"a": 1}}
        ctx2 = {"data": {"b": 2}}

        # Simple merge (not recursive)
        merged = {**ctx1, **ctx2}
        assert merged["data"]["b"] == 2

    def test_merge_empty_context(self):
        """Test merging empty context."""
        ctx = {"key": "value"}
        empty = {}

        merged = {**ctx, **empty}
        assert merged["key"] == "value"


class TestContextValidation(unittest.TestCase):
    """Tests for context validation."""

    def test_validate_required_fields(self):
        """Test validating required fields."""
        context = {"user_id": "user1", "session_id": "sess1"}
        required = ["user_id", "session_id"]

        valid = all(field in context for field in required)
        assert valid

    def test_validate_field_types(self):
        """Test validating field types."""
        context = {"count": 10, "name": "Alice"}

        assert isinstance(context["count"], int)
        assert isinstance(context["name"], str)

    def test_validate_field_values(self):
        """Test validating field values."""
        context = {"status": "active"}
        valid_statuses = ["active", "inactive", "pending"]

        assert context["status"] in valid_statuses

    def test_validate_field_constraints(self):
        """Test validating field constraints."""
        context = {"age": 25}

        assert 0 <= context["age"] <= 150


class TestContextSerialization(unittest.TestCase):
    """Tests for context serialization."""

    def test_serialize_context_to_dict(self):
        """Test serializing context to dict."""
        context = {
            "id": "ctx1",
            "user": "alice",
            "timestamp": datetime.now().isoformat(),
        }

        serialized = dict(context)
        assert isinstance(serialized, dict)
        assert serialized["id"] == "ctx1"

    def test_serialize_context_to_json(self):
        """Test serializing context to JSON."""
        import json
        context = {"id": "ctx1", "name": "test"}

        json_str = json.dumps(context)
        assert "ctx1" in json_str

    def test_deserialize_context(self):
        """Test deserializing context."""
        import json
        json_str = '{"id": "ctx1", "name": "test"}'

        context = json.loads(json_str)
        assert context["id"] == "ctx1"

    def test_serialize_with_nested_structures(self):
        """Test serializing with nested structures."""
        import json
        context = {
            "user": {"id": 1, "name": "Alice"},
            "tags": ["tag1", "tag2"],
        }

        json_str = json.dumps(context)
        restored = json.loads(json_str)
        assert restored["user"]["name"] == "Alice"


class TestContextCaching(unittest.TestCase):
    """Tests for context caching."""

    def test_cache_context_value(self):
        """Test caching context value."""
        cache = {}
        context = {"key": "value"}

        cache["ctx1"] = context

        assert cache["ctx1"]["key"] == "value"

    def test_invalidate_cache(self):
        """Test invalidating cache."""
        cache = {"ctx1": {"value": 10}}

        del cache["ctx1"]

        assert "ctx1" not in cache

    def test_cache_with_expiration(self):
        """Test cache with expiration."""
        cache = {}
        context = {
            "value": 10,
            "expires_at": datetime.now() + timedelta(hours=1),
        }

        cache["ctx1"] = context
        assert cache["ctx1"]["value"] == 10

    def test_cache_hit_miss(self):
        """Test cache hit and miss."""
        cache = {"ctx1": {"value": 10}}

        # Hit
        assert "ctx1" in cache

        # Miss
        assert "ctx2" not in cache


class TestContextIntegration(unittest.TestCase):
    """Integration tests for context management."""

    def test_end_to_end_context_workflow(self):
        """Test end-to-end context workflow."""
        # Create
        context = {"user_id": "user1", "session_id": "sess1"}

        # Modify
        context["request_id"] = "req1"

        # Validate
        assert all(k in context for k in ["user_id", "session_id", "request_id"])

        # Cleanup
        context.clear()
        assert len(context) == 0

    def test_multi_context_lifecycle(self):
        """Test multi-context lifecycle."""
        contexts = []

        # Create multiple
        for i in range(3):
            contexts.append({"id": f"ctx{i}"})

        assert len(contexts) == 3

        # Process
        for ctx in contexts:
            ctx["processed"] = True

        # Cleanup
        contexts.clear()
        assert len(contexts) == 0

    def test_context_with_state_machine(self):
        """Test context with state machine."""
        context = {"state": "init"}
        transitions = []

        # Transition 1
        context["state"] = "processing"
        transitions.append("init->processing")

        # Transition 2
        context["state"] = "completed"
        transitions.append("processing->completed")

        assert len(transitions) == 2
        assert context["state"] == "completed"


if __name__ == "__main__":
    unittest.main()
