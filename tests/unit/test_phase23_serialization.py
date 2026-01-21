"""
Phase 23: Advanced Serialization & Validation Tests

Tests for:
- ZeroCopySerializer: Zero-copy msgpack serialization
- TensorSchema: Tensor shape validation with symbolic dimensions
- ImmutableCollections: ConstantList, ConstantDict, FrozenDict
- CpuGpuBuffer: CPU-GPU tensor transfers
- LogitsProcessor: Token filtering pipeline
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# ==============================================================================
# TensorSchema Tests
# ==============================================================================

class TestTensorShape:
    """Tests for TensorShape class."""

    def test_basic_shape(self):
        """Test basic shape creation."""
        from src.core.base.logic.validation.tensor_schema import TensorShape

        shape = TensorShape(32, 768)
        assert len(shape) == 2
        assert shape.dims == (32, 768)

    def test_symbolic_dimensions(self):
        """Test symbolic dimension names."""
        from src.core.base.logic.validation.tensor_schema import TensorShape

        shape = TensorShape("batch", "seq_len", 768)
        assert shape.dims == ("batch", "seq_len", 768)

    def test_resolve_bindings(self):
        """Test resolving symbolic dimensions."""
        from src.core.base.logic.validation.tensor_schema import TensorShape

        shape = TensorShape("batch", "seq_len", 768)
        resolved = shape.resolve(batch=32, seq_len=512)
        assert resolved == (32, 512, 768)

    def test_partial_resolve(self):
        """Test partial resolution."""
        from src.core.base.logic.validation.tensor_schema import TensorShape

        shape = TensorShape("batch", "seq_len", 768)
        resolved = shape.resolve(batch=32)
        assert resolved == (32, "seq_len", 768)

    def test_matches_exact(self):
        """Test exact shape matching."""
        from src.core.base.logic.validation.tensor_schema import TensorShape

        shape = TensorShape(32, 512, 768)
        assert shape.matches((32, 512, 768))
        assert not shape.matches((32, 256, 768))

    def test_matches_with_bindings(self):
        """Test matching with bindings."""
        from src.core.base.logic.validation.tensor_schema import TensorShape

        shape = TensorShape("batch", 512, 768)
        assert shape.matches((32, 512, 768), batch=32)

    def test_dynamic_dimension(self):
        """Test dynamic dimensions."""
        from src.core.base.logic.validation.tensor_schema import TensorShape, DynamicDim

        shape = TensorShape("batch", DynamicDim("seq_len"), 768)
        assert "seq_len" in shape.dynamic_dims


class TestTensorSchema:
    """Tests for TensorSchema class."""

    def test_schema_creation(self):
        """Test schema with multiple fields."""
        from src.core.base.logic.validation.tensor_schema import TensorSchema, TensorShape

        schema = TensorSchema(
            input_ids=TensorShape("batch", "seq_len"),
            hidden_states=TensorShape("batch", "seq_len", 768),
        )
        assert "input_ids" in schema.fields
        assert "hidden_states" in schema.fields

    def test_schema_from_tuples(self):
        """Test schema creation from tuples."""
        from src.core.base.logic.validation.tensor_schema import TensorSchema

        schema = TensorSchema(
            input_ids=("batch", "seq_len"),
            mask=("batch", "seq_len"),
        )
        assert len(schema.fields) == 2


# ==============================================================================
# ImmutableCollections Tests
# ==============================================================================

class TestConstantList:
    """Tests for ConstantList class."""

    def test_read_access(self):
        """Test read operations."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        data = [1, 2, 3, 4, 5]
        const = ConstantList(data)

        assert const[0] == 1
        assert const[-1] == 5
        assert len(const) == 5
        assert 3 in const

    def test_iteration(self):
        """Test iteration."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        data = [1, 2, 3]
        const = ConstantList(data)

        assert list(const) == [1, 2, 3]
        assert list(reversed(const)) == [3, 2, 1]

    def test_append_blocked(self):
        """Test that append is blocked."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        const = ConstantList([1, 2, 3])
        with pytest.raises(TypeError, match="Cannot append"):
            const.append(4)

    def test_extend_blocked(self):
        """Test that extend is blocked."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        const = ConstantList([1, 2, 3])
        with pytest.raises(TypeError, match="Cannot extend"):
            const.extend([4, 5])

    def test_setitem_blocked(self):
        """Test that setitem is blocked."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        const = ConstantList([1, 2, 3])
        with pytest.raises(TypeError, match="Cannot set item"):
            const[0] = 100

    def test_delitem_blocked(self):
        """Test that delitem is blocked."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        const = ConstantList([1, 2, 3])
        with pytest.raises(TypeError, match="Cannot delete"):
            del const[0]

    def test_copy_returns_mutable(self):
        """Test that copy returns mutable list."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        const = ConstantList([1, 2, 3])
        mutable = const.copy()
        mutable.append(4)
        assert len(mutable) == 4
        assert len(const) == 3

    def test_index_and_count(self):
        """Test index and count methods."""
        from src.core.base.logic.structures.immutable_collections import ConstantList

        const = ConstantList([1, 2, 2, 3])
        assert const.index(2) == 1
        assert const.count(2) == 2


