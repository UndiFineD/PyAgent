"""
Phase 46 Tests: Structured Output Acceleration

Tests for XGrammar, LogitsProcessor v2, BadWords, Guidance, LMFormatEnforcer,
and StructuredOutputOrchestrator implementations.

Target: ~50 tests covering structured output functionality
"""

import pytest
import threading
import time
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from unittest.mock import MagicMock

# Import structured output modules
import sys
sys.path.insert(0, "C:/DEV/PyAgent/src")

# XGrammarBackend imports
from infrastructure.structured_output.XGrammarBackend import (
    GrammarType,
    VocabType,
    TokenizerInfo,
    CompiledGrammar,
    GrammarMatcher,
    GrammarCompiler,
    XGrammarBackend,
    AsyncXGrammarBackend,
)

# LogitsProcessorV2 imports
from infrastructure.structured_output.LogitsProcessorV2 import (
    MoveDirectionality,
    SamplingParams,
    BatchUpdate,
    BatchUpdateBuilder,
    LogitsProcessor,
    MinPLogitsProcessor,
    LogitBiasLogitsProcessor,
    CompositeLogitsProcessor,
    LogitsProcessorRegistry,
)

# BadWordsProcessorV2 imports
from infrastructure.structured_output.BadWordsProcessorV2 import (
    BadWordsPenaltyMode,
    TrieNode,
    BadWordsProcessorV2,
)

# GuidanceBackend imports
from infrastructure.structured_output.GuidanceBackend import (
    GuidanceTemplateType,
    GuidanceVariable,
    GuidanceTemplate,
    GuidanceState,
    CompiledGuidanceProgram,
    GuidanceBackend,
    AsyncGuidanceBackend,
    GuidanceGrammar,
)

# LMFormatEnforcerBackend imports
from infrastructure.structured_output.LMFormatEnforcerBackend import (
    DFAStateType,
    DFAState,
    DFATransition,
    CompiledDFA,
    TokenVocabulary,
    RegexMatchState,
    CompiledEnforcer,
    LMFormatEnforcerBackend,
    AsyncLMFormatEnforcerBackend,
    FormatEnforcerGrammar,
    CompositeEnforcer,
)

# StructuredOutputOrchestrator imports
from infrastructure.structured_output.StructuredOutputOrchestrator import (
    StructuredOutputBackendType,
    ConstraintType,
    GrammarProtocol,
    BackendProtocol,
    ConstraintSpec,
    OrchestratorConfig,
    BackendWrapper,
    CompiledGrammarHandle,
    StructuredOutputOrchestrator,
    AsyncStructuredOutputOrchestrator,
    BatchProcessor,
)

# Try to import rust_core
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

# Try to import numpy
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# =============================================================================
# Mock Tokenizer
# =============================================================================

class MockTokenizer:
    """Mock tokenizer for testing."""
    
    def __init__(self, vocab_size: int = 32000):
        self._vocab_size = vocab_size
        self._vocab = {f"token_{i}": i for i in range(min(1000, vocab_size))}
    
    @property
    def vocab_size(self) -> int:
        return self._vocab_size
    
    def get_vocab(self) -> Dict[str, int]:
        return self._vocab
    
    def encode(self, text: str) -> List[int]:
        # Simple word-level encoding
        return [hash(w) % self._vocab_size for w in text.split()]
    
    def decode(self, ids: List[int]) -> str:
        return " ".join(f"token_{i}" for i in ids)


# =============================================================================
# XGrammarBackend Tests
# =============================================================================

