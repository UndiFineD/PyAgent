#!/usr/bin/env python3
import sys
from pathlib import Path
from src.core.base.managers.ResourceQuotaManager import ResourceQuotaManager, QuotaConfig

# Add workspace to path
workspace_root = Path("c:/DEV/PyAgent")
sys.path.append(str(workspace_root))


def test_quotas():
    """Test ResourceQuotaManager."""
    # Test 1: Tokens
    config = QuotaConfig(max_tokens=100)
    mgr = ResourceQuotaManager(config)

    mgr.update_usage(tokens_input=50, tokens_output=40)
    exceeded, reason = mgr.check_quotas()
    print(f"Tokens 90/100: exceeded={exceeded}")

    mgr.update_usage(tokens_output=20)
    exceeded, reason = mgr.check_quotas()
    print(f"Tokens 110/100: exceeded={exceeded}, reason={reason}")

    # Test 2: Time
    config = QuotaConfig(max_time_seconds=1)
    mgr = ResourceQuotaManager(config)
    import time
    time.sleep(1.1)
    exceeded, reason = mgr.check_quotas()
    print(f"Time exceeded: exceeded={exceeded}, reason={reason}")


if __name__ == "__main__":
    test_quotas()