class TestConstantDict:
    """Tests for ConstantDict class."""

    def test_read_access(self):
        """Test read operations."""
        from src.core.base.logic.structures.immutable_collections import ConstantDict

        data = {"a": 1, "b": 2}
        const = ConstantDict(data)

        assert const["a"] == 1
        assert len(const) == 2
        assert "a" in const

    def test_setitem_blocked(self):
        """Test that setitem is blocked."""
        from src.core.base.logic.structures.immutable_collections import ConstantDict

        const = ConstantDict({"a": 1})
        with pytest.raises(TypeError, match="Cannot set item"):
            const["b"] = 2

    def test_pop_blocked(self):
        """Test that pop is blocked."""
        from src.core.base.logic.structures.immutable_collections import ConstantDict

        const = ConstantDict({"a": 1})
        with pytest.raises(TypeError, match="Cannot pop"):
            const.pop("a")

    def test_keys_values_items(self):
        """Test view methods."""
        from src.core.base.logic.structures.immutable_collections import ConstantDict

        const = ConstantDict({"a": 1, "b": 2})
        assert set(const.keys()) == {"a", "b"}
        assert set(const.values()) == {1, 2}
        assert set(const.items()) == {("a", 1), ("b", 2)}


class TestFrozenDict:
    """Tests for FrozenDict class."""

    def test_hashable(self):
        """Test that FrozenDict is hashable."""
        from src.core.base.logic.structures.immutable_collections import FrozenDict

        fd = FrozenDict({"a": 1, "b": 2})
        hash_val = hash(fd)
        assert isinstance(hash_val, int)

    def test_as_dict_key(self):
        """Test using as dictionary key."""
        from src.core.base.logic.structures.immutable_collections import FrozenDict

        fd = FrozenDict({"x": 1})
        cache = {fd: "value"}
        assert cache[fd] == "value"

    def test_equality(self):
        """Test equality."""
        from src.core.base.logic.structures.immutable_collections import FrozenDict

        fd1 = FrozenDict({"a": 1})
        fd2 = FrozenDict({"a": 1})
        fd3 = FrozenDict({"a": 2})

        assert fd1 == fd2
        assert fd1 != fd3
        assert fd1 == {"a": 1}

    def test_setitem_blocked(self):
        """Test that setitem is blocked."""
        from src.core.base.logic.structures.immutable_collections import FrozenDict

        fd = FrozenDict({"a": 1})
        with pytest.raises(TypeError):
            fd["b"] = 2


class TestAsConstant:
    """Tests for as_constant helper."""

    def test_wrap_list(self):
        """Test wrapping list."""
        from src.core.base.logic.structures.immutable_collections import as_constant, ConstantList

        result = as_constant([1, 2, 3])
        assert isinstance(result, ConstantList)

    def test_wrap_dict(self):
        """Test wrapping dict."""
        from src.core.base.logic.structures.immutable_collections import as_constant, ConstantDict

        result = as_constant({"a": 1})
        assert isinstance(result, ConstantDict)

    def test_wrap_invalid(self):
        """Test wrapping invalid type."""
        from src.core.base.logic.structures.immutable_collections import as_constant

        with pytest.raises(TypeError):
            as_constant("string")


# ==============================================================================
# LogitsProcessor Tests
# ==============================================================================

class TestLogitsProcessorList:
    """Tests for LogitsProcessorList class."""

    def test_empty_list(self):
        """Test empty processor list."""
        from src.core.base.logic.processing.logits_processor import LogitsProcessorList

        processors = LogitsProcessorList()
        assert len(processors) == 0

    def test_append(self):
        """Test appending processors."""
        from src.core.base.logic.processing.logits_processor import (
            LogitsProcessorList, TemperatureProcessor
        )

        processors = LogitsProcessorList()
        processors.append(TemperatureProcessor(0.7))
        assert len(processors) == 1


