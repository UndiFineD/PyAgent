"""
Phase 17 P2 Utilities Tests.

Tests for:
- LazyLoader: Lazy module loading utilities
- HashRegistry: Hash function registry with xxhash support
- ProfileDecorators: cProfile-based profiling utilities

Phase 17: vLLM Pattern Integration (P2)
"""
import pytest
import sys
import time
import hashlib


class TestLazyLoader:
    """Tests for LazyLoader module."""
    
    def test_lazy_import_basic(self):
        """Test basic lazy import."""
        from src.core.base.utils.lazy_loader import lazy_import, LazyModule
        
        # Lazy import json module
        json_mod = lazy_import('json')
        
        # Should be a LazyModule wrapper
        assert isinstance(json_mod, LazyModule)
        
        # Accessing attribute triggers load
        result = json_mod.dumps({'test': 1})
        assert result == '{"test": 1}'
    
    def test_lazy_import_submodule(self):
        """Test lazy import of submodule."""
        from src.core.base.utils.lazy_loader import lazy_import
        
        # Import os.path lazily
        path_mod = lazy_import('os.path')
        
        # Should work
        assert path_mod.exists('.')
    
    def test_optional_import_existing(self):
        """Test optional import of existing module."""
        from src.core.base.utils.lazy_loader import optional_import
        
        # json exists - returns (module, True)
        json_mod, available = optional_import('json')
        assert available is True
        assert json_mod is not None
        assert json_mod.loads('{"a": 1}') == {'a': 1}
    
    def test_optional_import_missing(self):
        """Test optional import of missing module."""
        from src.core.base.utils.lazy_loader import optional_import
        
        # This module doesn't exist - returns (fallback, False)
        missing, available = optional_import('nonexistent_module_xyz_123')
        assert available is False
        assert missing is None
    
    def test_require_import_existing(self):
        """Test require import of existing module."""
        from src.core.base.utils.lazy_loader import require_import
        
        # json exists
        json_mod = require_import('json', 'pip install json')
        assert json_mod is not None
    
    def test_require_import_missing(self):
        """Test require import of missing module raises."""
        from src.core.base.utils.lazy_loader import require_import
        
        with pytest.raises(ImportError) as exc_info:
            require_import('nonexistent_module_xyz', 'pip install nonexistent')
        
        assert 'pip install nonexistent' in str(exc_info.value)
    
    def test_lazy_import_class(self):
        """Test LazyImport class load static method."""
        from src.core.base.utils.lazy_loader import LazyImport
        
        # Use the static method with module:attr spec
        OrderedDict = LazyImport.load('collections:OrderedDict')
        
        od = OrderedDict([('a', 1), ('b', 2)])
        assert list(od.keys()) == ['a', 'b']
    
    def test_deferred_import_success(self):
        """Test DeferredImport context manager success."""
        from src.core.base.utils.lazy_loader import DeferredImport
        
        with DeferredImport('json') as json_import:
            pass
        
        # Should load successfully
        assert json_import.available is True
        assert json_import.module is not None
    
    def test_deferred_import_missing(self):
        """Test DeferredImport with missing module."""
        from src.core.base.utils.lazy_loader import DeferredImport
        
        with DeferredImport('nonexistent_xyz_123') as missing_import:
            pass
        
        # Should report not available
        assert missing_import.available is False
        assert missing_import.module is None


