# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\tests\tests_fabric\__init__.py
import warnings

import pytest

# Ignore cleanup warnings from pytest (rarely happens due to a race condition when executing pytest in parallel)
warnings.filterwarnings(
    "ignore", category=pytest.PytestWarning, message=r".*\(rm_rf\) error removing.*"
)