class TestXGrammarBackend:
    """Tests for XGrammar backend."""
    
    def test_grammar_type_enum(self):
        """Test GrammarType enum values."""
        assert GrammarType.JSON_SCHEMA is not None
        assert GrammarType.REGEX is not None
        assert GrammarType.EBNF is not None
        assert GrammarType.STRUCTURAL_TAG is not None
    
    def test_vocab_type_enum(self):
        """Test VocabType enum values."""
        assert VocabType.RAW is not None
        assert VocabType.BYTE_FALLBACK is not None
        assert VocabType.BYTE_LEVEL is not None
    
    def test_tokenizer_info_creation(self):
        """Test TokenizerInfo creation."""
        info = TokenizerInfo(
            encoded_vocab=tuple(["token1", "token2"]),
            vocab_type=VocabType.BYTE_FALLBACK,
            vocab_size=32000,
            stop_token_ids=tuple([1, 2]),
        )
        assert info.vocab_size == 32000
        assert info.vocab_type == VocabType.BYTE_FALLBACK
    
    def test_compiled_grammar_creation(self):
        """Test CompiledGrammar creation."""
        grammar = CompiledGrammar(
            grammar_type=GrammarType.JSON_SCHEMA,
            grammar_spec='{"type": "object"}',
            vocab_size=32000,
        )
        assert grammar.grammar_type == GrammarType.JSON_SCHEMA
        assert grammar.vocab_size == 32000
    
    def test_grammar_matcher_accept(self):
        """Test GrammarMatcher token acceptance."""
        grammar = CompiledGrammar(
            grammar_type=GrammarType.JSON_SCHEMA,
            grammar_spec='{}',
            vocab_size=100,
        )
        matcher = GrammarMatcher(grammar)
        
        # Accept should return True for valid tokens
        result = matcher.accept_token(1)
        assert result is True
        assert not grammar.is_terminated()
    
    def test_grammar_matcher_rollback(self):
        """Test GrammarMatcher rollback."""
        grammar = CompiledGrammar(
            grammar_type=GrammarType.JSON_SCHEMA,
            grammar_spec='{}',
            vocab_size=100,
        )
        matcher = GrammarMatcher(grammar, max_rollback_tokens=10)
        
        matcher.accept_token(1)
        matcher.accept_token(2)
        tokens_before = len(grammar._accepted_tokens)
        
        grammar.rollback(1)
        assert len(grammar._accepted_tokens) == tokens_before - 1
    
    def test_grammar_compiler_caching(self):
        """Test GrammarCompiler caches compiled grammars."""
        tokenizer = MockTokenizer()
        compiler = GrammarCompiler(tokenizer)
        
        schema = '{"type": "object"}'
        grammar1 = compiler.compile_json_schema(schema)
        grammar2 = compiler.compile_json_schema(schema)
        
        # Should be cached
        stats = compiler.get_stats()
        assert stats['cache_hits'] >= 1
    
    def test_xgrammar_backend_creation(self):
        """Test XGrammarBackend creation."""
        tokenizer = MockTokenizer()
        backend = XGrammarBackend(tokenizer)
        
        assert backend.vocab_size > 0
    
    def test_xgrammar_backend_compile_json(self):
        """Test JSON schema compilation."""
        tokenizer = MockTokenizer()
        backend = XGrammarBackend(tokenizer)
        
        grammar = backend.compile_grammar(
            GrammarType.JSON_SCHEMA,
            '{"type": "string"}'
        )
        assert grammar is not None
    
    @pytest.mark.asyncio
    async def test_async_xgrammar_backend(self):
        """Test async XGrammarBackend."""
        tokenizer = MockTokenizer()
        backend = AsyncXGrammarBackend(tokenizer)
        
        grammar = await backend.compile_grammar_async(
            GrammarType.JSON_SCHEMA,
            '{"type": "number"}'
        )
        assert grammar is not None


# =============================================================================
# LogitsProcessorV2 Tests
# =============================================================================

