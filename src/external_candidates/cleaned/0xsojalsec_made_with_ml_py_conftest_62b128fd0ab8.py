# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_made_with_ml.py\tests.py\code.py\conftest_62b128fd0ab8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Made-With-ML\tests\code\conftest.py

import pytest

from madewithml.data import CustomPreprocessor


@pytest.fixture
def dataset_loc():
    return "https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/dataset.csv"


@pytest.fixture
def preprocessor():
    return CustomPreprocessor()