class TestHashRegistry:
    """Tests for HashRegistry module."""
    
    def test_hash_sha256(self):
        """Test SHA256 hashing."""
        from src.core.base.utils.hash_registry import hash_sha256
        
        result = hash_sha256(b"hello")
        expected = hashlib.sha256(b"hello").hexdigest()
        assert result == expected
    
    def test_hash_md5(self):
        """Test MD5 hashing."""
        from src.core.base.utils.hash_registry import hash_md5
        
        result = hash_md5(b"hello")
        expected = hashlib.md5(b"hello", usedforsecurity=False).hexdigest()
        assert result == expected
    
    def test_hash_fnv1a(self):
        """Test FNV-1a hashing."""
        from src.core.base.utils.hash_registry import hash_fnv1a
        
        result = hash_fnv1a(b"hello")
        # FNV-1a is deterministic
        assert isinstance(result, str)
        assert len(result) == 16  # 64-bit hex
    
    def test_hash_xxhash64(self):
        """Test xxhash64 hashing."""
        from src.core.base.utils.hash_registry import hash_xxhash64
        
        result = hash_xxhash64(b"hello")
        assert isinstance(result, str)
        # Should be 16 hex chars (64-bit)
        assert len(result) == 16
    
    def test_safe_hash(self):
        """Test safe hash function."""
        from src.core.base.utils.hash_registry import safe_hash
        
        result = safe_hash(b"test data")
        assert isinstance(result, str)
        # Safe hash uses MD5 (32 chars) or SHA256 (64 chars) in FIPS mode
        assert len(result) in (32, 64)
    
    def test_hash_algorithm_enum(self):
        """Test HashAlgorithm enum."""
        from src.core.base.utils.hash_registry import HashAlgorithm
        
        # Enum uses auto() so values are integers, not strings
        assert HashAlgorithm.SHA256 is not None
        assert HashAlgorithm.XXHASH64 is not None
        assert HashAlgorithm.FNV1A is not None
    
    def test_get_hash_fn(self):
        """Test getting hash function by algorithm."""
        from src.core.base.utils.hash_registry import get_hash_fn, HashAlgorithm
        
        sha_fn = get_hash_fn(HashAlgorithm.SHA256)
        result = sha_fn(b"test")
        expected = hashlib.sha256(b"test").hexdigest()
        assert result == expected
    
    def test_get_hash_fn_by_name(self):
        """Test getting hash function by name."""
        from src.core.base.utils.hash_registry import get_hash_fn_by_name
        
        sha_fn = get_hash_fn_by_name('sha256')
        result = sha_fn(b"test")
        expected = hashlib.sha256(b"test").hexdigest()
        assert result == expected
    
    def test_hash_with(self):
        """Test hash_with convenience function."""
        from src.core.base.utils.hash_registry import hash_with
        
        # hash_with uses string algorithm names
        result = hash_with(b"test", 'sha256')
        expected = hashlib.sha256(b"test").hexdigest()
        assert result == expected
    
    def test_content_hasher_basic(self):
        """Test ContentHasher basic usage."""
        from src.core.base.utils.hash_registry import ContentHasher
        
        # ContentHasher uses string algorithm names
        hasher = ContentHasher(algorithm='sha256')
        result = hasher.hash(b"content")
        expected = hashlib.sha256(b"content").hexdigest()
        assert result == expected
    
    def test_content_hasher_prefix(self):
        """Test ContentHasher with prefix."""
        from src.core.base.utils.hash_registry import ContentHasher
        
        hasher = ContentHasher(algorithm='sha256', prefix="sha256")
        result = hasher.hash(b"content")
        expected = "sha256:" + hashlib.sha256(b"content").hexdigest()
        assert result == expected
    
    def test_content_hasher_truncate(self):
        """Test ContentHasher with truncation."""
        from src.core.base.utils.hash_registry import ContentHasher
        
        hasher = ContentHasher(algorithm='sha256', truncate=8)
        result = hasher.hash(b"content")
        expected = hashlib.sha256(b"content").hexdigest()[:8]
        assert result == expected
        assert len(result) == 8
    
    def test_default_hasher(self):
        """Test default hasher instance."""
        from src.core.base.utils.hash_registry import default_hasher
        
        result = default_hasher.hash(b"test")
        assert isinstance(result, str)
        # Default uses 'safe' hash (MD5=32 or SHA256=64 chars)
        assert len(result) in (32, 64)
    
    def test_fast_hasher(self):
        """Test fast hasher instance."""
        from src.core.base.utils.hash_registry import fast_hasher
        
        result = fast_hasher.hash(b"test")
        assert isinstance(result, str)
        assert len(result) == 16  # fnv1a (64-bit)
    
    def test_cache_hasher(self):
        """Test cache hasher instance."""
        from src.core.base.utils.hash_registry import cache_hasher
        
        result = cache_hasher.hash(b"test")
        assert isinstance(result, str)
        # Has prefix 'cache:' + 16 chars truncated hash
        assert result.startswith('cache:')
        assert len(result) == len('cache:') + 16
    
    def test_is_fips_mode(self):
        """Test FIPS mode detection."""
        from src.core.base.utils.hash_registry import is_fips_mode
        
        result = is_fips_mode()
        assert isinstance(result, bool)


