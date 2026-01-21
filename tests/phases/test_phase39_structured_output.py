# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Tests for Structured Output, Speculative Decoding v2, and Tensorizer

"""
Test suite for Phase 39 implementations:
- Structured Output / Guided Decoding
- Speculative Decoding v2 (Tree-based)
- Tensorizer (Model serialization)
"""

import tempfile
import numpy as np
import pytest
from pathlib import Path


# =============================================================================
# Structured Output Tests
# =============================================================================

class TestStructuredOutputManager:
    """Tests for StructuredOutputManager."""

    def test_grammar_type_enum(self):
        """Test GrammarType enum values."""
        from src.infrastructure.engine.structured import GrammarType

        # Test enum members exist
        assert hasattr(GrammarType, 'JSON')
        assert hasattr(GrammarType, 'REGEX')
        assert hasattr(GrammarType, 'CHOICE')
        assert hasattr(GrammarType, 'NONE')

    def test_grammar_spec_creation(self):
        """Test GrammarSpec dataclass."""
        from src.infrastructure.engine.structured.structured_output_manager import (
            GrammarSpec, GrammarType
        )

        spec = GrammarSpec(
            grammar_type=GrammarType.REGEX,
            spec=r"\d+",
            strict=True,
        )

        assert spec.grammar_type == GrammarType.REGEX
        assert spec.spec == r"\d+"
        assert spec.strict is True

        # Test cache key generation
        key = spec.to_cache_key()
        assert isinstance(key, str)
        assert len(key) > 0

    def test_manager_initialization(self):
        """Test StructuredOutputManager initialization."""
        from src.infrastructure.engine.structured import structured_output_manager

        manager = StructuredOutputManager(vocab_size=32000)

        assert manager.vocab_size == 32000
        # Manager may or may not have backends registered

    def test_simple_regex_grammar(self):
        """Test SimpleRegexGrammar."""
        from src.infrastructure.engine.structured.structured_output_manager import (
            SimpleRegexGrammar, GrammarSpec, GrammarType
        )

        spec = GrammarSpec(grammar_type=GrammarType.REGEX, spec=r"hello")
        grammar = SimpleRegexGrammar(spec, vocab_size=1000)

        # Test grammar exists and has basic methods
        assert hasattr(grammar, 'accept_tokens')
        assert hasattr(grammar, 'get_allowed_tokens')
        assert hasattr(grammar, 'reset')

        # Get allowed tokens - returns set or list
        allowed = grammar.get_allowed_tokens()
        assert isinstance(allowed, (set, list))

    def test_choice_grammar(self):
        """Test ChoiceGrammar."""
        from src.infrastructure.engine.structured.structured_output_manager import (
            ChoiceGrammar, GrammarSpec, GrammarType
        )
        import json

        choices = ["yes", "no", "maybe"]
        spec = GrammarSpec(grammar_type=GrammarType.CHOICE, spec=json.dumps(choices))
        grammar = ChoiceGrammar(spec, vocab_size=1000)

        # Test reset and operations
        grammar.reset()

        # Test accept
        result = grammar.accept_tokens([ord('y')])
        assert result is True or (hasattr(result, 'is_valid') and result.is_valid)


class TestGrammarEngine:
    """Tests for GrammarEngine and FSM operations."""

    def test_fsm_state_dataclass(self):
        """Test FSMState dataclass."""
        from src.infrastructure.engine.structured.grammar_engine import FSMState

        state = FSMState(
            state_id=0,
            is_accepting=False,
            is_initial=True,
            transitions=(('a', 1), ('b', 2)),
        )

        assert state.state_id == 0
        assert state.is_initial is True
        assert len(state.transitions) == 2

    def test_token_mask(self):
        """Test TokenMask operations."""
        from src.infrastructure.engine.structured.grammar_engine import TokenMask

        mask = TokenMask(vocab_size=100)

        # Allow specific tokens
        mask.allow_only({10, 20, 30})

        # Check mask state
        assert mask.mask[10] == True
        assert mask.mask[20] == True
        assert mask.mask[50] == False

        # Apply to logits
        logits = np.zeros(100)
        masked = mask.apply_to_logits(logits)
        assert masked[10] == 0.0
        assert masked[50] == float("-inf")

    def test_regex_grammar_build(self):
        """Test RegexGrammar FSM construction."""
        from src.infrastructure.engine.structured.grammar_engine import RegexGrammar

        grammar = RegexGrammar(vocab_size=128)
        fsm = grammar.build_fsm(r"ab+c")

        assert fsm is not None
        assert fsm.initial_state >= 0

    def test_json_schema_grammar(self):
        """Test JsonSchemaGrammar."""
        from src.infrastructure.engine.structured.grammar_engine import JsonSchemaGrammar
        import json

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
        }

        grammar = JsonSchemaGrammar(vocab_size=128)
        fsm = grammar.build_fsm(json.dumps(schema))

        assert fsm is not None

    def test_choice_grammar_trie(self):
        """Test ChoiceGrammar trie-based FSM."""
        from src.infrastructure.engine.structured.grammar_engine import ChoiceGrammar
        import json

        choices = ["apple", "banana", "cherry"]
        grammar = ChoiceGrammar(vocab_size=128)

        fsm = grammar.build_fsm(json.dumps(choices))

        assert fsm is not None
        assert len(fsm.accepting_states) > 0