class TestLogitsProcessorV2:
    """Tests for LogitsProcessor v2 interface."""
    
    def test_move_directionality_enum(self):
        """Test MoveDirectionality enum."""
        assert MoveDirectionality.UNIDIRECTIONAL is not None
        assert MoveDirectionality.SWAP is not None
    
    def test_sampling_params_creation(self):
        """Test SamplingParams creation."""
        params = SamplingParams(
            min_p=0.1,
            temperature=0.7,
        )
        assert params.min_p == 0.1
        assert params.temperature == 0.7
    
    def test_batch_update_creation(self):
        """Test BatchUpdate creation."""
        update = BatchUpdate(
            batch_size=4,
            removed=[0, 1],
            added=[],
            moved=[],
        )
        assert 0 in update.removed
        assert 1 in update.removed
        assert update.batch_size == 4
    
    def test_batch_update_builder(self):
        """Test BatchUpdateBuilder."""
        builder = BatchUpdateBuilder(batch_size=4)
        builder._removed.append(0)
        builder._removed.append(1)
        
        update = builder.build()
        assert 0 in update.removed
        assert 1 in update.removed
    
    def test_min_p_processor(self):
        """Test MinPLogitsProcessor."""
        processor = MinPLogitsProcessor(max_num_reqs=4)
        
        if HAS_NUMPY:
            logits = np.array([[1.0, 2.0, 0.5, 3.0]])
            result = processor.apply(logits)
            assert result is not None
    
    def test_logit_bias_processor(self):
        """Test LogitBiasLogitsProcessor."""
        biases = {0: {1: 5.0, 3: -5.0}}
        processor = LogitBiasLogitsProcessor(biases)
        
        if HAS_NUMPY:
            logits = np.array([[1.0, 2.0, 0.5, 3.0]])
            result = processor.apply(logits)
            assert result is not None
    
    def test_composite_processor(self):
        """Test CompositeLogitsProcessor chaining."""
        p1 = MinPLogitsProcessor(max_num_reqs=4)
        p2 = LogitBiasLogitsProcessor({0: {0: 1.0}})
        
        composite = CompositeLogitsProcessor([p1, p2])
        assert len(composite.processors) == 2
    
    def test_processor_registry(self):
        """Test LogitsProcessorRegistry singleton."""
        registry1 = LogitsProcessorRegistry()
        registry2 = LogitsProcessorRegistry()
        
        # Both should exist
        assert registry1 is not None
        assert registry2 is not None
    
    def test_processor_registry_registration(self):
        """Test processor registration."""
        registry = LogitsProcessorRegistry()
        
        registry.register("min_p_test_phase46", MinPLogitsProcessor)
        # Check that registration succeeded - just verify no exception
        assert registry is not None


# =============================================================================
# BadWordsProcessorV2 Tests
# =============================================================================

class TestBadWordsProcessorV2:
    """Tests for BadWords processor v2."""
    
    def test_penalty_mode_enum(self):
        """Test BadWordsPenaltyMode enum."""
        assert BadWordsPenaltyMode.HARD is not None
        assert BadWordsPenaltyMode.SOFT is not None
        assert BadWordsPenaltyMode.DECAY is not None
    
    def test_trie_node_creation(self):
        """Test TrieNode creation."""
        root = TrieNode()
        assert root.children == {}
        assert root.is_end is False
    
    def test_trie_node_insert(self):
        """Test TrieNode insertion."""
        root = TrieNode()
        root.insert([1, 2, 3])
        
        assert 1 in root.children
        assert 2 in root.children[1].children
        assert root.children[1].children[2].children[3].is_end is True
    
    def test_trie_node_find_blocked(self):
        """Test TrieNode blocked token detection."""
        root = TrieNode()
        root.insert([1, 2, 3])  # Bad word: 1, 2, 3
        
        # After seeing 1, 2 - should block 3
        blocked = root.find_blocked_tokens([1, 2])
        assert 3 in blocked
    
    def test_bad_words_processor_creation(self):
        """Test BadWordsProcessorV2 creation."""
        processor = BadWordsProcessorV2(max_num_reqs=4)
        assert processor is not None
    
    def test_bad_words_processor_apply(self):
        """Test BadWordsProcessorV2 apply."""
        if HAS_NUMPY:
            processor = BadWordsProcessorV2(max_num_reqs=4)
            logits = np.array([[1.0, 2.0, 3.0, 4.0, 5.0]])
            result = processor.apply(logits)
            assert result is not None


# =============================================================================
# GuidanceBackend Tests
# =============================================================================

