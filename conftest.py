#!/usr/bin/env python3
import os
import shutil
import pytest

# Skip tests that reference the ingested/auto external candidates tree which
# isn't present in local clones and causes many FileNotFoundErrors during
# collection. Also skip network test that expects `ipconfig` when it's absent.

ROOT = os.path.abspath(os.path.dirname(__file__))
EXTERNAL_DIR = os.path.normpath(os.path.join(ROOT, "src", "external_candidates"))


def _is_external_candidate_test(item):
    try:
        path = str(item.fspath)
    except Exception:
        return False
    return EXTERNAL_DIR in os.path.normpath(path)


def pytest_collection_modifyitems(config, items):
    skip_reason_external = "skip external_candidates tests (not present locally)"
    skip_reason_ip = "skip network test: 'ipconfig' command not found"

    ipconfig_missing = shutil.which("ipconfig") is None

    for item in list(items):
        # Skip tests under src/external_candidates
        if _is_external_candidate_test(item):
            item.add_marker(pytest.mark.skip(reason=skip_reason_external))
            continue

        # Skip network test that relies on ipconfig when it's not available
        if ipconfig_missing and os.path.basename(str(item.fspath)) == "test_network.py":
            item.add_marker(pytest.mark.skip(reason=skip_reason_ip))