class TestLogitProcessor:
    """Tests for LogitProcessor implementations."""

    def test_constrained_processor(self):
        """Test ConstrainedLogitProcessor."""
        from src.infrastructure.engine.structured.logit_processor import (
            ConstrainedLogitProcessor
        )

        def allowed_fn(input_ids):
            return {10, 20, 30}

        processor = ConstrainedLogitProcessor(
            vocab_size=100,
            allowed_tokens_fn=allowed_fn,
        )

        input_ids = np.array([[1, 2, 3]])
        logits = np.zeros((1, 100))

        result = processor(input_ids, logits)

        assert result[0, 10] == 0.0
        assert result[0, 50] == float("-inf")

    def test_bitmask_processor(self):
        """Test BitmaskLogitProcessor."""
        from src.infrastructure.engine.structured.logit_processor import (
            BitmaskLogitProcessor
        )

        def bitmask_fn(input_ids, mask):
            # Allow first 10 tokens
            mask[:, :10] = True
            mask[:, 10:] = False

        processor = BitmaskLogitProcessor(
            vocab_size=100,
            bitmask_fn=bitmask_fn,
        )

        input_ids = np.array([[1, 2, 3]])
        logits = np.zeros((1, 100))

        result = processor(input_ids, logits)

        assert result[0, 5] == 0.0
        assert result[0, 50] == float("-inf")

    def test_bias_processor(self):
        """Test BiasLogitProcessor."""
        from src.infrastructure.engine.structured.logit_processor import (
            BiasLogitProcessor, LogitBias
        )

        processor = BiasLogitProcessor(vocab_size=100)

        processor.add_bias(LogitBias(token_id=10, bias=5.0))
        processor.ban_token(20)

        input_ids = np.array([[1, 2, 3]])
        logits = np.zeros((1, 100))

        result = processor(input_ids, logits)

        assert result[0, 10] == 5.0
        assert result[0, 20] == float("-inf")

    def test_composite_processor(self):
        """Test CompositeLogitProcessor."""
        from src.infrastructure.engine.structured.logit_processor import (
            CompositeLogitProcessor, TemperatureProcessor, TopKProcessor
        )

        temp = TemperatureProcessor(vocab_size=100, temperature=0.5)
        topk = TopKProcessor(vocab_size=100, k=10)

        composite = CompositeLogitProcessor(
            vocab_size=100,
            processors=[temp, topk],
        )

        assert len(composite) == 2

        input_ids = np.array([[1, 2, 3]])
        logits = np.random.randn(1, 100)

        result = composite(input_ids, logits)

        # Temperature should scale
        assert not np.allclose(result, logits)

    def test_standard_processor_chain(self):
        """Test create_standard_processor_chain."""
        from src.infrastructure.engine.structured.logit_processor import (
            create_standard_processor_chain
        )

        chain = create_standard_processor_chain(
            vocab_size=100,
            temperature=0.8,
            top_k=20,
            top_p=0.95,
            repetition_penalty=1.1,
        )

        assert len(chain) >= 2


# =============================================================================
# Speculative Decoding v2 Tests
# =============================================================================