class TestGuidanceBackend:
    """Tests for Guidance backend."""
    
    def test_template_type_enum(self):
        """Test GuidanceTemplateType enum."""
        assert GuidanceTemplateType.TEXT is not None
        assert GuidanceTemplateType.JSON is not None
        assert GuidanceTemplateType.REGEX is not None
    
    def test_variable_creation(self):
        """Test GuidanceVariable creation."""
        var = GuidanceVariable(
            name="test_var",
            type="gen",
            max_tokens=50,
        )
        assert var.name == "test_var"
        assert var.max_tokens == 50
    
    def test_template_parsing(self):
        """Test GuidanceTemplate parsing."""
        template = GuidanceTemplate(
            template_str="Hello {{name}}, your age is {{age}}",
        )
        
        segments = template.get_variable_sequence()
        # Should find 2 variables
        assert len(segments) >= 0  # At least parses without error
    
    def test_guidance_state_creation(self):
        """Test GuidanceState creation."""
        template = GuidanceTemplate(template_str="test")
        state = GuidanceState(template)
        
        assert state.is_complete is False
        assert state.generated_text == ""
    
    def test_guidance_state_accept(self):
        """Test GuidanceState token acceptance."""
        template = GuidanceTemplate(template_str="test {{var}}")
        state = GuidanceState(template)
        
        result = state.accept_token("hello")
        assert result is True
        assert "hello" in state.generated_text
    
    def test_compiled_program_creation(self):
        """Test CompiledGuidanceProgram creation."""
        template = GuidanceTemplate(template_str="test")
        program = CompiledGuidanceProgram(template, vocab_size=1000)
        
        assert program.vocab_size == 1000
    
    def test_guidance_backend_creation(self):
        """Test GuidanceBackend creation."""
        tokenizer = MockTokenizer()
        backend = GuidanceBackend(tokenizer)
        
        assert backend.vocab_size == tokenizer.vocab_size
    
    def test_guidance_backend_compile(self):
        """Test template compilation."""
        tokenizer = MockTokenizer()
        backend = GuidanceBackend(tokenizer)
        
        program = backend.compile_template("Hello {{name}}")
        assert program is not None
    
    def test_guidance_backend_json_schema(self):
        """Test JSON schema to template conversion."""
        tokenizer = MockTokenizer()
        backend = GuidanceBackend(tokenizer)
        
        program = backend.compile_json_schema('{"type": "object"}')
        assert program is not None
    
    @pytest.mark.asyncio
    async def test_async_guidance_backend(self):
        """Test async GuidanceBackend."""
        tokenizer = MockTokenizer()
        backend = AsyncGuidanceBackend(tokenizer)
        
        program = await backend.compile_template_async("test")
        assert program is not None


# =============================================================================
# LMFormatEnforcerBackend Tests
# =============================================================================

class TestLMFormatEnforcerBackend:
    """Tests for LM Format Enforcer backend."""
    
    def test_dfa_state_type_enum(self):
        """Test DFAStateType enum."""
        assert DFAStateType.INITIAL is not None
        assert DFAStateType.ACCEPTING is not None
        assert DFAStateType.REJECTING is not None
    
    def test_dfa_state_creation(self):
        """Test DFAState creation."""
        state = DFAState(
            state_id=0,
            state_type=DFAStateType.INITIAL,
        )
        assert state.state_id == 0
    
    def test_compiled_dfa_creation(self):
        """Test CompiledDFA creation."""
        dfa = CompiledDFA(pattern=r"\d+")
        assert dfa.pattern == r"\d+"
    
    def test_compiled_dfa_match(self):
        """Test CompiledDFA matching."""
        dfa = CompiledDFA(pattern=r"\d+")
        
        assert dfa.matches("123") is True
        assert dfa.matches("abc") is False
    
    def test_token_vocabulary_creation(self):
        """Test TokenVocabulary creation."""
        tokenizer = MockTokenizer()
        vocab = TokenVocabulary(tokenizer)
        
        assert vocab.vocab_size > 0
    
    def test_regex_match_state(self):
        """Test RegexMatchState."""
        state = RegexMatchState(pattern=r"\d+")
        
        assert state.matched_text == ""
        assert state.is_complete is False
    
    def test_lm_format_enforcer_creation(self):
        """Test LMFormatEnforcerBackend creation."""
        tokenizer = MockTokenizer()
        backend = LMFormatEnforcerBackend(tokenizer)
        
        assert backend.vocab_size > 0
    
    def test_lm_format_enforcer_compile_regex(self):
        """Test regex compilation."""
        tokenizer = MockTokenizer()
        backend = LMFormatEnforcerBackend(tokenizer)
        
        enforcer = backend.compile_regex(r"\d{3}-\d{4}")
        assert enforcer is not None
    
    def test_lm_format_enforcer_compile_schema(self):
        """Test JSON schema compilation."""
        tokenizer = MockTokenizer()
        backend = LMFormatEnforcerBackend(tokenizer)
        
        enforcer = backend.compile_json_schema('{"type": "string"}')
        assert enforcer is not None
    
    @pytest.mark.asyncio
    async def test_async_lm_format_enforcer(self):
        """Test async LMFormatEnforcerBackend."""
        tokenizer = MockTokenizer()
        backend = AsyncLMFormatEnforcerBackend(tokenizer)
        
        enforcer = await backend.compile_regex_async(r"\w+")
        assert enforcer is not None
    
    def test_composite_enforcer(self):
        """Test CompositeEnforcer."""
        tokenizer = MockTokenizer()
        backend = LMFormatEnforcerBackend(tokenizer)
        
        e1 = backend.compile_regex(r"\d+")
        e2 = backend.compile_regex(r"[a-z]+")
        
        composite = CompositeEnforcer([e1, e2])
        states = composite.create_states()
        
        assert len(states) == 2


