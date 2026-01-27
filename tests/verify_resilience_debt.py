
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path.cwd()))

def test_imports():
    try:
        from src.infrastructure.services.resilience.circuit_breaker import CircuitBreaker
        from src.infrastructure.services.resilience.adaptive_rate_limiter import AdaptiveRateLimiter
        from src.infrastructure.services.metrics.lora.manager import LoRAStatsManager
        from src.infrastructure.storage.kv_transfer.arc.manager import ARCOffloadManager
        print("Imports successful.")
    except Exception as e:
        print(f"Import failed: {e}")
        sys.exit(1)

def test_instantiation():
    from src.infrastructure.services.resilience.adaptive_rate_limiter import AdaptiveRateLimiter
    from src.infrastructure.services.resilience.circuit_breaker import CircuitBreaker
    
    # Test AdaptiveRateLimiter has name param
    limiter = AdaptiveRateLimiter(name="test_limiter")
    print("AdaptiveRateLimiter instantiated with name.")

    # Test CircuitBreaker instantiates
    breaker = CircuitBreaker(name="test_breaker")
    print("CircuitBreaker instantiated.")

if __name__ == "__main__":
    test_imports()
    test_instantiation()