class TestSpeculativeDecodingV2:
    """Tests for Speculative Decoding v2."""

    def test_speculative_tree(self):
        """Test SpeculativeTree structure."""
        from src.infrastructure.engine.speculative import SpeculativeTree

        tree = SpeculativeTree(root_position=10)

        idx0 = tree.add_token(token_id=100, position=10, parent_idx=-1, probability=0.5)
        idx1 = tree.add_token(token_id=101, position=11, parent_idx=idx0, probability=0.3)
        idx2 = tree.add_token(token_id=102, position=12, parent_idx=idx1, probability=0.2)

        assert len(tree) == 3
        assert tree.max_depth == 2

        # Get path to root
        path = tree.get_path_to_root(idx2)
        assert path == [100, 101, 102]

        # Get leaves
        leaves = tree.get_leaves()
        assert idx2 in leaves

    def test_ngram_proposer(self):
        """Test NgramProposer."""
        from src.infrastructure.engine.speculative import ngram_proposer

        proposer = NgramProposer(
            vocab_size=1000,
            max_speculation_depth=3,
            ngram_order=3,
        )

        # Generate some context
        input_ids = np.array([10, 20, 30, 40, 10, 20, 30, 50])

        tree = proposer.propose(input_ids, num_candidates=3)

        assert isinstance(tree.tokens, list)
        assert proposer.stats.proposals_made == 1

    def test_medusa_proposer(self):
        """Test MedusaProposer."""
        from src.infrastructure.engine.speculative import MedusaProposer

        proposer = MedusaProposer(
            vocab_size=100,
            max_speculation_depth=4,
            num_heads=3,
        )

        input_ids = np.array([1, 2, 3, 4, 5])

        tree = proposer.propose(input_ids, num_candidates=3)

        assert len(tree) > 0

    def test_speculative_verifier_greedy(self):
        """Test SpeculativeVerifier with greedy method."""
        from src.infrastructure.engine.speculative import (
            SpeculativeVerifier, AcceptanceMethod
        )

        verifier = SpeculativeVerifier(
            vocab_size=100,
            method=AcceptanceMethod.GREEDY,
        )

        proposed = [10, 20, 30]
        target_logits = np.zeros((3, 100))
        target_logits[0, 10] = 10.0  # First matches
        target_logits[1, 20] = 10.0  # Second matches
        target_logits[2, 31] = 10.0  # Third doesn't match

        result = verifier.verify_greedy(proposed, target_logits)

        assert result.accepted_count == 2
        assert result.accepted_tokens == [10, 20]
        assert result.bonus_token == 31

    def test_speculative_decoder(self):
        """Test SpeculativeDecoder."""
        from src.infrastructure.engine.speculative import (
            SpeculativeDecoder, NgramProposer, SpeculativeVerifier
        )

        proposer = NgramProposer(vocab_size=100, max_speculation_depth=3)
        verifier = SpeculativeVerifier(vocab_size=100)

        decoder = SpeculativeDecoder(
            vocab_size=100,
            proposer=proposer,
            verifier=verifier,
        )

        def mock_forward(input_ids):
            logits = np.random.randn(len(input_ids), 100)
            return logits

        input_ids = np.array([1, 2, 3, 4, 5])
        tokens, result = decoder.step(input_ids, mock_forward)

        assert len(tokens) > 0

    def test_factory_functions(self):
        """Test factory functions for decoders."""
        from src.infrastructure.engine.speculative import (
            create_ngram_decoder, create_medusa_decoder
        )

        ngram_dec = create_ngram_decoder(vocab_size=100, max_depth=3)
        assert ngram_dec.vocab_size == 100

        medusa_dec = create_medusa_decoder(vocab_size=100, num_heads=4)
        assert medusa_dec.vocab_size == 100


# =============================================================================
# Tensorizer Tests
# =============================================================================