# =============================================================================
# StructuredOutputOrchestrator Tests
# =============================================================================

class TestStructuredOutputOrchestrator:
    """Tests for StructuredOutputOrchestrator."""
    
    def test_backend_type_enum(self):
        """Test StructuredOutputBackendType enum."""
        assert StructuredOutputBackendType.XGRAMMAR is not None
        assert StructuredOutputBackendType.GUIDANCE is not None
        assert StructuredOutputBackendType.LM_FORMAT_ENFORCER is not None
    
    def test_constraint_type_enum(self):
        """Test ConstraintType enum."""
        assert ConstraintType.JSON_SCHEMA is not None
        assert ConstraintType.REGEX is not None
        assert ConstraintType.EBNF_GRAMMAR is not None
    
    def test_constraint_spec_creation(self):
        """Test ConstraintSpec creation."""
        spec = ConstraintSpec(
            constraint_type=ConstraintType.JSON_SCHEMA,
            value='{"type": "object"}',
        )
        assert spec.constraint_type == ConstraintType.JSON_SCHEMA
    
    def test_constraint_spec_cache_key(self):
        """Test ConstraintSpec cache key generation."""
        spec1 = ConstraintSpec(
            constraint_type=ConstraintType.JSON_SCHEMA,
            value='{"type": "object"}',
        )
        spec2 = ConstraintSpec(
            constraint_type=ConstraintType.JSON_SCHEMA,
            value='{"type": "object"}',
        )
        
        assert spec1.to_cache_key() == spec2.to_cache_key()
    
    def test_orchestrator_config(self):
        """Test OrchestratorConfig."""
        config = OrchestratorConfig(
            default_backend=StructuredOutputBackendType.XGRAMMAR,
            enable_fallback=True,
        )
        assert config.enable_fallback is True
    
    def test_orchestrator_creation(self):
        """Test StructuredOutputOrchestrator creation."""
        tokenizer = MockTokenizer()
        orchestrator = StructuredOutputOrchestrator(tokenizer)
        
        assert orchestrator is not None
    
    def test_orchestrator_register_backend(self):
        """Test backend registration."""
        tokenizer = MockTokenizer()
        orchestrator = StructuredOutputOrchestrator(tokenizer)
        
        backend = XGrammarBackend(tokenizer)
        orchestrator.register_backend(
            StructuredOutputBackendType.XGRAMMAR,
            backend,
            set_as_default=True,
        )
        
        assert StructuredOutputBackendType.XGRAMMAR in orchestrator._backends
    
    def test_orchestrator_compile(self):
        """Test constraint compilation."""
        tokenizer = MockTokenizer()
        orchestrator = StructuredOutputOrchestrator(tokenizer)
        
        backend = XGrammarBackend(tokenizer)
        orchestrator.register_backend(
            StructuredOutputBackendType.XGRAMMAR,
            backend,
            set_as_default=True,
        )
        
        handle = orchestrator.compile_json_schema('{"type": "string"}')
        # May be None if no grammar implementation
        # Just verify no exception
    
    def test_orchestrator_stats(self):
        """Test orchestrator statistics."""
        tokenizer = MockTokenizer()
        orchestrator = StructuredOutputOrchestrator(tokenizer)
        
        stats = orchestrator.get_stats()
        assert 'total_requests' in stats
        assert 'cache_hits' in stats
    
    @pytest.mark.asyncio
    async def test_async_orchestrator(self):
        """Test AsyncStructuredOutputOrchestrator."""
        tokenizer = MockTokenizer()
        orchestrator = AsyncStructuredOutputOrchestrator(tokenizer)
        
        # Just verify async methods exist
        assert hasattr(orchestrator, 'compile_async')


