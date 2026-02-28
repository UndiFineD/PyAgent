# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-h2o-llmstudio\tests\ui\conftest.py
import logging
from functools import partial, partialmethod

import pytest

logging.TRACE = 5  # type: ignore
logging.addLevelName(logging.TRACE, "TRACE")  # type: ignore
logging.Logger.trace = partialmethod(logging.Logger.log, logging.TRACE)  # type: ignore
logging.trace = partial(logging.log, logging.TRACE)  # type: ignore


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    return logging.getLogger("ui-tests")
