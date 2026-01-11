import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass

def test_sha256_text(report_module: Any) -> None:
    """Test SHA256 calculation."""
    text = "hello world"
    # echo -n "hello world" | sha256sum
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert report_module._sha256_text(text) == expected