class TestProfileDecorators:
    """Tests for ProfileDecorators module."""
    
    def test_timer_context(self):
        """Test timer context manager."""
        from src.observability.profiling.profile_decorators import timer_context
        
        with timer_context("test_op") as timing:
            time.sleep(0.01)
        
        assert timing['name'] == 'test_op'
        assert timing['elapsed_ms'] >= 10  # At least 10ms
        assert timing['elapsed_seconds'] >= 0.01
    
    def test_timer_decorator(self, capsys):
        """Test timer decorator."""
        from src.observability.profiling.profile_decorators import timer
        
        @timer("my_func")
        def slow_func():
            time.sleep(0.01)
            return 42
        
        result = slow_func()
        assert result == 42
        
        captured = capsys.readouterr()
        assert "[TIMER] my_func:" in captured.out
    
    def test_cprofile_context(self):
        """Test cprofile context manager."""
        from src.observability.profiling.profile_decorators import cprofile_context
        
        with cprofile_context(enabled=True) as result:
            sum(range(1000))
        
        assert result.elapsed_seconds > 0
        assert result.call_count > 0
    
    def test_cprofile_context_disabled(self):
        """Test cprofile context when disabled."""
        from src.observability.profiling.profile_decorators import cprofile_context
        
        with cprofile_context(enabled=False) as result:
            sum(range(1000))
        
        assert result.elapsed_seconds > 0
        assert result.stats is None  # No stats when disabled
    
    def test_cprofile_decorator(self):
        """Test cprofile decorator."""
        from src.observability.profiling.profile_decorators import cprofile
        
        @cprofile(enabled=True, print_stats=False)
        def compute():
            return sum(range(10000))
        
        result = compute()
        assert result == sum(range(10000))
    
    def test_profile_result_summary(self):
        """Test ProfileResult summary generation."""
        from src.observability.profiling.profile_decorators import ProfileResult
        
        result = ProfileResult(
            name='test',
            elapsed_seconds=0.123,
            call_count=100,
            top_functions=[('func1', 0.05), ('func2', 0.03)],
        )
        
        summary = result.summary()
        assert summary['name'] == 'test'
        assert summary['elapsed_ms'] == 123.0
        assert summary['call_count'] == 100
    
    def test_profile_accumulator(self):
        """Test ProfileAccumulator."""
        from src.observability.profiling.profile_decorators import ProfileAccumulator
        
        acc = ProfileAccumulator()
        
        @acc.track
        def tracked_func():
            time.sleep(0.001)
            return 1
        
        for _ in range(5):
            tracked_func()
        
        report = acc.report()
        assert 'tracked_func' in report
        assert report['tracked_func']['count'] == 5
        assert report['tracked_func']['avg_ms'] > 0
    
    def test_global_track_decorator(self):
        """Test global track decorator."""
        from src.observability.profiling.profile_decorators import (
            track, get_profile_report, reset_profile_data
        )
        
        reset_profile_data()
        
        @track
        def global_tracked():
            return sum(range(100))
        
        for _ in range(3):
            global_tracked()
        
        report = get_profile_report()
        assert 'global_tracked' in report
        assert report['global_tracked']['count'] == 3
        
        reset_profile_data()
        assert get_profile_report() == {}


class TestHashPerformance:
    """Performance tests for hash functions."""
    
    def test_hash_speed_comparison(self):
        """Compare speed of different hash algorithms."""
        from src.core.base.utils.hash_registry import (
            hash_sha256, hash_md5, hash_xxhash64, hash_fnv1a
        )
        
        data = b"x" * 1000  # 1KB data
        iterations = 1000
        
        results = {}
        
        # SHA256
        start = time.perf_counter()
        for _ in range(iterations):
            hash_sha256(data)
        results['sha256'] = time.perf_counter() - start
        
        # MD5
        start = time.perf_counter()
        for _ in range(iterations):
            hash_md5(data)
        results['md5'] = time.perf_counter() - start
        
        # xxhash64
        start = time.perf_counter()
        for _ in range(iterations):
            hash_xxhash64(data)
        results['xxhash64'] = time.perf_counter() - start
        
        # FNV-1a
        start = time.perf_counter()
        for _ in range(iterations):
            hash_fnv1a(data)
        results['fnv1a'] = time.perf_counter() - start
        
        # All should complete in reasonable time
        for name, elapsed in results.items():
            assert elapsed < 1.0, f"{name} too slow: {elapsed:.3f}s"
        
        # xxhash should be faster than SHA256
        # (may not always be true on all systems)
        print(f"\nHash performance ({iterations} iters, 1KB data):")
        for name, elapsed in sorted(results.items(), key=lambda x: x[1]):
            print(f"  {name}: {elapsed*1000:.2f}ms")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