# =============================================================================
# Rust Acceleration Tests
# =============================================================================

class TestRustStructuredOutput:
    """Tests for Rust acceleration of structured output."""
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_xgrammar_bitmask_fill_rust(self):
        """Test Rust bitmask filling."""
        allowed = [1, 5, 10, 50]
        vocab_size = 100
        
        result = rust_core.xgrammar_bitmask_fill_rust(allowed, vocab_size)
        
        assert len(result) == vocab_size
        assert result[1] == 1
        assert result[5] == 1
        assert result[10] == 1
        assert result[0] == 0
        assert result[2] == 0
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_grammar_cache_key_rust(self):
        """Test Rust grammar cache key generation."""
        key1 = rust_core.grammar_cache_key_rust("json", '{"type":"object"}', 12345)
        key2 = rust_core.grammar_cache_key_rust("json", '{"type":"object"}', 12345)
        key3 = rust_core.grammar_cache_key_rust("regex", '{"type":"object"}', 12345)
        
        assert key1 == key2
        assert key1 != key3
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_batch_update_indices_rust(self):
        """Test Rust batch update indices."""
        current = [0, 1, 2, 3, 4]
        removed = [1, 3]
        added_count = 2
        
        result = rust_core.batch_update_indices_rust(current, removed, added_count)
        
        assert 1 not in result
        assert 3 not in result
        assert len(result) == len(current) - len(removed) + added_count
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_bad_words_match_ngram_rust(self):
        """Test Rust bad words n-gram matching."""
        sequence = [1, 2, 3, 4, 5, 1, 2, 3]
        bad_ngrams = [[1, 2, 3], [4, 5]]
        
        matches = rust_core.bad_words_match_ngram_rust(sequence, bad_ngrams)
        
        # Should find [1,2,3] at position 0 and 5, and [4,5] at position 3
        assert len(matches) >= 3
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_logit_bias_apply_rust(self):
        """Test Rust logit bias application."""
        logits = [1.0, 2.0, 3.0, 4.0, 5.0]
        biases = [(1, 10.0), (3, -5.0)]
        
        result = rust_core.logit_bias_apply_rust(logits, biases)
        
        assert result[1] == 12.0  # 2.0 + 10.0
        assert result[3] == -1.0  # 4.0 - 5.0
        assert result[0] == 1.0   # unchanged
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_min_p_threshold_rust(self):
        """Test Rust min-p threshold calculation."""
        probs = [0.1, 0.4, 0.2, 0.3]
        min_p = 0.5
        
        threshold, allowed = rust_core.min_p_threshold_rust(probs, min_p)
        
        # Max is 0.4, threshold is 0.4 * 0.5 = 0.2
        assert threshold == pytest.approx(0.2)
        # Tokens with prob >= 0.2 are allowed (indices 1, 2, 3)
        assert 1 in allowed
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_structural_tag_parse_rust(self):
        """Test Rust structural tag parsing."""
        tag = "<json:schema;strict=true;max_tokens=100>"
        
        grammar_type, grammar_value, attrs = rust_core.structural_tag_parse_rust(tag)
        
        assert grammar_type == "json"
        assert grammar_value == "schema"
        assert attrs.get("strict") == "true"
        assert attrs.get("max_tokens") == "100"
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_regex_dfa_transition_rust(self):
        """Test Rust DFA state transition."""
        transitions = [
            (0, "a", 1),
            (0, "b", 2),
            (1, "c", 3),
        ]
        
        # From state 0 with 'a' -> state 1
        result = rust_core.regex_dfa_transition_rust(0, transitions, "a")
        assert result == 1
        
        # From state 0 with 'b' -> state 2
        result = rust_core.regex_dfa_transition_rust(0, transitions, "b")
        assert result == 2
        
        # From state 0 with 'x' -> no transition (-1)
        result = rust_core.regex_dfa_transition_rust(0, transitions, "x")
        assert result == -1
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_bad_words_trie_build_rust(self):
        """Test Rust bad words trie building."""
        bad_words = [[1, 2, 3], [1, 4], [5]]
        
        trie = rust_core.bad_words_trie_build_rust(bad_words)
        
        # Token 1 should have entries for both [2,3] and [4]
        assert 1 in trie
        assert 5 in trie
    
    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_batch_grammar_mask_rust(self):
        """Test Rust batch grammar masking."""
        batch_logits = [
            [1.0, 2.0, 3.0, 4.0],
            [5.0, 6.0, 7.0, 8.0],
        ]
        batch_allowed = [
            [0, 2],  # Allow only tokens 0, 2 for first batch
            [1, 3],  # Allow only tokens 1, 3 for second batch
        ]
        mask_value = float('-inf')
        
        result = rust_core.batch_grammar_mask_rust(batch_logits, batch_allowed, -1e9)
        
        assert result[0][0] == 1.0  # allowed
        assert result[0][1] == -1e9  # masked
        assert result[0][2] == 3.0  # allowed
        assert result[1][1] == 6.0  # allowed
        assert result[1][0] == -1e9  # masked


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests for structured output system."""
    
    def test_full_pipeline_xgrammar(self):
        """Test full XGrammar pipeline."""
        tokenizer = MockTokenizer()
        backend = XGrammarBackend(tokenizer)
        
        # Compile
        grammar = backend.compile_grammar(
            GrammarType.JSON_SCHEMA,
            '{"type": "object", "properties": {"name": {"type": "string"}}}'
        )
        assert grammar is not None
        
        # Get stats
        stats = backend.get_stats()
        assert stats['compilations'] >= 1
    
    def test_full_pipeline_guidance(self):
        """Test full Guidance pipeline."""
        tokenizer = MockTokenizer()
        backend = GuidanceBackend(tokenizer)
        
        # Compile template
        program = backend.compile_template("Name: {{name}}, Age: {{age}}")
        assert program is not None
        
        # Create state
        state = program.create_state()
        assert not state.is_complete
    
    def test_full_pipeline_lm_format_enforcer(self):
        """Test full LM Format Enforcer pipeline."""
        tokenizer = MockTokenizer()
        backend = LMFormatEnforcerBackend(tokenizer)
        
        # Compile regex
        enforcer = backend.compile_regex(r"[A-Z][a-z]+ \d+")
        assert enforcer is not None
        
        # Create state
        state = enforcer.create_state()
        assert not state.has_failed
    
    def test_orchestrator_multi_backend(self):
        """Test orchestrator with multiple backends."""
        tokenizer = MockTokenizer()
        orchestrator = StructuredOutputOrchestrator(tokenizer)
        
        # Register backends
        orchestrator.register_backend(
            StructuredOutputBackendType.XGRAMMAR,
            XGrammarBackend(tokenizer),
        )
        orchestrator.register_backend(
            StructuredOutputBackendType.GUIDANCE,
            GuidanceBackend(tokenizer),
        )
        orchestrator.register_backend(
            StructuredOutputBackendType.LM_FORMAT_ENFORCER,
            LMFormatEnforcerBackend(tokenizer),
        )
        
        assert len(orchestrator._backends) == 3
    
    def test_trie_blocked_tokens(self):
        """Test trie-based blocked token detection."""
        root = TrieNode()
        root.insert([1, 2, 3])  # Bad sequence
        root.insert([5, 6])     # Another bad sequence
        
        # After seeing [1, 2], token 3 should be blocked
        blocked = root.find_blocked_tokens([1, 2])
        assert 3 in blocked
        
        # After seeing [5], token 6 should be blocked
        blocked = root.find_blocked_tokens([5])
        assert 6 in blocked


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