class TestTemperatureProcessor:
    """Tests for TemperatureProcessor."""

    def test_temperature_scaling(self):
        """Test temperature scaling."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import TemperatureProcessor

        processor = TemperatureProcessor(0.5)
        logits = torch.tensor([1.0, 2.0, 3.0])
        result = processor([], logits)

        expected = logits / 0.5
        assert torch.allclose(result, expected)

    def test_temperature_one_unchanged(self):
        """Test temperature=1 returns unchanged."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import TemperatureProcessor

        processor = TemperatureProcessor(1.0)
        logits = torch.tensor([1.0, 2.0, 3.0])
        result = processor([], logits)

        assert torch.equal(result, logits)

    def test_invalid_temperature(self):
        """Test invalid temperature."""
        from src.core.base.logic.processing.logits_processor import TemperatureProcessor

        with pytest.raises(ValueError):
            TemperatureProcessor(0)
        with pytest.raises(ValueError):
            TemperatureProcessor(-1)


class TestTopKProcessor:
    """Tests for TopKProcessor."""

    def test_top_k_filtering(self):
        """Test top-k filtering."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import TopKProcessor

        processor = TopKProcessor(2)
        logits = torch.tensor([1.0, 3.0, 2.0, 0.5])
        result = processor([], logits)

        # Only top 2 (indices 1, 2) should be kept
        assert result[1] == 3.0  # Highest kept
        assert result[2] == 2.0  # Second highest kept
        assert result[0] == float("-inf")  # Filtered
        assert result[3] == float("-inf")  # Filtered

    def test_top_k_larger_than_vocab(self):
        """Test top-k larger than vocab size."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import TopKProcessor

        processor = TopKProcessor(100)
        logits = torch.tensor([1.0, 2.0, 3.0])
        result = processor([], logits)

        assert torch.equal(result, logits)


class TestTopPProcessor:
    """Tests for TopPProcessor."""

    def test_top_p_filtering(self):
        """Test nucleus sampling."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import TopPProcessor

        processor = TopPProcessor(0.9)
        logits = torch.tensor([1.0, 5.0, 0.5, 0.1])
        result = processor([], logits)

        # At least one token should be kept
        assert not torch.all(result == float("-inf"))

    def test_top_p_one_unchanged(self):
        """Test top_p=1 returns unchanged."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import TopPProcessor

        processor = TopPProcessor(1.0)
        logits = torch.tensor([1.0, 2.0, 3.0])
        result = processor([], logits)

        assert torch.equal(result, logits)


class TestRepetitionPenaltyProcessor:
    """Tests for RepetitionPenaltyProcessor."""

    def test_repetition_penalty(self):
        """Test repetition penalty application."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import RepetitionPenaltyProcessor

        processor = RepetitionPenaltyProcessor(1.5)
        logits = torch.tensor([1.0, 2.0, 3.0])
        input_ids = [0, 1]  # Tokens 0 and 1 have appeared

        result = processor(input_ids, logits)

        assert result[0] < logits[0]  # Penalized
        assert result[1] < logits[1]  # Penalized
        assert result[2] == logits[2]  # Unchanged

    def test_penalty_one_unchanged(self):
        """Test penalty=1 returns unchanged."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import RepetitionPenaltyProcessor

        processor = RepetitionPenaltyProcessor(1.0)
        logits = torch.tensor([1.0, 2.0, 3.0])
        result = processor([0, 1], logits)

        assert torch.equal(result, logits)


class TestNoBadWordsProcessor:
    """Tests for NoBadWordsProcessor."""

    def test_single_token_blocking(self):
        """Test single token bad words."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import NoBadWordsProcessor

        processor = NoBadWordsProcessor([[1], [3]])
        logits = torch.tensor([0.0, 1.0, 2.0, 3.0])

        result = processor([], logits)

        assert result[1] == float("-inf")  # Blocked
        assert result[3] == float("-inf")  # Blocked
        assert result[0] == 0.0  # Unchanged
        assert result[2] == 2.0  # Unchanged

    def test_multi_token_sequence(self):
        """Test multi-token bad word sequences."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import NoBadWordsProcessor

        processor = NoBadWordsProcessor([[1, 2, 3]])
        logits = torch.tensor([0.0, 1.0, 2.0, 3.0, 4.0])

        # Prefix [1, 2] present - should block token 3
        result = processor([1, 2], logits)
        assert result[3] == float("-inf")

        # Different prefix - should not block
        result2 = processor([0, 1], logits)
        assert result2[3] == 3.0