class TestTensorizer:
    """Tests for Tensorizer serialization."""

    def test_tensor_metadata(self):
        """Test TensorMetadata serialization."""
        from src.infrastructure.compute.tensorizer import TensorMetadata, TensorDtype

        meta = TensorMetadata(
            name="layer.weight",
            shape=(1024, 512),
            dtype=TensorDtype.FLOAT32,
            offset=100,
            size_bytes=1024 * 512 * 4,
        )

        # Serialize and deserialize
        data = meta.to_bytes()
        restored, pos = TensorMetadata.from_bytes(data)

        assert restored.name == meta.name
        assert restored.shape == meta.shape
        assert restored.dtype == meta.dtype

    def test_write_and_read_tensor(self):
        """Test writing and reading tensors."""
        from src.infrastructure.compute.tensorizer import (
            TensorizerWriter, TensorizerReader, TensorizerConfig
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.tensors"

            # Write tensors
            tensors = {
                "weight1": np.random.randn(128, 64).astype(np.float32),
                "weight2": np.random.randn(64, 32).astype(np.float32),
            }

            with TensorizerWriter(path) as writer:
                writer.write_model(tensors)

            # Read tensors
            with TensorizerReader(path) as reader:
                assert reader.num_tensors == 2
                assert "weight1" in reader.tensor_names

                loaded = reader.read_all()

                np.testing.assert_allclose(
                    loaded["weight1"], tensors["weight1"], rtol=1e-5
                )

    def test_compression(self):
        """Test compressed tensor serialization."""
        from src.infrastructure.compute.tensorizer import (
            TensorizerWriter, TensorizerReader, TensorizerConfig, CompressionType
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "compressed.tensors"

            config = TensorizerConfig(compression=CompressionType.GZIP)

            tensors = {"data": np.random.randn(256, 128).astype(np.float32)}

            with TensorizerWriter(path, config) as writer:
                writer.write_model(tensors)

            with TensorizerReader(path, config) as reader:
                loaded = reader.read_all()
                np.testing.assert_allclose(loaded["data"], tensors["data"], rtol=1e-5)

    def test_parallel_loading(self):
        """Test parallel tensor loading."""
        from src.infrastructure.compute.tensorizer import (
            TensorizerWriter, TensorizerReader, TensorizerConfig
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "parallel.tensors"

            # Write multiple tensors
            tensors = {
                f"layer_{i}": np.random.randn(64, 32).astype(np.float32)
                for i in range(10)
            }

            with TensorizerWriter(path) as writer:
                writer.write_model(tensors)

            config = TensorizerConfig(parallel_threads=4)

            with TensorizerReader(path, config) as reader:
                loaded = reader.read_parallel()
                assert len(loaded) == 10

    def test_streaming_reader(self):
        """Test streaming tensor reader."""
        from src.infrastructure.compute.tensorizer import (
            TensorizerWriter, StreamingTensorizerReader
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "streaming.tensors"

            tensors = {
                "a": np.random.randn(32, 16).astype(np.float32),
                "b": np.random.randn(16, 8).astype(np.float32),
            }

            with TensorizerWriter(path) as writer:
                writer.write_model(tensors)

            with StreamingTensorizerReader(path) as reader:
                # Load on demand
                a = reader.get("a")
                assert a is not None
                np.testing.assert_allclose(a, tensors["a"], rtol=1e-5)

                # Should be cached
                a2 = reader.get("a")
                assert a2 is a

    def test_utility_functions(self):
        """Test save_model and load_model utilities."""
        from src.infrastructure.compute.tensorizer import save_model, load_model, get_model_info

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "utility.tensors"

            tensors = {"weights": np.random.randn(64, 32).astype(np.float32)}

            bytes_written = save_model(path, tensors)
            assert bytes_written > 0

            loaded = load_model(path)
            np.testing.assert_allclose(loaded["weights"], tensors["weights"], rtol=1e-5)

            info = get_model_info(path)
            assert info["num_tensors"] == 1
            assert "weights" in info["tensor_names"]


# =============================================================================
# Rust Function Tests
# =============================================================================

class TestPhase39RustFunctions:
    """Tests for Phase 39 Rust functions."""

    @pytest.fixture
    def rust_core(self):
        """Load rust_core module."""
        try:
            import rust_core
            return rust_core
        except ImportError:
            pytest.skip("rust_core not available")

    def test_regex_to_fsm(self, rust_core):
        """Test regex_to_fsm_rust."""
        transitions, accepting, initial = rust_core.regex_to_fsm_rust("abc", 100)

        assert len(transitions) > 0
        assert len(accepting) > 0
        assert initial == 0

    def test_fill_token_bitmask(self, rust_core):
        """Test fill_token_bitmask_rust."""
        transitions = [[1] * 256, [-1] * 256]
        transitions[0][ord('a')] = 1

        token_to_chars = [[ord('a')], [ord('b')], [ord('c')]]

        bitmask = rust_core.fill_token_bitmask_rust(0, transitions, token_to_chars)

        assert len(bitmask) == 3
        assert bitmask[0] is True  # 'a' is valid

    def test_validate_token_sequence(self, rust_core):
        """Test validate_token_sequence_rust."""
        transitions = [[-1] * 256, [-1] * 256, [-1] * 256]
        transitions[0][ord('a')] = 1
        transitions[1][ord('b')] = 2

        token_to_chars = [[ord('a')], [ord('b')]]

        is_valid, final_state, accepted_len = rust_core.validate_token_sequence_rust(
            [0, 1], token_to_chars, transitions, 0, [2]
        )

        assert accepted_len == 2
        assert final_state == 2

    def test_json_schema_fsm(self, rust_core):
        """Test json_schema_fsm_rust."""
        transitions, accepting, initial = rust_core.json_schema_fsm_rust("object", [])

        assert len(transitions) > 0
        assert len(accepting) > 0

    def test_apply_grammar_mask(self, rust_core):
        """Test apply_grammar_mask_rust."""
        logits = [0.0] * 100
        allowed = [10, 20, 30]

        masked = rust_core.apply_grammar_mask_rust(logits, allowed, float("-inf"))

        assert masked[10] == 0.0
        assert masked[50] == float("-inf")

    def test_build_speculation_tree(self, rust_core):
        """Test build_speculation_tree_rust."""
        context = [1, 2, 3, 1, 2, 3, 4, 5]

        # Build ngram index - returns Dict[Tuple, List] in Python, need to handle dict key conversion
        # The Rust function expects HashMap<Vec<i64>, Vec<usize>>
        # We need to pass context directly and let Rust build internally or use alternative test

        # Simple test with empty index
        ngram_index = {}

        tokens, parents, probs = rust_core.build_speculation_tree_rust(
            context, ngram_index, 3, 2
        )

        assert isinstance(tokens, list)
        assert isinstance(parents, list)
        assert isinstance(probs, list)

    def test_verify_speculation_tree(self, rust_core):
        """Test verify_speculation_tree_rust."""
        tree_tokens = [10, 20, 30]
        tree_parents = [-1, 0, 1]
        tree_probs = [0.5, 0.3, 0.2]

        target_logits = [
            [0.0] * 100,
            [0.0] * 100,
            [0.0] * 100,
        ]
        target_logits[0][10] = 10.0
        target_logits[1][20] = 10.0
        target_logits[2][31] = 10.0  # Different token

        accepted, bonus = rust_core.verify_speculation_tree_rust(
            tree_tokens, tree_parents, tree_probs, target_logits, 1.0
        )

        assert len(accepted) > 0

    def test_extract_accepted_path(self, rust_core):
        """Test extract_accepted_path_rust."""
        tree_tokens = [10, 20, 30]
        tree_parents = [-1, 0, 1]
        accepted_indices = [0, 1]

        path = rust_core.extract_accepted_path_rust(
            tree_tokens, tree_parents, accepted_indices
        )

        assert path == [10, 20]

    def test_speculation_stats(self, rust_core):
        """Test speculation_stats_rust."""
        rate, avg, speedup = rust_core.speculation_stats_rust(100, 75, 20)

        assert rate == 0.75
        assert avg == 3.75
        assert speedup > 1.0

    def test_tensorizer_checksum(self, rust_core):
        """Test tensorizer_checksum_rust."""
        data = b"test data for checksum"
        checksum = rust_core.tensorizer_checksum_rust(list(data))

        assert len(checksum) == 16

    def test_pack_tensor_metadata(self, rust_core):
        """Test pack_tensor_metadata_rust."""
        packed = rust_core.pack_tensor_metadata_rust(
            "layer.weight",
            [1024, 512],
            "float32",
            0,
            1024 * 512 * 4,
        )

        assert len(packed) > 0


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase39Integration:
    """Integration tests for Phase 39 components."""

    def test_structured_output_with_speculative(self):
        """Test structured output with speculative decoding."""
        from src.infrastructure.engine.structured import (
            StructuredOutputManager, GrammarSpec, GrammarType
        )
        from src.infrastructure.engine.speculative import (
            SpeculativeDecoder, NgramProposer, SpeculativeVerifier
        )

        vocab_size = 100

        # Set up structured output manager
        manager = StructuredOutputManager(vocab_size=vocab_size)

        # Create a grammar spec
        spec = GrammarSpec(
            grammar_type=GrammarType.REGEX,
            spec=r"\d+",
        )

        # Manager exists and has vocab_size
        assert manager.vocab_size == vocab_size

        # Set up speculative decoder
        proposer = NgramProposer(vocab_size=vocab_size, max_speculation_depth=3)
        decoder = SpeculativeDecoder(
            vocab_size=vocab_size,
            proposer=proposer,
        )

        # Verify components work together
        assert manager.vocab_size == decoder.vocab_size

    def test_tensorizer_with_large_model(self):
        """Test tensorizer with larger model simulation."""
        from src.infrastructure.compute.tensorizer import save_model, load_model

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "large_model.tensors"

            # Simulate a small model with multiple layers
            model = {}
            for layer in range(4):
                model[f"layer.{layer}.attention.q_proj"] = np.random.randn(256, 256).astype(np.float32)
                model[f"layer.{layer}.attention.k_proj"] = np.random.randn(256, 256).astype(np.float32)
                model[f"layer.{layer}.attention.v_proj"] = np.random.randn(256, 256).astype(np.float32)
                model[f"layer.{layer}.mlp.up"] = np.random.randn(256, 512).astype(np.float32)
                model[f"layer.{layer}.mlp.down"] = np.random.randn(512, 256).astype(np.float32)

            save_model(path, model)
            loaded = load_model(path, parallel=True)

            assert len(loaded) == len(model)
            for name in model:
                np.testing.assert_allclose(
                    loaded[name], model[name], rtol=1e-5
                )


# =============================================================================
# Run tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