class TestMinLengthProcessor:
    """Tests for MinLengthProcessor."""

    def test_blocks_eos_before_min_length(self):
        """Test EOS blocking before min length."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import MinLengthProcessor

        processor = MinLengthProcessor(min_length=5, eos_token_id=2)
        logits = torch.tensor([1.0, 2.0, 3.0, 4.0])

        # Length 3 < min_length 5
        result = processor([0, 1, 0], logits)
        assert result[2] == float("-inf")

    def test_allows_eos_after_min_length(self):
        """Test EOS allowed after min length."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import MinLengthProcessor

        processor = MinLengthProcessor(min_length=3, eos_token_id=2)
        logits = torch.tensor([1.0, 2.0, 3.0, 4.0])

        # Length 5 >= min_length 3
        result = processor([0, 1, 0, 1, 0], logits)
        assert result[2] == 3.0  # Unchanged


class TestCreateProcessorChain:
    """Tests for create_processor_chain helper."""

    def test_empty_chain(self):
        """Test creating empty chain."""
        from src.core.base.logic.processing.logits_processor import create_processor_chain

        chain = create_processor_chain()
        assert len(chain) == 0

    def test_full_chain(self):
        """Test creating full chain."""
        from src.core.base.logic.processing.logits_processor import create_processor_chain

        chain = create_processor_chain(
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2,
        )
        assert len(chain) == 4


# ==============================================================================
# ZeroCopySerializer Tests (if msgspec available)
# ==============================================================================

class TestZeroCopySerializer:
    """Tests for ZeroCopySerializer (requires msgspec)."""

    def test_msgspec_available_check(self):
        """Test MSGSPEC_AVAILABLE flag."""
        from src.infrastructure.storage.serialization.zero_copy_serializer import MSGSPEC_AVAILABLE
        # Just check it's a boolean
        assert isinstance(MSGSPEC_AVAILABLE, bool)

    @pytest.mark.skipif(
        not pytest.importorskip("msgspec", reason="msgspec not installed"),
        reason="msgspec not available"
    )
    def test_encode_simple_dict(self):
        """Test encoding simple dictionary."""
        msgspec = pytest.importorskip("msgspec")
        from src.infrastructure.storage.serialization.zero_copy_serializer import ZeroCopyEncoder

        encoder = ZeroCopyEncoder()
        data = {"key": "value", "number": 42}
        buffers = encoder.encode(data)

        assert len(buffers) >= 1
        assert isinstance(buffers[0], (bytes, bytearray))

    @pytest.mark.skipif(
        not pytest.importorskip("msgspec", reason="msgspec not installed"),
        reason="msgspec not available"
    )
    def test_encode_decode_roundtrip(self):
        """Test encode/decode roundtrip."""
        msgspec = pytest.importorskip("msgspec")
        from src.infrastructure.storage.serialization.zero_copy_serializer import (
            ZeroCopyEncoder, ZeroCopyDecoder
        )

        encoder = ZeroCopyEncoder()
        decoder = ZeroCopyDecoder()

        data = {"items": [1, 2, 3], "nested": {"a": 1}}
        buffers = encoder.encode(data)
        result = decoder.decode(buffers)

        assert result == data


# ==============================================================================
# Integration Tests
# ==============================================================================

class TestPhase23Integration:
    """Integration tests for Phase 23 components."""

    def test_immutable_in_schema(self):
        """Test using immutable collections in validation."""
        from src.core.base.logic.structures.immutable_collections import ConstantList
        from src.core.base.logic.validation.tensor_schema import TensorShape

        # Create a constant list of shapes
        shapes = ConstantList([
            TensorShape(32, 768),
            TensorShape(32, 512),
        ])

        assert len(shapes) == 2
        assert shapes[0].dims == (32, 768)

    def test_processor_chain_with_params(self):
        """Test processor chain creation and application."""
        pytest.importorskip("torch")
        import torch
        from src.core.base.logic.processing.logits_processor import (
            LogitsProcessorList, TemperatureProcessor, TopKProcessor
        )

        chain = LogitsProcessorList([
            TemperatureProcessor(0.8),
            TopKProcessor(10),
        ])

        logits = torch.randn(100)
        result = chain([], logits)

        # Should have at most 10 non-inf values
        non_inf = (result != float("-inf")).sum()
        assert non_inf <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
